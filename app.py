from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
# from openai import OpenAI
# from opik.integrations.openai import track_openai
from dotenv import load_dotenv
import os
import time
from mistralai import Mistral





load_dotenv()
app = Flask(__name__)
CORS(app)



@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json["message"]
    
    
    # openai_client = track_openai(OpenAI(api_key=os.environ['OPENAI_API_KEY'],base_url = "https://openrouter.ai/api/v1",
    # ))
    
    # response = openai_client.chat.completions.create(
    #     model="mistralai/mistral-7b-instruct",
    #     messages=[{"role": "user", "content": user_message}],
    # )
    client = Mistral(api_key=os.environ["MISTRAL_API_KEY"])

    response = client.chat.complete(
        model="ft:open-mistral-7b:38fbd7ba:20250504:d519d181",  
        messages=[
            {"role": "user", "content": user_message}
        ]
    )
    reply = response.choices[0].message.content
    return jsonify({"reply": reply})
   

if __name__ == '__main__':
    app.run(port=5000)
