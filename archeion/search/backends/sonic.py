from typing import List

try:
    from sonic import IngestClient, SearchClient
except ImportError:
    raise RuntimeError("sonic-client is not installed")

MAX_SONIC_TEXT_TOTAL_LENGTH = 100_000_000  # don't index more than 100 million characters per text
MAX_SONIC_TEXT_CHUNK_LENGTH = 2_000  # don't index more than 2000 characters per chunk
MAX_SONIC_ERRORS_BEFORE_ABORT = 5


class SonicSearchBackend:
    """Uses sonic as a search backend."""

    def __init__(self, config: dict):
        self.config = config
        self.host = config["host"]
        self.port = config["port"]
        self.password = config["password"]
        self.bucket = config["bucket"]
        self.collection = config["collection"]

    def index_link(self, link_id: str, tags: List[str]) -> None:
        """Index a link."""
        pass

    def index_artifact(self, artifact_id: str, link_id: str, content: str) -> None:
        error_count = 0
        with IngestClient(self.host, self.port, self.password) as ingestcl:
            chunks = (
                content[i : i + MAX_SONIC_TEXT_CHUNK_LENGTH]
                for i in range(
                    0,
                    min(len(content), MAX_SONIC_TEXT_TOTAL_LENGTH),
                    MAX_SONIC_TEXT_CHUNK_LENGTH,
                )
            )
            try:
                doc_id = f"{link_id}/{artifact_id}"
                for chunk in chunks:
                    ingestcl.push(self.collection, self.bucket, doc_id, str(chunk))
                ingestcl.flush_object(self.collection, self.bucket, doc_id)
            except Exception as err:
                print(f"[!] Sonic search backend threw an error while indexing: {err.__class__.__name__} {err}")
                error_count += 1
                if error_count > MAX_SONIC_ERRORS_BEFORE_ABORT:
                    raise

    def search(self, query: str) -> List[str]:
        with SearchClient(self.host, self.port, self.password) as querycl:
            doc_ids = querycl.query(self.collection, self.bucket, query)
        return [doc_id.split("/")[0] for doc_id in doc_ids]
