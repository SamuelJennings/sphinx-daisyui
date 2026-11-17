"""A module for the body tests to document."""


def greet(name: str) -> str:
    """Greet someone.

    Args:
        name: Who to greet.

    Returns:
        The greeting.
    """
    return f"Hello {name}"


class Thing:
    """A thing."""

    def method(self) -> None:
        """Do something."""
