from .knowledge_loader.loader import KnowledgeLoader
from .models.embedding_model import EmbeddingModel
from .indexing.indexer import Indexer
from .indexing.search_engine import SearchEngine

class KnowledgeBase:
    def __init__(self, owner: str, repo: str, header_level=2):
        self.loader = KnowledgeLoader(owner, repo)
        self.embedding_model = EmbeddingModel()
        self.indexer = None
        self.engine = None
        self.header_level = header_level

    def build(self):
        docs = self.loader.load_repository()
        chunks = []

        for doc in docs:
            meta = doc.copy()
            content = meta.pop("content")
            sections = self.loader.chunk_by_headers(content, level=self.header_level)

            for section in sections:
                d = meta.copy()
                d["section"] = section
                chunks.append(d)

        self.indexer = Indexer(self.embedding_model)
        text_index, vector_index = self.indexer.build_indexes(chunks)

        self.engine = SearchEngine(text_index, vector_index, self.embedding_model)

    def query(self, text: str, num_results=5):
        if not self.engine:
            raise RuntimeError("Knowledge base not built. Call build() first.")
        return self.engine.search(text, num_results=num_results)