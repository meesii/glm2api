from __future__ import annotations

import gzip
from typing import Iterator

from curl_cffi import requests as curl_requests
from curl_cffi.requests.exceptions import HTTPError as CurlHTTPError
from curl_cffi.requests.exceptions import RequestException


DEFAULT_IMPERSONATE = "chrome"


class RequestError(Exception):
    pass


class HTTPError(Exception):
    def __init__(
        self,
        url: str,
        code: int,
        msg: str,
        headers: object,
        body: bytes,
    ) -> None:
        super().__init__(msg)
        self.url = url
        self.code = code
        self.headers = headers
        self._body = body

    def read(self) -> bytes:
        return self._body


class _HeaderView:
    def __init__(self, headers: object) -> None:
        self._headers = headers

    def get(self, key: str, default: str | None = None) -> str:
        value = self._headers.get(key) if hasattr(self._headers, "get") else None
        if value is None:
            value = self._headers.get(key.lower()) if hasattr(self._headers, "get") else None
        if value is None and hasattr(self._headers, "get"):
            for header_key, header_value in self._headers.items():
                if str(header_key).lower() == key.lower():
                    return str(header_value)
        return str(value) if value is not None else (default or "")

    def get_content_type(self) -> str:
        content_type = self.get("Content-Type", "application/octet-stream")
        return content_type.split(";", 1)[0].strip() or "application/octet-stream"


class HttpResponse:
    def __init__(self, curl_response, stream: bool = False) -> None:
        self._resp = curl_response
        self.status = int(curl_response.status_code)
        self.headers = _HeaderView(curl_response.headers)
        self._stream = stream
        self._buffer = b""
        self._iter: Iterator[bytes] | None = None
        self._closed = False
        if stream:
            self._iter = curl_response.iter_content(chunk_size=4096)

    def read(self, size: int = -1) -> bytes:
        if self._closed:
            return b""
        if not self._stream:
            content = bytes(self._resp.content or b"")
            if size < 0:
                return content
            return content[:size]

        chunk_size = 4096 if size < 0 else size
        while len(self._buffer) < chunk_size:
            if self._iter is None:
                break
            try:
                chunk = next(self._iter)
            except StopIteration:
                self._iter = None
                break
            if not chunk:
                self._iter = None
                break
            self._buffer += chunk

        if size < 0:
            size = len(self._buffer)
        result = self._buffer[:size]
        self._buffer = self._buffer[size:]
        return result

    def close(self) -> None:
        if self._closed:
            return
        self._closed = True
        self._resp.close()

    def __enter__(self) -> HttpResponse:
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()


def urlopen(
    url: str,
    *,
    method: str = "GET",
    data: bytes | None = None,
    headers: dict[str, str] | None = None,
    timeout: float = 120,
    stream: bool = False,
    impersonate: str | None = DEFAULT_IMPERSONATE,
) -> HttpResponse:
    request_headers = dict(headers or {})
    try:
        curl_response = curl_requests.request(
            method=method.upper(),
            url=url,
            data=data,
            headers=request_headers,
            timeout=timeout,
            stream=stream,
            impersonate=impersonate or DEFAULT_IMPERSONATE,
        )
    except CurlHTTPError as exc:
        response = exc.response
        body = bytes(response.content if response is not None else b"")
        status_code = int(response.status_code) if response is not None else 0
        response_headers = response.headers if response is not None else {}
        raise HTTPError(url, status_code, str(exc), response_headers, body) from exc
    except RequestException as exc:
        raise RequestError(str(exc)) from exc

    status_code = int(curl_response.status_code)
    if status_code >= 400:
        body = bytes(curl_response.content or b"")
        raise HTTPError(url, status_code, f"HTTP Error {status_code}", curl_response.headers, body)

    return HttpResponse(curl_response, stream=stream)


def read_error_body(error: HTTPError) -> dict[str, object]:
    try:
        raw_body = error.read()
        content_encoding = _HeaderView(error.headers).get("Content-Encoding", "").lower()
        if content_encoding == "gzip":
            raw_body = gzip.decompress(raw_body)
        text = raw_body.decode("utf-8", errors="ignore")
    except Exception as exc:
        return {"message": f"读取上游错误响应失败: {exc}"}
    try:
        import json

        payload = json.loads(text)
        if isinstance(payload, dict):
            return payload
    except json.JSONDecodeError:
        pass
    return {"message": text}
