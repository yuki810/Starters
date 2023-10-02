from flask import Flask
# from app.views import index
from views import index

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'null'
app.config['SESSION_PERMANENT'] = False
app.register_blueprint(index.view)

app.secret_key = 'your_secret_key_here'

if __name__ == '__main__':
  app.run()