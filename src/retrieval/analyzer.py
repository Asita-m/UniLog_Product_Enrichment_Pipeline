from bs4 import BeautifulSoup


def analyze_source(page: dict) -> dict:
    """
    Analyze a fetched webpage and determine
    what extraction methods might work.
    """

    html = page.get("html", "")

    soup = BeautifulSoup(
        html,
        "html.parser"
    )


    analysis = {
        "content_type": page.get("content_type"),
        "has_json_ld": False,
        "has_scripts": False,
        "has_embedded_json": False,
        "has_product_keywords": False,
        "frameworks": [],
        "recommended_extractor": None,
    }


    # Check JSON-LD
    for script in soup.find_all(
        "script",
        type="application/ld+json"
    ):
        analysis["has_json_ld"] = True
        break


    # Check JavaScript
    scripts = soup.find_all("script")

    if scripts:
        analysis["has_scripts"] = True


    html_lower = html.lower()


    # Detect possible embedded data
    json_keywords = [
        "product",
        "sku",
        "mpn",
        "brand",
        "offers",
        "description",
    ]

    keyword_matches = 0

    for keyword in json_keywords:
        if keyword in html_lower:
            keyword_matches += 1


    if keyword_matches >= 3:
        analysis["has_embedded_json"] = True
        analysis["has_product_keywords"] = True


    # Detect common frameworks
    frameworks = {
        "react": [
            "__next",
            "react",
            "_reactroot",
        ],
        "vue": [
            "__vue__",
            "vue",
        ],
        "angular": [
            "ng-version",
        ],
        "shopify": [
            "shopify",
        ],
    }


    for framework, indicators in frameworks.items():
        for indicator in indicators:
            if indicator in html_lower:
                analysis["frameworks"].append(
                    framework
                )
                break


    # Decide first extraction strategy
    if analysis["has_json_ld"]:
        analysis["recommended_extractor"] = "json_ld"

    elif analysis["has_embedded_json"]:
        analysis["recommended_extractor"] = "embedded_json"

    else:
        analysis["recommended_extractor"] = "html"


    return analysis
