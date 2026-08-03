import uuid
import time


class BrowserSession:


    def __init__(self):

        self.id = str(
            uuid.uuid4()
        )

        self.created = time.time()

        self.pages_visited = 0


    def visit(self):

        self.pages_visited += 1


    def info(self):

        return {
            "id": self.id,
            "created": self.created,
            "pages": self.pages_visited
        }


session = BrowserSession()
