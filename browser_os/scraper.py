from bs4 import BeautifulSoup
from browser_os.browser import browser


def get_title():

    html = browser.get_html()

    if not html:
        return "No page opened"


    soup = BeautifulSoup(
        html,
        "html.parser"
    )


    if soup.title:
        return soup.title.text


    return "No title"


def get_text(limit=5000):

    html = browser.get_html()

    if not html:
        return "No page opened"


    soup = BeautifulSoup(
        html,
        "html.parser"
    )


    for tag in soup(
        ["script", "style"]
    ):
        tag.decompose()


    text = soup.get_text(
        separator="\n"
    )

    return text[:limit]
