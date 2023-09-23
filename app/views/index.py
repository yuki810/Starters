from flask import Blueprint, render_template

view = Blueprint('index', __name__, url_prefix='/')
@view.route('/', methods=['GET'])
def show():
    return render_template('index.html', name='default')

@view.route('/tweet/<username>', methods=['GET'])
def checktweet(username):
    return "UserName: " + str(username)