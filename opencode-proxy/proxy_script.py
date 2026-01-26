import sqlite3
import json
from datetime import datetime
from mitmproxy import http
import os

DB_PATH = os.environ.get("DB_PATH", "/proxy/logs/logs.db")


def setup_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS api_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            method TEXT,
            url TEXT,
            request_headers TEXT,
            request_body TEXT,
            response_status INTEGER,
            response_headers TEXT,
            response_body TEXT,
            duration_ms REAL
        )
        """
    )
    conn.commit()
    conn.close()


def compact_streaming_response(raw_body: str) -> str:
    """Compact SSE streaming chunks into a single response."""
    chunks = []
    content_parts = []
    metadata = {}

    for line in raw_body.split("\n"):
        line = line.strip()
        if not line.startswith("data:"):
            continue

        data_str = line[5:].strip()
        if data_str == "[DONE]":
            continue

        try:
            chunk = json.loads(data_str)
            chunks.append(chunk)

            if not metadata and "id" in chunk:
                metadata = {
                    "id": chunk.get("id"),
                    "model": chunk.get("model"),
                    "created": chunk.get("created"),
                    "object": chunk.get("object", "chat.completion"),
                }

            for choice in chunk.get("choices", []):
                delta = choice.get("delta", {})
                if "content" in delta and delta["content"]:
                    content_parts.append(delta["content"])
                if "finish_reason" in choice and choice["finish_reason"]:
                    metadata["finish_reason"] = choice["finish_reason"]
        except json.JSONDecodeError:
            continue

    if not chunks:
        return raw_body

    compacted = {
        **metadata,
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": "".join(content_parts),
                },
                "finish_reason": metadata.get("finish_reason", "stop"),
            }
        ],
        "_streaming": True,
        "_chunk_count": len(chunks),
    }

    return json.dumps(compacted, indent=2)


setup_database()


class APILogger:
    def __init__(self):
        self.flows = {}

    def request(self, flow: http.HTTPFlow) -> None:
        self.flows[flow] = datetime.now()

    def response(self, flow: http.HTTPFlow) -> None:
        if flow not in self.flows:
            return

        start_time = self.flows[flow]
        duration = (datetime.now() - start_time).total_seconds() * 1000

        request_body = (
            flow.request.content.decode("utf-8", errors="replace")
            if flow.request.content
            else ""
        )
        response_body = (
            flow.response.content.decode("utf-8", errors="replace")
            if flow.response.content
            else ""
        )

        content_type = flow.response.headers.get("content-type", "")
        if "text/event-stream" in content_type or response_body.startswith("data:"):
            response_body = compact_streaming_response(response_body)

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO api_logs (
                timestamp, method, url, request_headers, request_body,
                response_status, response_headers, response_body, duration_ms
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                start_time.isoformat(),
                flow.request.method,
                flow.request.pretty_url,
                json.dumps(dict(flow.request.headers)),
                request_body,
                flow.response.status_code,
                json.dumps(dict(flow.response.headers)),
                response_body,
                duration,
            ),
        )
        conn.commit()
        conn.close()

        del self.flows[flow]


addons = [APILogger()]
