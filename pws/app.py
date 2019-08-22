import os
import uuid
from flask import Flask

app = Flask(__name__)
my_uuid = str(uuid.uuid1())

@app.route('/')
def mainmenu():

    response = """
    <html>
        <head>
        </head>
    <body>
     <h1><u>RPi Tackman - Top Page</u></h1>
     <br>
     Hi, I'm GUID: {}<br>
    </body>
    </html>
    """.format(my_uuid)

    return response


if __name__ == "__main__":
	app.run(debug=False,host='0.0.0.0', port=int(os.getenv('PORT', '5000')))

