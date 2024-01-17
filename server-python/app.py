from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
app.config.from_pyfile('config.py')
CORS(app, supports_credentials=True, 
     origins="http://localhost:3000", 
     methods=["GET", "POST", "PUT", "DELETE"])


from view import *
from view_logs import *
from view_movimentacoes import *


if __name__ == "__main__":
    app.run(debug=True)