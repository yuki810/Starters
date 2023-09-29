from flask import Blueprint, render_template, request, session, redirect, url_for
from codes import code1
import base64
import time
# from app.code.code import checkMessage
# from code.code import 
import random
import json

# CHatGPT用
import openai

openai.api_key = ''
isCompleted = False
with open("app/static/apikey.txt") as f:
   openai.api_key = f.read()

# 音声生成用
import boto3
import playsound
import speech_recognition as sr
import openai
from contextlib import closing

r = sr.Recognizer()
polly = boto3.client("polly")

def craeteIkemen(text):
   
  response = openai.Image.create(
      prompt="good-looking man, left front facing, black background, roland, smile",
      n=1,
      size="512x512",
      response_format="b64_json",
  )

  img_data = base64.b64decode(response["data"][0]["b64_json"])
  with open(f"app/static/ikemen.png", "wb") as f:
      f.write(img_data)
  


def checkMessage(text):
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

def recommendMessage(text):
  response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
          {"role": "system", "content": "以下のコメントを、女の子らしく誰も傷つけない言い方に変えて"},
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

@view.route('/?pref=<type>', methods=['PUT'])
def select_type(type):
  print(type)
  session["select_type"] = type
    

@view.route('/check', methods=['POST'])
def checktweet():
    text = request.form['text_area']
    print(request.form)
    # response = json.loads(openai.Moderation.create(input=text))
    isOK = openai.Moderation.create(input=text)["results"][0]["flagged"]
    #isOK = checkMessage(text)
    # isOK = "TRUE"
    print(text)
    print(isOK)
    variable_value = session.get('isCompleted', False)
    postText = session.get('postText', "")
    session["saved_text"] = text

    if isOK:

      # 画像生成
      type = session.get("select_type","select")
      if type == "select":
        number = random.randrange(3)+1
        link = f"static/person/ikemen{number}.jpg"
      else:
        craeteIkemen(text)
        link = "static/ikemen.png"

      # alert文生成
      # a = alertMessage(text)
      a = code1.study_main(text)

      # recommend文生成
      time5 = time.time()
      recommend = recommendMessage(text)
      time6 = time.time()
      print(f"おすすめ生成：{time6-time5}")
      session['recommend'] = recommend
      print(recommend)

      # recommend文読み上げ
      text_to_voice(recommend)

      return render_template('alert.html', alert = a, postText=postText, isCompleted=variable_value, inputText = text, recommend = recommend, link=link)
    else:
       isCompleted = True
       session['isCompleted'] = True
       session["postText"] = text
       session["saved_text"] = ""
       return redirect("/")
  
@view.route('/agree', methods=['POST'])
def agree():
    session['isCompleted'] = True
    session["postText"] = session.get('recommend', "")
    session["saved_text"] = ""
    return redirect("/")
    
   
@view.route('/disagree', methods=['POST'])
def disagree():
    session['isCompleted'] = False
    session["saved_text"] = session.get('saved_text', "")
    return redirect("/")


def text_to_voice(text):
    mp3_path = "app/static/sound/speech.mp3"
    response = polly.synthesize_speech(
        Engine='neural',
        Text = text,
        OutputFormat = "mp3",
        VoiceId = "Takumi"
    )

    audio_stream = response.get("AudioStream")
    if audio_stream :
        with closing(audio_stream) as stream:
            with open(mp3_path, "wb") as file:
                file.write(stream.read())
    # playsound.playsound(mp3_path)