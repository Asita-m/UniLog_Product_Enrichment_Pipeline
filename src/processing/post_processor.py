def attach_images(
    product: dict,
    images: list
) -> dict:
    """
    Attach ranked product images
    into catalog fields.
    """

    image_fields = [
        "Product Image",
        "Alternate Image 1",
        "Alternate Image 2",
        "Alternate Image 3",
        "Alternate Image 4",
    ]

    for index, field in enumerate(image_fields):

        if index < len(images):
            product[field] = images[index]["url"]
        else:
            product[field] = None

    return product



def post_process_product(
    product: dict,
    source_url: str,
    images: list = None
) -> dict:
    """
    Final product enrichment.

    Does not modify extracted values.
    Only adds external metadata.
    """


    # Add manufacturer/source URL
    if not product.get("MFR URL"):
        product["MFR URL"] = source_url


    # Attach product images
    if images:
        product = attach_images(
            product,
            images
        )


    return product
