from urllib.parse import urlparse

from ddgs import DDGS

from src.models.product import Product
from src.models.source import Source
from src.retrieval.discovery import build_search_queries


def search_web(
    product: Product,
    max_results: int = 5
) -> list[Source]:

    queries = build_search_queries(product)

    print("\nSEARCH QUERIES:")
    for q in queries:
        print(q)


    sources = []


    for query in queries:

        print(
            "\nRunning query:",
            query
        )


        try:

            # Fresh search session per query
            with DDGS() as ddgs:

                results = ddgs.text(
                    query,
                    max_results=max_results
                )


            print(
                "Results:",
                len(results)
            )


        except Exception as e:

            print(
                "Query failed:",
                e
            )

            continue



        for result in results:

            url = result.get(
                "href"
            )


            if not url:
                continue


            sources.append(
                Source(
                    url=url,
                    source_type="web_search",
                    title=result.get("title"),
                    domain=urlparse(url).netloc
                )
            )


    if not sources:

        raise Exception(
            "No results found."
        )


    return sources
