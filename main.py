from flask import Flask, abort
from api.api_reporter import api_reporter

app = Flask(__name__)
app.register_blueprint(api_reporter)


@app.route('/', methods=['GET'])
def home():
    abort(404)


if __name__ == '__main__':
    app.run()
