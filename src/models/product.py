from dataclasses import dataclass
from typing import Optional


@dataclass
class Product:
    mpn: str
    description: str

    e1_brand: Optional[str]
    unilog_brand: Optional[str]
    dib_brand: Optional[str]

    manufacturer: Optional[str]
