"""RAG service client."""

from dataclasses import dataclass, field
from typing import Any
import httpx


@dataclass
class RetrievedDocument:
    """A document retrieved from the RAG service."""

    content: str
    score: float = 0.0
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class RAGResponse:
    """Response from a RAG query."""

    answer: str
    retrieved_docs: list[RetrievedDocument] = field(default_factory=list)
    raw_response: dict[str, Any] = field(default_factory=dict)


class RAGClient:
    """Client for interacting with a RAG service."""

    def __init__(
        self,
        service_url: str = "http://localhost:8091",
        query_endpoint: str = "/query",
        retrieve_endpoint: str = "/retrieve",
        ingest_endpoint: str = "/ingest",
        timeout: float = 30.0,
    ) -> None:
        """Initialize the RAG client.

        Args:
            service_url: Base URL of the RAG service.
            query_endpoint: Endpoint for query requests.
            retrieve_endpoint: Endpoint for retrieve-only requests.
            ingest_endpoint: Endpoint for ingesting documents.
            timeout: Request timeout in seconds.
        """
        self.service_url = service_url.rstrip("/")
        self.query_endpoint = query_endpoint
        self.retrieve_endpoint = retrieve_endpoint
        self.ingest_endpoint = ingest_endpoint
        self.timeout = timeout
        self._client = httpx.Client(timeout=timeout)

    def query(self, query: str, **kwargs: Any) -> RAGResponse:
        """Send a query to the RAG service and get a response with retrieved docs.

        Args:
            query: The query string.
            **kwargs: Additional parameters to pass to the service.

        Returns:
            RAGResponse with answer and retrieved documents.
        """
        url = f"{self.service_url}{self.query_endpoint}"
        payload = {"query": query, **kwargs}

        try:
            response = self._client.post(url, json=payload)
            response.raise_for_status()
            data = response.json()
            return self._parse_response(data)
        except httpx.HTTPError as e:
            return RAGResponse(
                answer=f"Error: {str(e)}",
                raw_response={"error": str(e)},
            )

    def retrieve(self, query: str, top_k: int = 5, **kwargs: Any) -> list[RetrievedDocument]:
        """Retrieve documents without generating a response.

        Args:
            query: The query string.
            top_k: Number of documents to retrieve.
            **kwargs: Additional parameters to pass to the service.

        Returns:
            List of retrieved documents.
        """
        url = f"{self.service_url}{self.retrieve_endpoint}"
        payload = {"query": query, "top_k": top_k, **kwargs}

        try:
            response = self._client.post(url, json=payload)
            response.raise_for_status()
            data = response.json()
            return self._parse_documents(data.get("documents", []))
        except httpx.HTTPError:
            return []

    def ingest(self, content: str, metadata: dict[str, Any] | None = None) -> bool:
        """Ingest a document into the RAG service.

        Args:
            content: Document content to ingest.
            metadata: Optional metadata for the document.

        Returns:
            True if ingestion was successful.
        """
        url = f"{self.service_url}{self.ingest_endpoint}"
        payload = {"content": content, "metadata": metadata or {}}

        try:
            response = self._client.post(url, json=payload)
            response.raise_for_status()
            return True
        except httpx.HTTPError:
            return False

    def _parse_response(self, data: dict[str, Any]) -> RAGResponse:
        """Parse a RAG service response into a RAGResponse object."""
        answer = data.get("answer", data.get("response", ""))
        docs = self._parse_documents(data.get("documents", data.get("sources", [])))

        return RAGResponse(
            answer=answer,
            retrieved_docs=docs,
            raw_response=data,
        )

    def _parse_documents(self, docs: list[dict[str, Any]]) -> list[RetrievedDocument]:
        """Parse document data into RetrievedDocument objects."""
        result = []
        for doc in docs:
            result.append(
                RetrievedDocument(
                    content=doc.get("content", doc.get("text", "")),
                    score=doc.get("score", doc.get("similarity", 0.0)),
                    metadata=doc.get("metadata", {}),
                )
            )
        return result

    def close(self) -> None:
        """Close the HTTP client."""
        self._client.close()

    def __enter__(self) -> "RAGClient":
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()


class MockRAGClient(RAGClient):
    """Mock RAG client for testing without a running service."""

    def __init__(self, **kwargs: Any) -> None:
        """Initialize the mock client (ignores service URL)."""
        super().__init__(**kwargs)
        self._mock_docs: list[dict[str, Any]] = []
        self._mock_responses: dict[str, str] = {}

    def add_mock_document(self, content: str, metadata: dict[str, Any] | None = None) -> None:
        """Add a mock document to be returned in retrieval."""
        self._mock_docs.append({
            "content": content,
            "metadata": metadata or {},
            "score": 0.9,
        })

    def set_mock_response(self, query: str, response: str) -> None:
        """Set a mock response for a specific query."""
        self._mock_responses[query] = response

    def query(self, query: str, **kwargs: Any) -> RAGResponse:
        """Return a mock response."""
        answer = self._mock_responses.get(
            query,
            f"Mock response for: {query}",
        )
        docs = [
            RetrievedDocument(
                content=d["content"],
                score=d.get("score", 0.9),
                metadata=d.get("metadata", {}),
            )
            for d in self._mock_docs
        ]
        return RAGResponse(
            answer=answer,
            retrieved_docs=docs,
            raw_response={"mock": True},
        )

    def retrieve(self, query: str, top_k: int = 5, **kwargs: Any) -> list[RetrievedDocument]:
        """Return mock documents."""
        docs = self._mock_docs[:top_k]
        return [
            RetrievedDocument(
                content=d["content"],
                score=d.get("score", 0.9),
                metadata=d.get("metadata", {}),
            )
            for d in docs
        ]

    def ingest(self, content: str, metadata: dict[str, Any] | None = None) -> bool:
        """Mock ingest always succeeds."""
        self.add_mock_document(content, metadata)
        return True
