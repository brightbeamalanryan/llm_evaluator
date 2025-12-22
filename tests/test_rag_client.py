"""Tests for RAG client request profiles."""

import json

import httpx

from eval_fw.rag.client import RAGClient


def test_request_profile_builds_request() -> None:
    captured: dict[str, object] = {}

    def handler(request: httpx.Request) -> httpx.Response:
        captured["url"] = str(request.url)
        captured["method"] = request.method
        captured["headers"] = dict(request.headers)
        captured["json"] = json.loads(request.content.decode("utf-8"))
        return httpx.Response(200, json={"answer": "ok", "documents": []})

    transport = httpx.MockTransport(handler)
    client = RAGClient(
        request_profile={
            "url": "https://receive.hellotars.com/v1/stream-agent",
            "method": "POST",
            "headers": {"Content-Type": "application/json"},
            "body": {
                "query": "{{query}}",
                "account_id": "ABC",
                "prompt": "You are a helpful assistant.",
                "history": "{{history}}",
            },
        }
    )
    client._client = httpx.Client(transport=transport)

    response = client.query(
        "What time is it?",
        history=[{"query": "Hi", "answer": "Hello"}],
    )

    assert captured["url"] == "https://receive.hellotars.com/v1/stream-agent"
    assert captured["method"] == "POST"
    headers = captured["headers"]
    assert isinstance(headers, dict)
    assert headers.get("content-type") == "application/json"
    payload = captured["json"]
    assert payload["query"] == "What time is it?"
    assert payload["account_id"] == "ABC"
    assert payload["history"] == [{"query": "Hi", "answer": "Hello"}]
    assert response.answer == "ok"


def test_query_uses_legacy_endpoints_when_profile_missing() -> None:
    captured: dict[str, object] = {}

    def handler(request: httpx.Request) -> httpx.Response:
        captured["url"] = str(request.url)
        captured["method"] = request.method
        captured["json"] = json.loads(request.content.decode("utf-8"))
        return httpx.Response(200, json={"answer": "legacy", "documents": []})

    transport = httpx.MockTransport(handler)
    client = RAGClient(
        service_url="http://localhost:1234",
        query_endpoint="/query",
    )
    client._client = httpx.Client(transport=transport)

    response = client.query("Hello")

    assert captured["url"] == "http://localhost:1234/query"
    assert captured["method"] == "POST"
    payload = captured["json"]
    assert payload["query"] == "Hello"
    assert response.answer == "legacy"


def test_request_profile_sse_response_parsing() -> None:
    sse_body = (
        "event: agent_response\n"
        "data: Yes\n\n"
        "event: agent_response\n"
        "data: ,\n\n"
        "event: agent_response\n"
        "data:  I\n\n"
        "event: agent_response\n"
        "data:  can\n\n"
    )

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            content=sse_body.encode("utf-8"),
            headers={"Content-Type": "text/event-stream"},
        )

    transport = httpx.MockTransport(handler)
    client = RAGClient(
        request_profile={
            "url": "https://receive.hellotars.com/v1/stream-agent",
            "method": "POST",
            "headers": {"Content-Type": "application/json"},
            "body": {"query": "{{query}}"},
            "response_profile": {"type": "sse"},
        }
    )
    client._client = httpx.Client(transport=transport)

    response = client.query("What time is it?")

    assert response.answer == "Yes, I can"


def test_request_profile_chatbase_response_parsing() -> None:
    body = (
        'f:{"messageId":"msg-jgbFiYeabdSWZvosxPMN7yEv"}\n'
        '0:"You "\n'
        '0:"can "\n'
        '0:"contact "\n'
        '0:"the "\n'
        '0:"Chatbase "\n'
        '0:"team "\n'
        '0:"by "\n'
        '8:[{"id":"820897be-14fc-4b57-a81d-f9bb7eacc4f3","followUpId":null,'
        '"showQnaMatched":false,"matchedSources":[]}]\n'
        '0:"email "\n'
        '0:"at:\\n\\n"\n'
        '0:"support@chatbase.co"\n'
        'e:{"finishReason":"stop","usage":{"promptTokens":9600,"completionTokens":25},'
        '"isContinued":false}\n'
        'd:{"finishReason":"stop","usage":{"promptTokens":9600,"completionTokens":25}}\n'
    )

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, content=body.encode("utf-8"))

    transport = httpx.MockTransport(handler)
    client = RAGClient(
        request_profile={
            "url": "https://www.chatbase.co/api/chat/z2c2HSfKnCTh5J4650V0I",
            "method": "POST",
            "headers": {"Content-Type": "application/json"},
            "body": {"messages": [{"role": "user", "content": "{{query}}"}]},
            "response_profile": {"type": "chatbase"},
        }
    )
    client._client = httpx.Client(transport=transport)

    response = client.query("How do I reach Chatbase?")

    assert response.answer == "You can contact the Chatbase team by email at:\n\nsupport@chatbase.co"
