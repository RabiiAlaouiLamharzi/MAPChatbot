import os
from main import docsearch
from main import chain
from firebase import firebase
from flask import Flask, jsonify, request
from flask_cors import CORS
import subprocess
import requests

app = Flask(__name__)
CORS(app)

firebase = firebase.FirebaseApplication('https://chatbotmap-7cabf-default-rtdb.firebaseio.com/', None)

@app.route('/run')
def get__response():
    DontKnow = "Je suis désolé, mais je ne suis pas en mesure de vous fournir une réponse à votre question à partir des données sur lesquelles j'ai été entraîné."
    query1 = firebase.get('https://chatbotmap-7cabf-default-rtdb.firebaseio.com/interaction/0/question','')
    if query1:
        # Perform similarity search and generate response
        docs = docsearch.similarity_search(query1)
        response = chain.run(input_documents=docs, question=query1)

        if response == " I don't know.":
            firebase.put('https://chatbotmap-7cabf-default-rtdb.firebaseio.com/interaction/0/','answer', DontKnow)
            return(DontKnow)
        else:
            firebase.put('https://chatbotmap-7cabf-default-rtdb.firebaseio.com/interaction/0/','answer', response)
            return(response)

if __name__ == '__main__':
    app.run()