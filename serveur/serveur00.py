


from  flask import Flask, jsonify, request

from flask_cors import CORS
app = Flask(import_name=__name__)
CORS(app)


if __name__ == "__main__" : 
    app.run(debug=True)
