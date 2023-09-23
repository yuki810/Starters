from flask import Blueprint, render_template, request, session, redirect, url_for
# from app.code.code import checkMessage
# from code.code import 
import openai
openai.api_key = ''
isCompleted = False


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

def alertMessage(text):
  openai.api_key = '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'
  response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
          {"role": "system", "content": "以下のコメントに対し,でちゅまちゅ口調で優しく諭して"},
          {"role": "user", "content": "その時に返す言葉は30文字以内にしてほしい"},
          {"role": "user", "content": text},
      ],
    temperature=0.1
  )

  a = response.choices[0].message['content'].strip()
  return a


view = Blueprint('index', __name__, url_prefix='/')
@view.route('/', methods=['GET'])
def show():
    variable_value = session.get('isCompleted', False)
    postText = session.get('postText', "")
    return render_template('index.html', name='default', postText=postText, isCompleted=variable_value)

@view.route('/check', methods=['POST'])
def checktweet():
    print("a")
    print(request)
    text = request.form['text_area']
    print(text)
    isOK = checkMessage(text)
    print(text)
    print(isOK)
    variable_value = session.get('isCompleted', False)
    postText = session.get('postText', "")
    
    if isOK == "TRUE":
      a = alertMessage(text)
      #  a = "それで本当にいいのかな？？"
      print(a)
      return render_template('alert.html', alert = a, postText=postText, isCompleted=variable_value, inputText = text)
    else:
       isCompleted = True
       session['isCompleted'] = True
       session["postText"] = text
       return redirect("/")