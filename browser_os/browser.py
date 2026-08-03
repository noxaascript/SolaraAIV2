import requests
from browser_os.memory import add_history


class Browser:

    def __init__(self):
        self.session = requests.Session()
        self.current_url = None
        self.current_html = None


    def open(self, url):

        try:
            headers = {
                "User-Agent": "SolaraAI BrowserOS V1"
            }

            response = self.session.get(
                url,
                headers=headers,
                timeout=10
            )

            self.current_url = url
            self.current_html = response.text

            add_history(
                url,
                "open"
            )

            return {
                "status": "success",
                "url": url,
                "code": response.status_code
            }

        except Exception as e:

            return {
                "status": "error",
                "message": str(e)
            }


    def get_html(self):

        return self.current_html


    def get_url(self):

        return self.current_url


    def close(self):

        self.session.close()

        return "Browser closed"


browser = Browser()
