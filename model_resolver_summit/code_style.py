from typing import Any

from pygments import lex
from pygments.lexers import get_lexer_by_name
from pygments.styles import get_style_by_name
from pygments.token import Token


def tokenize_code(code: str, style_name: str = "material", lexer: str = "python") -> list[dict]:
    """
    Tokenizes a Python code string and returns a list of
    {text, color, bold, italic} dicts ready for UI rendering.

    Args:
        code: The Python source code string to highlight.
        style_name: A Pygments style name (e.g. "monokai", "dracula").

    Returns:
        List of token dicts with keys: text, color, bold, italic.
    """
    style = get_style_by_name(style_name)
    lexer = get_lexer_by_name(lexer)
    default_color = (
        f"#{style.style_for_token(Token)['color']}"
        if style.style_for_token(Token)["color"]
        else "#000000"
    )

    tokens: list[dict[str, Any]] = []
    for token_type, value in lex(code, lexer):
        entry = style.style_for_token(token_type)
        tokens.append(
            {
                "text": value,
                "color": f"#{entry['color']}" if entry["color"] else default_color,
                "bold": entry["bold"],
                "italic": entry["italic"],
            }
        )

    return tokens
