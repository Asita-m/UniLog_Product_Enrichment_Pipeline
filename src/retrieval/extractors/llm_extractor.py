import os
import json

from dotenv import load_dotenv
from google import genai

from src.models.output_schema import OUTPUT_FIELDS


load_dotenv()


api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        "GEMINI_API_KEY not found"
    )


client = genai.Client(
    api_key=api_key
)


def extract_product_data(
    product_input: dict,
    content: str,
) -> dict:
    """
    Extract product information from webpage content
    using existing catalog information as context.
    """

    schema = "\n".join(
        OUTPUT_FIELDS
    )


    prompt = f"""
You are a professional product data extraction system.

Extract product information from the webpage content.

STRICT RULES:

- Return ONLY JSON.
- Do not rename fields.
- Do not remove fields.
- Every field must exist.
- Use null if information is unavailable.
- Do not invent product facts.
- Only use information available in the webpage content.

CATALOG INPUT RULES:

The following information comes from the existing catalog input.

Existing catalog values should be preserved.

Rules:

- If a catalog field already has a value, do not replace it.
- If a catalog field is null, keep it null unless the webpage explicitly provides the value.
- Do not convert null values into inferred values.
- Do not convert unbranded/no-brand placeholders into another brand.
- Do not guess missing manufacturer, brand, or catalog information.

Existing catalog information:

{json.dumps(product_input, indent=2)}


CATALOG DESCRIPTION RULES:

For these fields only:

- SHORT_DESC
- MOBILE_DESC
- INVOICE_DESC
- Part_Desc
- MARKETING_DESCRIPTION

you may create a concise catalog-friendly description using information already present in the webpage.

Rules:

- Do not add new specifications.
- Do not add unsupported claims.
- Preserve important identifiers, sizes, quantities, and brand names when available.


For:

- Includes
- Application
- ITEM_FEATURES fields

extract or summarize information from the webpage only.


ATTRIBUTE EXTRACTION RULES:

- Preserve every ATTRIBUTE_LABEL and ATTRIBUTE_VALUE pair independently.
- Do not merge multiple attributes together.
- Maintain exact relationship between attribute label and value.
- Keep attribute names as separate fields.
- If unavailable, use null.


Required fields:

{schema}


Webpage content:

{content}

"""


    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
    )


    text = response.text.strip()


    # Remove markdown formatting if Gemini adds it
    if "```" in text:
        text = text.replace(
            "```json",
            ""
        )
        text = text.replace(
            "```",
            ""
        )
        text = text.strip()


    # Extract JSON safely
    start = text.find("{")
    end = text.rfind("}")


    if start == -1 or end == -1:
        raise ValueError(
            "No JSON object found in Gemini response"
        )


    text = text[start:end + 1]


    data = json.loads(text)


    # Guarantee output schema
    for field in OUTPUT_FIELDS:
        if field not in data:
            data[field] = None


    return data
