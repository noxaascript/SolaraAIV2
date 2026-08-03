import requests
from bs4 import BeautifulSoup


def search(query):

    url = (
        "https://duckduckgo.com/html/?q="
        + query
    )

    try:

        html = requests.get(
            url,
            timeout=10
        ).text


        soup = BeautifulSoup(
            html,
            "html.parser"
        )


        results = []


        for link in soup.find_all(
            "a",
            limit=5
        ):

            text = link.text.strip()

            href = link.get("href")


            if text:
                results.append({
                    "title": text,
                    "url": href
                })


        return results


    except Exception as e:

        return [
            {
                "error": str(e)
            }
        ]
