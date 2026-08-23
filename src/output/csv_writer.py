import csv

from src.models.output_schema import OUTPUT_FIELDS


def write_csv(
    products: list[dict],
    filename: str = "output.csv"
):
    """
    Writes extracted product data
    into the required delivery format.

    Accepts multiple products and
    creates a compiled CSV.
    """


    with open(
        filename,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:


        writer = csv.DictWriter(
            file,
            fieldnames=OUTPUT_FIELDS
        )


        # Header
        writer.writeheader()


        # Rows
        for product_data in products:

            row = {}

            for field in OUTPUT_FIELDS:

                row[field] = product_data.get(
                    field,
                    None
                )


            writer.writerow(row)


    return filename
