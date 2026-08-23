from bs4 import BeautifulSoup


def extract_browser_html(page: dict) -> dict:
    """
    Extract complete rendered page content.
    No filtering happens here.
    """

    html = page.get("html", "")

    soup = BeautifulSoup(
        html,
        "html.parser"
    )

    text = soup.get_text(
        separator=" ",
        strip=True
    )

    return {
        "title": page.get("title"),
        "url": page.get("url"),
        "html": html,
        "text": text,
        "text_length": len(text),
    }
