import re
from typing import List

class MarkdownProcessor:

    @staticmethod
    def split_by_header_level(text: str, level: int = 2) -> List[str]:
        """Split markdown text by a specific header level."""
        header_pattern = rf"^(#{{{level}}} )(.+)$"
        pattern = re.compile(header_pattern, re.MULTILINE)

        parts = pattern.split(text)
        sections = []

        for i in range(1, len(parts), 3):
            header = (parts[i] + parts[i+1]).strip()
            content = parts[i+2].strip() if i + 2 < len(parts) else ""
            sections.append(f"{header}\n\n{content}" if content else header)

        return sections

    @staticmethod
    def sliding_window(text: str, size: int, step: int):
        """Chunk text using a sliding window."""
        if size <= 0 or step <= 0:
            raise ValueError("size and step must be positive")

        chunks = []
        n = len(text)

        for i in range(0, n, step):
            chunk = text[i:i+size]
            chunks.append({"start": i, "chunk": chunk})
            if i + size >= n:
                break

        return chunks

    @staticmethod
    def split_paragraphs(text: str):
        """
        Chunk markdown into paragraphs separated by empty lines.
        """
        return re.split(r"(?:\r?\n\s*){2,}", text.strip())