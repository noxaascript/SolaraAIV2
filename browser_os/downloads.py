import os
import requests


DOWNLOAD_FOLDER = "downloads"


def setup():

    os.makedirs(
        DOWNLOAD_FOLDER,
        exist_ok=True
    )


def download(url, filename):

    try:

        setup()

        path = (
            f"{DOWNLOAD_FOLDER}/{filename}"
        )

        response = requests.get(
            url,
            timeout=20
        )


        with open(
            path,
            "wb"
        ) as file:

            file.write(response.content)


        return {
            "status": "done",
            "file": path
        }


    except Exception as e:

        return {
            "status": "error",
            "message": str(e)
        }
