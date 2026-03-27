from minsearch import Index, VectorSearch
import numpy as np
from tqdm.auto import tqdm

class Indexer:
    def __init__(self, embedding_model):
        self.embedding_model = embedding_model
        self.index = None
        self.vindex = None
        self.embeddings = None

    def build_indexes(self, documents):
        self.index = Index(
            text_fields=["name", "section", "filename"],
            keyword_fields=[]
        )
        self.index.fit(documents)

        vectors = []
        for d in tqdm(documents):
            text = d["filename"] + " " + d["section"]
            v = self.embedding_model.encode(text)
            vectors.append(v)

        self.embeddings = np.array(vectors)
        self.vindex = VectorSearch()
        self.vindex.fit(self.embeddings, documents)

        return self.index, self.vindex

    def get_text_index(self):
        return self.index

    def get_vector_index(self):
        return self.vindex