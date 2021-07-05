from flask import Flask

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return '''
    <html>
    <body>
    <h1>Hello World</h1>
    </body>
    </html>
    '''

if __name__ == '__main__':
    # setting debug=True ensures that saving changes get loaded into the already running service, instead of having to restart it
    app.run(port=7000, debug=True)