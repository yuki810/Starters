from flask import Flask
from app.views import index
app = Flask(__name__)
app.register_blueprint(index.view)

if __name__ == '__main__':
  app.run()