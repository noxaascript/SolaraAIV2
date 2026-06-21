from browser_os.navigator import navigator
from browser_os.scraper import (
    get_text,
    get_title
)


class BrowserAgent:


    def visit(self, url):

        result = navigator.open(url)

        if result["status"] != "success":
            return result


        return {
            "page": get_title(),
            "content": get_text(2000)
        }


    def summarize(self, url):

        data = self.visit(url)

        return f"""
BrowserOS Report

Title:
{data['page']}

Content:

{data['content']}
"""


agent = BrowserAgent()
