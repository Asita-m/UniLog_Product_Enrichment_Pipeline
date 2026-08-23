from playwright.sync_api import sync_playwright

from src.models.source import Source


def fetch_with_browser(source: Source) -> dict:
    """
    Render a webpage using a real browser.
    """

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=False,
            args=[
                "--disable-blink-features=AutomationControlled"
            ]
        )


        context = browser.new_context(

            user_agent=(
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 "
                "(KHTML, like Gecko) "
                "Chrome/139.0.0.0 Safari/537.36"
            ),

            viewport={
                "width": 1280,
                "height": 900
            },

            locale="en-US",

            extra_http_headers={
                "Accept-Language": "en-US,en;q=0.9"
            }
        )


        page = context.new_page()


        page.goto(
            source.url,
            wait_until="domcontentloaded",
            timeout=60000,
        )


        # Wait for JS-rendered content
        page.wait_for_timeout(5000)


        # Scroll to trigger lazy-loaded sections/images
        page.evaluate(
            """
            window.scrollTo(
                0,
                document.body.scrollHeight
            )
            """
        )


        page.wait_for_timeout(5000)


        # Try to wait for product content
        try:

            page.wait_for_selector(
                "h1",
                timeout=10000
            )

        except:

            pass


        html = page.content()

        title = page.title()


        context.close()
        browser.close()


    return {
        "url": source.url,
        "title": title,
        "html": html,
        "content_type": "text/html",
    }
