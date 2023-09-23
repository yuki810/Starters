from flask import Blueprint, render_template, request
# from app.code.code import checkMessage
# from code.code import 
import openai
openai.api_key = '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'
  

def checkMessage(text):
  openai.api_key = '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'
  response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
          {"role": "system", "content": "以下のコメントに対し不適切であるかどうか、TRUE or FALSEで答えて"},
          {"role": "user", "content": text},
      ],
    temperature=0.1
  )

  a = response.choices[0].message['content'].strip()
  return a

view = Blueprint('index', __name__, url_prefix='/')
@view.route('/', methods=['GET'])
def show():
    return render_template('index.html', name='default', isCompleted=True, postText="Hello")

@view.route('/check', methods=['POST'])
def checktweet():
    print("a")
    # data = request.form.get('key')
    # isOK = checkMessage(data)
    isOK = "a"
    return isOK