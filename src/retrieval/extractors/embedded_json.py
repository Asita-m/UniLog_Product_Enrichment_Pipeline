import json
import re

from bs4 import BeautifulSoup


PRODUCT_KEYS = {
    "name",
    "title",
    "sku",
    "mpn",
    "model",
    "brand",
    "description",
    "productid",
    "product_id",
}


def extract_embedded_json(
    page: dict,
    product_mpn: str | None = None
) -> dict:
    """
    Extract product-like information from
    embedded JavaScript/JSON in a webpage.

    If product_mpn is provided, only keep
    extracted data that appears related
    to that product.
    """

    html = page.get("html", "")

    soup = BeautifulSoup(
        html,
        "html.parser"
    )

    evidence = {}

    scripts = soup.find_all("script")

    for script in scripts:

        if not script.string:
            continue

        content = script.string.strip()

        extracted = {}


        # Try parsing pure JSON blocks
        try:
            data = json.loads(content)

            extracted.update(
                extract_fields(data)
            )

        except json.JSONDecodeError:
            pass


        # Try extracting JSON-like values from JS
        extracted.update(
            extract_from_text(content)
        )


        # Validate against product MPN
        if extracted:

            if product_mpn:

                if matches_product(
                    extracted,
                    product_mpn
                ):
                    evidence.update(extracted)

            else:
                evidence.update(extracted)


    return evidence



def extract_fields(
    data,
    result=None
):
    """
    Recursively search dictionaries/lists
    for product-related keys.
    """

    if result is None:
        result = {}


    if isinstance(data, dict):

        for key, value in data.items():

            normalized_key = (
                key.lower()
                .replace("-", "_")
                .replace(" ", "_")
            )

            if normalized_key in PRODUCT_KEYS:

                result[normalized_key] = value


            elif isinstance(
                value,
                (dict, list)
            ):
                extract_fields(
                    value,
                    result
                )


    elif isinstance(data, list):

        for item in data:

            extract_fields(
                item,
                result
            )


    return result



def extract_from_text(
    text: str
) -> dict:
    """
    Extract obvious key-value pairs
    from JavaScript objects.
    """

    result = {}

    patterns = {
        "sku": r'"sku"\s*:\s*"([^"]+)"',
        "mpn": r'"mpn"\s*:\s*"([^"]+)"',
        "name": r'"name"\s*:\s*"([^"]+)"',
        "description": r'"description"\s*:\s*"([^"]+)"',
    }


    for key, pattern in patterns.items():

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:
            result[key] = match.group(1)


    return result



def matches_product(
    data: dict,
    product_mpn: str
) -> bool:
    """
    Check whether extracted data
    belongs to the requested product.
    """

    product_mpn = product_mpn.lower()


    for value in data.values():

        if isinstance(value, str):

            if product_mpn in value.lower():
                return True


    return False
