from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os
import json
import re


def extract_assets(
    html: str,
    base_url: str
) -> dict:
    """
    Collect all possible webpage assets.

    Image selection happens later
    through semantic ranking.
    """

    soup = BeautifulSoup(
        html,
        "html.parser"
    )


    images = []
    documents = []


    def add_image(url, alt=""):

        if not url:
            return


        url = url.strip()


        if url.startswith("//"):
            url = "https:" + url


        url = urljoin(
            base_url,
            url
        )


        filename = os.path.basename(
            url.split("?")[0]
        )


        images.append(
            {
                "url": url,
                "alt": alt,
                "filename": filename,
                "type": "image"
            }
        )



    # -------------------------
    # Collect <img> images
    # -------------------------

    for img in soup.find_all("img"):

        attributes = [
            "src",
            "data-src",
            "data-original",
            "data-lazy",
            "data-image"
        ]


        for attr in attributes:

            src = img.get(attr)

            if src:
                add_image(
                    src,
                    img.get("alt", "")
                )


        srcset = img.get("srcset")

        if srcset:

            for item in srcset.split(","):

                add_image(
                    item.split()[0],
                    img.get("alt", "")
                )



    # -------------------------
    # OpenGraph images
    # -------------------------

    for meta in soup.find_all(
        "meta"
    ):

        if meta.get("property") in [
            "og:image",
            "og:image:url"
        ]:

            add_image(
                meta.get("content"),
                "og:image"
            )



    # -------------------------
    # JSON-LD images
    # -------------------------

    for script in soup.find_all(
        "script",
        type="application/ld+json"
    ):

        try:

            data = json.loads(
                script.string
            )


            json_text = json.dumps(
                data
            )


            found = re.findall(
                r'https?://[^"]+\.(?:jpg|jpeg|png|webp)[^"]*',
                json_text,
                re.I
            )


            for url in found:

                add_image(
                    url,
                    "json-ld"
                )


        except Exception:

            continue



    # -------------------------
    # Collect documents
    # -------------------------

    for link in soup.find_all("a"):

        href = link.get("href")


        if not href:
            continue


        url = urljoin(
            base_url,
            href
        )


        text = link.get_text(
            " ",
            strip=True
        )


        filename = os.path.basename(
            url.split("?")[0]
        )


        if (
            ".pdf" in url.lower()
            or
            any(
                word in (
                    text.lower()
                    + " "
                    + url.lower()
                )
                for word in [
                    "manual",
                    "spec",
                    "sheet",
                    "catalog",
                    "warranty",
                    "instruction",
                    "safety"
                ]
            )
        ):

            documents.append(
                {
                    "url": url,
                    "text": text,
                    "filename": filename,
                    "type": "document"
                }
            )


    return {
        "images": images,
        "documents": documents
    }
