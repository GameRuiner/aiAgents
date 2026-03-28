from .github_reader import GitHubReader
from .markdown_processor import MarkdownProcessor

class KnowledgeLoader:
    def __init__(self, owner: str, repo: str):
        self.reader = GitHubReader(owner, repo)

    def load_repository(self):
        return self.reader.read_repository()

    def chunk_sliding_window(self, text, size=2000, step=1000):
        return MarkdownProcessor.sliding_window(text, size, step)
    
    def chunk_by_paragraphs(self, text):
        return MarkdownProcessor.split_paragraphs(text)

    def chunk_by_headers(self, text, level=2):
        return MarkdownProcessor.split_by_header_level(text, level)