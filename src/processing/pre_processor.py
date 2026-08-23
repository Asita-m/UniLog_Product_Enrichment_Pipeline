def preprocess_product(row: dict) -> dict:
    """
    Clean and normalize input catalog row
    before passing it to extraction pipeline.

    This function only performs formatting cleanup.
    Catalog values are preserved exactly.
    """

    product = row.copy()


    # Normalize whitespace only
    for key, value in product.items():

        if isinstance(value, str):
            product[key] = value.strip()


    return product
