import openai

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