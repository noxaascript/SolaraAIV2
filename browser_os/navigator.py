from browser_os.browser import browser


class Navigator:

    def __init__(self):

        self.history = []
        self.position = -1


    def open(self, url):

        result = browser.open(url)

        if result["status"] == "success":

            self.history.append(url)
            self.position += 1

        return result


    def back(self):

        if self.position <= 0:
            return "No previous page"

        self.position -= 1

        return browser.open(
            self.history[self.position]
        )


    def current(self):

        return browser.get_url()


navigator = Navigator()
