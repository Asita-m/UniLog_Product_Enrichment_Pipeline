import json
import os

from dotenv import load_dotenv
from google import genai

from src.models.product import Product
from src.models.source import Source


load_dotenv()


client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)



def rank_sources(
    product: Product,
    sources: list[Source]
) -> Source:
    """
    Select the best product source using LLM reasoning.

    This does not fetch webpages.
    It only ranks discovered URLs.
    """


    candidates = []


    for idx, source in enumerate(sources):

        candidates.append(
            {
                "id": idx,
                "title": source.title,
                "url": source.url,
                "domain": source.domain,
            }
        )


    prompt = f"""
You are a product catalog source ranking system.

Your job is to select the best webpage
for extracting a complete product catalog record.

Product:

Manufacturer Part Number:
{product.mpn}

Description:
{product.description}

Brand:
{product.e1_brand}

Manufacturer:
{product.manufacturer}


Evaluate these candidate sources:

{json.dumps(candidates, indent=2)}


Ranking preference:

Highest priority:
- Official manufacturer product pages
- Product detail pages from trusted distributors
- Retail product pages with specifications,
  dimensions, features, images

Lower priority:
- User manuals
- Installation guides
- PDF documents
- Category pages
- Search pages
- Accessories pages
- Reviews


Consider:

- Does the URL appear to represent this exact product?
- Does the title match the product?
- Is this likely to contain specifications?
- Is this useful for building a catalog record?


Return ONLY JSON:

{{
    "best_source_id": 0,
    "reason": "short explanation"
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


    selected_id = result.get(
        "best_source_id"
    )


    if selected_id is None:
        raise Exception(
            "LLM did not return source id"
        )


    print(
        "SOURCE RANKING REASON:",
        result.get("reason")
    )


    return sources[selected_id]
