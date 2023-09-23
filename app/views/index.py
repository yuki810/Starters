from flask import Blueprint, render_template, request
from app.code.code import checkMessage

view = Blueprint('index', __name__, url_prefix='/')
@view.route('/', methods=['GET'])
def show():
    return render_template('index.html', name='default')

@view.route('/check', methods=['GET'])
def checktweet():
    data = request.form.get('key')
    isOK = checkMessage(data)
    
    return isOK