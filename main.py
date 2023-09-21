from flask import Flask

app = Flask(__app__)




@app.route('api/v1/<user>')
def post():
    pass

app.run()