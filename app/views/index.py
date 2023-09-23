from flask import Blueprint, render_template, request, session, redirect, url_for
# from app.code.code import checkMessage
# from code.code import 
import openai
openai.api_key = ''
  

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
    return render_template('index.html', name='default', isCompleted=True, postText="Hello")

@view.route('/check', methods=['POST'])
def checktweet():
    text = request.form['text_area']
    isOK = checkMessage(text)

    print(text)
    print(isOK)

    if isOK == "TRUE":
       a = alertMessage(text)
       print(a)
       return render_template('alert.html', alert = a)
    else:
       return redirect(url_for('/')) 