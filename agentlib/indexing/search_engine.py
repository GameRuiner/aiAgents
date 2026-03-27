class SearchEngine:
    def __init__(self, text_index, vector_index, embedding_model):
        self.text_index = text_index
        self.vector_index = vector_index
        self.embedding_model = embedding_model

    def search(self, query: str, num_results=5):
        v_q = self.embedding_model.encode(query)
        vec_res = self.vector_index.search(v_q, num_results=num_results)

        text_res = self.text_index.search(query, num_results=num_results)

        return text_res + vec_res