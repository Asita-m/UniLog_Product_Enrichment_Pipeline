import json
import os
import re

from dotenv import load_dotenv
from google import genai


load_dotenv()


client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)



def normalize_image_url(url: str) -> str:
    """
    Removes image transformation parameters
    to detect duplicate images.

    Example:

    tr:w-100/image123
    tr:w-600/image123

    become:

    image123
    """

    url = re.sub(
        r"tr:w-\d+/",
        "",
        url
    )

    return url



def deduplicate_images(images: list) -> list:
    """
    Remove duplicate images
    after ranking.
    """

    seen = set()

    unique = []


    for image in images:

        normalized = normalize_image_url(
            image["url"]
        )


        if normalized not in seen:

            seen.add(normalized)

            unique.append(image)


    return unique



def rank_product_images(
    product_name: str,
    images: list
) -> list:
    """
    Select relevant product images
    and remove duplicates.
    """


    candidates = []

    for idx, image in enumerate(images):

        candidates.append(
            {
                "id": idx,
                "url": image.get("url"),
                "alt": image.get("alt"),
                "filename": image.get("filename")
            }
        )


    prompt = f"""
You are a product catalog image ranking system.

Product:
{product_name}


Select only images that represent this exact product.

Keep:
- Main product images
- Product packaging images
- Alternate views of the same product


Reject:
- Logos
- Icons
- Category images
- Application images
- Related products
- Website decoration


Candidates:

{json.dumps(candidates, indent=2)}


Return ONLY JSON:

{{
    "selected_images": [
        {{
            "id": 0,
            "reason": "main product image"
        }}
    ]
}}
"""


    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
        config={
            "temperature": 0,
            "response_mime_type": "application/json"
        }
    )


    result = json.loads(
        response.text
    )


    selected = []


    for item in result.get(
        "selected_images",
        []
    ):

        index = item["id"]

        selected.append(
            images[index]
        )


    # Remove duplicate resolutions
    selected = deduplicate_images(
        selected
    )


    return selected
