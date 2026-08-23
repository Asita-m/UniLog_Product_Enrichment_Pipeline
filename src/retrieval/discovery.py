from src.models.product import Product


def valid_value(value):

    if not value:
        return False

    invalid_values = [
        "-- Unbranded --",
        "-- No Unilog Brand --",
        "-- No DIB Brand --",
    ]

    return value not in invalid_values



def build_search_queries(
    product: Product
) -> list[str]:

    queries = []


    if product.mpn:

        # Primary search
        queries.append(
            product.mpn
        )

        # Broader product search
        queries.append(
            f"{product.mpn} product"
        )


    if (
        product.mpn
        and valid_value(product.description)
    ):

        queries.append(
            f"{product.mpn} {product.description}"
        )


    if (
        product.mpn
        and valid_value(product.manufacturer)
    ):

        queries.append(
            f"{product.mpn} {product.manufacturer}"
        )


    return queries
