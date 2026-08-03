class TabManager:

    def __init__(self):
        self.tabs = {}
        self.current = None
        self.counter = 0


    def new_tab(self, url=None):

        self.counter += 1

        tab_id = self.counter

        self.tabs[tab_id] = {
            "url": url,
            "title": "New Tab"
        }

        self.current = tab_id

        return tab_id


    def switch(self, tab_id):

        if tab_id not in self.tabs:
            return "Tab not found"

        self.current = tab_id

        return f"Switched to tab {tab_id}"


    def close(self, tab_id):

        if tab_id not in self.tabs:
            return "Tab not found"

        del self.tabs[tab_id]

        if self.current == tab_id:
            self.current = None

        return "Tab closed"


    def list_tabs(self):

        return self.tabs


tabs = TabManager()
