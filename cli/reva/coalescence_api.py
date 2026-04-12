"""Small REST client for Coalescence platform operations used by reva."""

from __future__ import annotations

import json
import mimetypes
import uuid
from pathlib import Path
from urllib import error, request


BASE_URL = "https://coale.science/api/v1"


class CoalescenceAPIError(RuntimeError):
    """Raised when the Coalescence REST API returns an error response."""

    def __init__(self, status: int, message: str):
        super().__init__(f"Coalescence API error {status}: {message}")
        self.status = status
        self.message = message


class CoalescenceRestClient:
    """Minimal stdlib-only client for authenticated Coalescence REST calls."""

    def __init__(self, api_key: str, base_url: str = BASE_URL):
        self.api_key = api_key.strip()
        self.base_url = base_url.rstrip("/")

    def create_paper(
        self,
        *,
        title: str,
        abstract: str,
        domain: str,
        pdf_url: str | None = None,
        github_repo_url: str | None = None,
    ) -> dict:
        payload = {
            "title": title,
            "abstract": abstract,
            "domain": domain,
        }
        if pdf_url:
            payload["pdf_url"] = pdf_url
        if github_repo_url:
            payload["github_repo_url"] = github_repo_url
        return self._json_request("POST", "/papers/", payload, expected_status=201)

    def upload_paper_pdf(self, paper_id: str, pdf_path: Path) -> dict:
        body, content_type = _multipart_file_body("file", pdf_path)
        return self._request(
            "POST",
            f"/papers/{paper_id}/upload-pdf",
            body=body,
            headers={"Content-Type": content_type},
            expected_status=200,
        )

    def _json_request(
        self,
        method: str,
        path: str,
        payload: dict,
        *,
        expected_status: int,
    ) -> dict:
        body = json.dumps(payload).encode("utf-8")
        return self._request(
            method,
            path,
            body=body,
            headers={"Content-Type": "application/json"},
            expected_status=expected_status,
        )

    def _request(
        self,
        method: str,
        path: str,
        *,
        body: bytes,
        headers: dict[str, str],
        expected_status: int,
    ) -> dict:
        req = request.Request(
            f"{self.base_url}{path}",
            data=body,
            method=method,
            headers={**headers, "Authorization": _authorization_value(self.api_key)},
        )
        try:
            with request.urlopen(req, timeout=60) as resp:
                payload = resp.read().decode("utf-8")
                if resp.status != expected_status:
                    raise CoalescenceAPIError(resp.status, payload)
                return json.loads(payload) if payload else {}
        except error.HTTPError as exc:
            payload = exc.read().decode("utf-8", errors="replace")
            raise CoalescenceAPIError(exc.code, payload) from exc
        except error.URLError as exc:
            raise CoalescenceAPIError(0, str(exc.reason)) from exc


def _authorization_value(api_key: str) -> str:
    if api_key.startswith("Bearer ") or api_key.startswith("cs_"):
        return api_key
    return f"Bearer {api_key}"


def _multipart_file_body(field_name: str, path: Path) -> tuple[bytes, str]:
    boundary = f"----reva-{uuid.uuid4().hex}"
    content_type = mimetypes.guess_type(path.name)[0] or "application/pdf"
    disposition = (
        f'--{boundary}\r\n'
        f'Content-Disposition: form-data; name="{field_name}"; filename="{path.name}"\r\n'
        f"Content-Type: {content_type}\r\n\r\n"
    ).encode("utf-8")
    closing = f"\r\n--{boundary}--\r\n".encode("utf-8")
    return disposition + path.read_bytes() + closing, f"multipart/form-data; boundary={boundary}"
