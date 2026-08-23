import streamlit as st
import pandas as pd
import subprocess
import os


# -------------------------
# Ensure Playwright browser
# exists on Streamlit Cloud
# -------------------------

PLAYWRIGHT_PATH = "/home/appuser/.cache/ms-playwright"


if not os.path.exists(PLAYWRIGHT_PATH):

    st.info(
        "Installing browser dependencies..."
    )

    subprocess.run(
        [
            "playwright",
            "install",
            "chromium"
        ],
        check=True
    )


# -------------------------
# Pipeline imports
# -------------------------

from main import (
    load_products,
    build_product,
    is_valid_page
)

from src.retrieval.search import (
    search_web
)

from src.retrieval.rankers.source_ranker import (
    rank_sources
)

from src.retrieval.browser import (
    fetch_with_browser
)

from src.retrieval.extractors.browser_html import (
    extract_browser_html
)

from src.retrieval.extractors.llm_extractor import (
    extract_product_data
)



# -------------------------
# Streamlit UI
# -------------------------

st.set_page_config(
    page_title="UniLog AI",
    layout="wide"
)


st.title(
    "UniLog AI"
)


st.subheader(
    "AI Powered Product Catalog Enrichment System"
)


st.write(
    """
Upload a product CSV containing minimal catalog information.

UniLog AI will:
- Discover product sources
- Select relevant webpages
- Extract product information
- Generate enriched catalog data
"""
)


uploaded_file = st.file_uploader(
    "Upload Product CSV",
    type=["csv"]
)



def process_product(row):

    product = build_product(
        row
    )


    st.write(
        f"Searching source for: {product.mpn}"
    )


    sources = search_web(
        product
    )


    source = rank_sources(
        product,
        sources
    )


    st.write(
        "Selected source:"
    )

    st.write(
        source.url
    )


    page = fetch_with_browser(
        source
    )


    data = extract_browser_html(
        page
    )


    if not is_valid_page(
        data["text"]
    ):

        raise Exception(
            "Invalid webpage content"
        )


    extracted = extract_product_data(
        product.mpn,
        data["text"]
    )


    return extracted



if uploaded_file:

    df = pd.read_csv(
        uploaded_file
    )


    st.write(
        "Input Data"
    )


    st.dataframe(
        df
    )


    if st.button(
        "Generate Catalog"
    ):

        results = []


        progress = st.progress(
            0
        )


        total = len(df)


        for index, row in df.iterrows():

            try:

                result = process_product(
                    row.to_dict()
                )


                results.append(
                    result
                )


            except Exception as e:

                st.error(
                    f"Failed: {row.get('Mfg_Part_Num')} - {e}"
                )


            progress.progress(
                (index + 1) / total
            )


        if results:

            output_df = pd.DataFrame(
                results
            )


            st.success(
                "Catalog generation completed"
            )


            st.write(
                "Generated Output"
            )


            st.dataframe(
                output_df
            )


            csv = output_df.to_csv(
                index=False
            )


            st.download_button(
                label="Download Output CSV",
                data=csv,
                file_name="unilog_output.csv",
                mime="text/csv"
            )


        else:

            st.warning(
                "No products were successfully processed"
            )
