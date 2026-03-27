from sentence_transformers import SentenceTransformer

class EmbeddingModel:
    def __init__(self, model_name: str = "multi-qa-distilbert-cos-v1"):
        self.model = SentenceTransformer(model_name)

    def encode(self, text: str):
        return self.model.encode(text)