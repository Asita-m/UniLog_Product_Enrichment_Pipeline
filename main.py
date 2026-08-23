import csv

from src.models.product import Product

from src.processing.pre_processor import (
    preprocess_product
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

from src.output.csv_writer import (
    write_csv
)



def load_products(filename: str) -> list[dict]:

    products = []

    with open(
        filename,
        "r",
        encoding="utf-8"
    ) as file:

        reader = csv.DictReader(file)


        print(
            "Columns found:"
        )

        print(
            reader.fieldnames
        )


        for row in reader:
            products.append(row)


    return products



def build_product(row: dict) -> Product:

    row = preprocess_product(
        row
    )


    return Product(

        mpn=row.get(
            "Mfg_Part_Num"
        ),

        description=row.get(
            "Part_Desc"
        ),

        e1_brand=row.get(
            "E1_Brand"
        ),

        unilog_brand=row.get(
            "Unilog_Brand"
        ),

        dib_brand=row.get(
            "DIB_Brand"
        ),

        manufacturer=row.get(
            "Part_Manuf"
        ),
    )



def is_valid_page(text: str) -> bool:

    if not text:
        return False


    blocked_terms = [
        "access denied",
        "forbidden",
        "you don't have permission",
        "reference #"
    ]


    lower_text = text.lower()


    for term in blocked_terms:

        if term in lower_text:
            return False


    if len(text.strip()) < 500:
        return False


    return True



def main():

    filename = input(
        "Enter input CSV filename: "
    ).strip()


    rows = load_products(
        filename
    )


    print(
        "Total products:",
        len(rows)
    )


    results = []


    for row in rows:

        try:

            product = build_product(
                row
            )


            print(
                "\nSearching product..."
            )


            sources = search_web(
                product
            )


            if not sources:

                raise Exception(
                    "No sources found"
                )


            print(
                "\nRanking sources..."
            )


            source = rank_sources(
                product,
                sources
            )


            print(
                "Selected source:",
                source.url
            )


            print(
                "Fetching webpage..."
            )


            page = fetch_with_browser(
                source
            )


            print(
                "Browser fetch completed"
            )


            print(
                "Extracting HTML..."
            )


            data = extract_browser_html(
                page
            )


            print(
                "\nPAGE TITLE:"
            )

            print(
                data["title"]
            )


            print(
                "\nTEXT LENGTH:"
            )

            print(
                data["text_length"]
            )


            print(
                "\nTEXT PREVIEW:"
            )

            print(
                data["text"][:2000]
            )


            if not is_valid_page(
                data["text"]
            ):

                raise Exception(
                    "Invalid or blocked page content"
                )


            print(
                "\nExtracting product data..."
            )


            extracted = extract_product_data(
                product.mpn,
                data["text"]
            )


            results.append(
                extracted
            )


        except Exception as e:

            print(
                "FAILED:",
                row.get("Mfg_Part_Num"),
                e
            )


    print(
        "\nWriting output..."
    )


    write_csv(
        results,
        "Data/output.csv"
    )


    print(
        "Completed:",
        len(results),
        "products"
    )



if __name__ == "__main__":
    main()
