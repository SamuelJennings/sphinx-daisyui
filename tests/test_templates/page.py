from html.parser import HTMLParser
from pathlib import Path


class Page(HTMLParser):
    """A built page, read into its start tags in the order they were written."""

    def __init__(self, text: str) -> None:
        super().__init__()
        self.tags: list[tuple[str, dict[str, str | None]]] = []
        self.text = text
        self.feed(text)

    @classmethod
    def read(cls, path: Path) -> "Page":
        """Read a built page from its file."""
        return cls(path.read_text(encoding="utf-8"))

    def inside(self, tag: str) -> "Page":
        """Read what the first tag of one kind holds, as a page of its own."""
        start = self.text.index(f"<{tag}")
        end = self.text.index(f"</{tag}>", start)
        return Page(self.text[start:end])

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.tags.append((tag, dict(attrs)))

    def find(self, tag: str, **attrs: str | None) -> list[dict[str, str | None]]:
        """Find the tags of one kind that carry every attribute given."""
        return [
            found
            for name, found in self.tags
            if name == tag and all(found.get(k) == v for k, v in attrs.items())
        ]

    def having(self, attribute: str) -> list[dict[str, str | None]]:
        """Find every tag carrying an attribute, whatever its value."""
        return [found for _, found in self.tags if attribute in found]

    def order(self, attribute: str) -> list[str | None]:
        """List the values of an attribute in document order."""
        return [found[attribute] for found in self.having(attribute)]
