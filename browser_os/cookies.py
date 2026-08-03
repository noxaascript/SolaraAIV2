class CookieManager:

    def __init__(self):
        self.cookies = {}


    def save(self, domain, cookie):

        self.cookies[domain] = cookie

        return "Cookie saved"


    def get(self, domain):

        return self.cookies.get(domain)


    def clear(self):

        self.cookies = {}

        return "Cookies cleared"


cookies = CookieManager()
