from src.models.product import Product
from src.input.normalizer import normalize_value


def parse_row(row: dict) -> Product:
    return Product(
        mpn=normalize_value(row["Mfg_Part_Num"]),
        description=normalize_value(row["Part_Desc"]),
        e1_brand=normalize_value(row["E1_Brand"]),
        unilog_brand=normalize_value(row["Unilog_Brand"]),
        dib_brand=normalize_value(row["DIB_Brand"]),
        manufacturer=normalize_value(row["Part_Manuf"]),
    )
