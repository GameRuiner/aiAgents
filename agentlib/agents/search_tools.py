from typing import List, Any

class SearchTool:
    def __init__(self, kb):
        self.kb = kb

    def search(self, query: str) -> List[Any]:
        """
        Perform a text-based search on the documentation knowledge base.

        Args:
            query (str): The search query string.

        Returns:
            List[Any]: A list of up to 5 search results returned by the documentation knowledge base.
        """
        return self.kb.query(query, num_results=5)