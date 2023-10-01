from flask import Blueprint, render_template, request, session, redirect, url_for, g
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

# polly = boto3.client("polly")
# リージョンを指定してセッションを作成
boto_session = boto3.Session(region_name='us-east-1')
# クライアントを作成
polly1 = boto_session.client('polly')

def craeteIkemen(text):
   
  response = openai.Image.create(
      prompt="good-looking man, left front facing, black background, roland, smile",
      n=1,
      size="512x512",
      response_format="b64_json",
  )
  print(response)

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

@view.before_request
def disable_session():
    g.disable_session = True

#Start画面　セッションを無効に
@view.route('/', methods=['GET'])
def start():
  session.clear()
  return redirect("/post")


@view.route('/post', methods=['GET'])
def show():
    variable_value = session.get('isCompleted', False)
    postText = session.get('postText', "")
    mode = session.get('select_mode', 'select')
    return render_template('index.html', name='default', postText=postText, isCompleted=variable_value)

#モードの選択
@view.route('/select_mode', methods=['POST'])
def select_type():
  type = request.form['pref']
  print(type)
  session["select_type"] = type
  return redirect("/post")
    
# コメントされた内容に応じて処理を変更する
@view.route('/check', methods=['POST'])
def checktweet():
    text = request.form['text_area']
    # コメントされた内容が不適切か確認
    isOK = openai.Moderation.create(input=text)["results"][0]["flagged"]
    print(f' 投稿内容：{text}')
    print(f'不適切か？：{isOK}')
    variable_value = session.get('isCompleted', False)
    postText = session.get('postText', "")
    session["saved_text"] = text

    # 不適切な場合
    if isOK:
      #美男・美女モードか確認
      mode = session.get("select_type", "select")
      # 画像生成
      if mode == "select":
        number = random.randrange(3)+1
        link = f"static/person/ikemen{number}.jpg"
      elif mode == "auto":
        craeteIkemen(text)
        link = "static/ikemen.png"
      else:
        number = random.randrange(1)+1
        link = f"static/person/beautiful{number}.png"
        
      # alert文生成
      if mode=="anmika":alert = code1.study_main(text, "anmika")
      else: alert = alert = code1.study_main(text, "roland")

      # recommend文生成
      recommend = recommendMessage(text)
      session['recommend'] = recommend

      # recommend文読み上げ
      if mode == "anmika":text_to_voice(alert, "anmika")
      else: text_to_voice(alert, "roland")

      return render_template('alert.html', alert = alert, postText=postText, isCompleted=variable_value, inputText = text, recommend = recommend, link=link, select_mode = mode)
    # 健全な内容の時、そのままPOSTする
    else:
       session['isCompleted'] = True
       session["postText"] = text
       session["saved_text"] = ""
       return redirect("/post")
  
@view.route('/agree', methods=['POST'])
def agree():
    session['isCompleted'] = True
    session["postText"] = session.get('recommend', "")
    session["saved_text"] = ""
    return redirect("/post")
    
   
@view.route('/disagree', methods=['POST'])
def disagree():
    session['isCompleted'] = False
    session["saved_text"] = session.get('saved_text', "")
    return redirect("/post")


def text_to_voice(text, model_name):
    mp3_path = "app/static/sound/speech.mp3"
    voice = {
       "roland":"Takumi",
       "anmika":"Tomoko"
    }
    response = polly1.synthesize_speech(
        Engine='neural',
        Text = text,
        OutputFormat = "mp3",
        VoiceId = voice[model_name]
    )

    audio_stream = response.get("AudioStream")
    if audio_stream :
        with closing(audio_stream) as stream:
            with open(mp3_path, "wb") as file:
                file.write(stream.read())
    # playsound.playsound(mp3_path)