from flask import Flask

app = Flask(__name__)
app.secret_key = '5baa61e4c9b93f3f0682250b6cf8331b7ee68fd8'

from app import routes
