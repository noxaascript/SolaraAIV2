import requests
from bs4 import BeautifulSoup


def fetch_url(url):
    try:
        headers = {
            "User-Agent": "SolaraAI-Browser/1.0"
        }

        res = requests.get(url, headers=headers, timeout=10)

        soup = BeautifulSoup(res.text, "html.parser")

        # remove scripts/styles biar bersih
        for tag in soup(["script", "style", "noscript"]):
            tag.decompose()

        text = soup.get_text(separator="\n")

        clean = "\n".join(
            line.strip() for line in text.splitlines() if line.strip()
        )

        return clean[:3000]

    except Exception as e:
        return f"Browser error: {str(e)}"
