from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import abc_1
import string
import os
import speech_recognition as sr
from flask import Flask, render_template, Response, jsonify
import cv2
import mediapipe as mp
import abc_1  # Your ASL recognition module
import pyttsx3
import speech_recognition as sr
import requests
from googletrans import Translator
from flask import jsonify, request
translator = Translator()





app = Flask(__name__)
CORS(app)  # Allows frontend to communicate with backend 

    

@app.route('/asl-to-speech', methods=['GET'])
def asl_to_speech_api():
    result = abc_1.run()
    return jsonify({"output": result})




# List of predefined ISL words that have corresponding GIFs
isl_gif = ['any questions', 'are you angry', 'are you busy', 'are you hungry', 'are you sick', 'be careful',
               'can we meet tomorrow', 'did you book tickets', 'did you finish homework', 'do you go to office', 'do you have money',
               'do you want something to drink', 'do you want tea or coffee', 'do you watch TV', 'dont worry', 'flower is beautiful',
               'good afternoon', 'good evening', 'good morning', 'good night', 'good question', 'had your lunch', 'happy journey',
               'hello what is your name', 'how many people are there in your family', 'i am a clerk', 'i am bore doing nothing', 
               'i am fine', 'i am sorry', 'i am thinking', 'i am tired', 'i dont understand anything', 'i go to a theatre', 'i love to shop',
               'i had to say something but i forgot', 'i have headache', 'i like pink colour', 'i live in nagpur', 'lets go for lunch', 'my mother is a homemaker',
               'my name is john', 'nice to meet you', 'no smoking please', 'open the door', 'please call me later',
               'please clean the room', 'please give me your pen', 'please use dustbin dont throw garbage', 'please wait for sometime', 'shall I help you',
               'shall we go together tommorow', 'sign language interpreter', 'sit down', 'stand up', 'take care', 'there was traffic jam', 'wait I am thinking',
               'what are you doing', 'what is the problem', 'what is todays date', 'what is your father do', 'what is your job',
               'what is your mobile number', 'what is your name', 'whats up', 'when is your interview', 'when we will go', 'where do you stay',
               'where is the bathroom', 'where is the police station', 'you are wrong', 'address', 'agra', 'ahemdabad', 'all', 'april', 'assam', 'august', 'australia', 'badoda', 'banana', 'banaras', 'banglore',
               'bihar', 'bihar', 'bridge', 'cat', 'chandigarh', 'chennai', 'christmas', 'church', 'clinic', 'coconut', 'crocodile', 'dasara',
               'deaf', 'december', 'deer', 'delhi', 'dollar', 'duck', 'febuary', 'friday', 'fruits', 'glass', 'grapes', 'gujrat', 'hello',
               'hindu', 'hyderabad', 'india', 'january', 'jesus', 'job', 'july', 'july', 'karnataka', 'kerala', 'krishna', 'litre', 'mango',
               'may', 'mile', 'monday', 'mumbai', 'museum', 'muslim', 'nagpur', 'october', 'orange', 'pakistan', 'pass', 'police station',
               'post office', 'pune', 'punjab', 'rajasthan', 'ram', 'restaurant', 'saturday', 'september', 'shop', 'sleep', 'southafrica',
               'story', 'sunday', 'tamil nadu', 'temperature', 'temple', 'thursday', 'toilet', 'tomato', 'town', 'tuesday', 'usa', 'village',
               'voice', 'wednesday', 'weight', 'please wait for sometime', 'what is your mobile number', 'what are you doing', 'are you busy']  # Keeping your predefined list intact
    

def indian_sign_language(text):
    text = text.lower()
    for c in string.punctuation:
        text = text.replace(c, "")

    image_paths = []

    # Check if the entire phrase has a GIF
    gif_path = f"static/ISL_Gifs/{text}.gif"
    if os.path.exists(gif_path):
        image_paths.append(gif_path)  # ✅ Add GIF if it exists
    
    else:
        words = text.split()
        for word in words:
            word_images = [] 
            for char in word:
                if char.isalpha():  # Ensure it's a valid letter
                    char_path = f"static/letters/{char}.jpg"
                    if os.path.exists(char_path):
                        word_images.append(char_path)

            if word_images:
                image_paths.append(word_images)  # Add the word's images to the main list
            else:
                # If no images found for the word, add a placeholder or empty list (optional)
                image_paths.append([])

    return image_paths


# Text to ISL Route (Handles GIFs + Letter Images)
@app.route('/text-to-isl', methods=['POST', 'GET'])
def text_to_isl_api():
    if request.method == 'POST':
        data = request.json
        text = data.get("text", "")
        sign_images = indian_sign_language(text)

        if sign_images:
            return jsonify({"status": "success", "images": sign_images})
        else:
            return jsonify({"status": "error", "message": "No matching signs found!"})
    else:
        return render_template("text_to_isl.html")

import os
import string

def american_sign_language(text):
    text = text.lower()
    for c in string.punctuation:
        text = text.replace(c, "")  # Remove punctuation

    words = text.split()  # Split text into words
    image_paths = []  # List to store image paths

    for word in words:
        word_images = []  # List to store images for each word
        # Add individual letter images for the word
        for char in word:
            if char.isalpha():  # Ensure it's a valid letter
                char_path = f"static/Aletters/{char}.jpeg"
                if os.path.exists(char_path):
                    word_images.append(char_path)

        if word_images:
            image_paths.append(word_images)  # Add the word's images to the main list
        else:
            # If no images found for the word, add a placeholder or empty list (optional)
            image_paths.append([])

    return image_paths

#text to asl 
@app.route('/text-to-asl', methods=['POST', 'GET'])
def text_to_asl_api():
    if request.method == 'POST':
        data = request.json
        text = data.get("text", "")
        sign_images = american_sign_language(text)

        if sign_images:
            return jsonify({"status": "success", "images": sign_images})
        else:
            return jsonify({"status": "error", "message": "No matching signs found!"})
    else:
        return render_template("text_to_asl.html")

# Serve the index.html file
@app.route("/")
def home():
    return render_template("index.html")

# Speech to ASL
@app.route('/speech-to-asl', methods=['POST', 'GET'])
def speech_to_asl_api():
    if request.method == 'POST':
        try:
            data = request.get_json()  # ✅ Ensure `data` is always assigned
            if not data or "text" not in data:
                return jsonify({"status": "error", "message": "Invalid request data"}), 400
            
            text = data["text"]
            url = "https://text-translator2.p.rapidapi.com/translate"
            headers = {
                "content-type": "application/x-www-form-urlencoded",
                "X-RapidAPI-Key": "0f491a5108mshbe7b62a9976bafbp15461ejsn7894515d0926",
                "X-RapidAPI-Host": "text-translator2.p.rapidapi.com",
            }
            payload = {
                "source_language": "auto",
                "target_language": "en",
                "text": text,
            }
            response = requests.post(url, data=payload, headers=headers)
            translation = response.json()
            text = translation["data"]["translatedText"]
            
            print("Translated text =", text)
            text = text.lower()

            # Call function to convert text to ISL images (ensure this function exists)
            sign_images = american_sign_language(text)
            
            return jsonify({"status": "success", "text": text, "images": sign_images})
        except sr.UnknownValueError:
            return jsonify({"status": "error", "message": "Speech not recognized"})
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)})
    else:
        return render_template("speech_to_asl.html")


# Speech to ISL

# Load API Key from environment variables
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")

@app.route('/speech-to-isl', methods=['POST', 'GET'])
def speech_to_isl_api():
    if request.method == 'POST':
        try:
            data = request.get_json()  # ✅ Ensure `data` is always assigned
            if not data or "text" not in data:
                return jsonify({"status": "error", "message": "Invalid request data"}), 400
            
            text = data["text"]
            url = "https://text-translator2.p.rapidapi.com/translate"
            headers = {
                "content-type": "application/x-www-form-urlencoded",
                "X-RapidAPI-Key": "0f491a5108mshbe7b62a9976bafbp15461ejsn7894515d0926",
                "X-RapidAPI-Host": "text-translator2.p.rapidapi.com",
            }
            payload = {
                "source_language": "auto",
                "target_language": "en",
                "text": text,
            }
            response = requests.post(url, data=payload, headers=headers)
            translation = response.json()
            text = translation["data"]["translatedText"]
            
            print("Translated text =", text)
            text = text.lower()

            # Call function to convert text to ISL images (ensure this function exists)
            sign_images = indian_sign_language(text)
            
            return jsonify({"status": "success", "text": text, "images": sign_images})
        except sr.UnknownValueError:
            return jsonify({"status": "error", "message": "Speech not recognized"})
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)})
    else:
        return render_template("speech_to_isl.html")

@app.route("/translate-to-english", methods=["POST"])
def translate_to_english():
    try:
        data = request.get_json()  # ✅ Ensure `data` is always assigned
        if not data or "text" not in data or "sourceLang" not in data:
            return jsonify({"status": "error", "message": "Invalid request data"}), 400

        text = data["text"]
        source_lang = data["sourceLang"]

        from googletrans import Translator
        translator = Translator()
        translated_text = translator.translate(text, src=source_lang, dest="en").text
        
        return jsonify({"status": "success", "translatedText": translated_text})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})



# ASL to ISL

@app.route('/asl-to-isl', methods=['POST','GET'])
def asl_to_isl_api():
    result = abc_1.run()
    return jsonify({"output": result})

@app.route('/display_signs')
def display_signs():
    text = request.args.get('text', '')
    images = indian_sign_language(text)  # or however you process the input
    return render_template('output.html', images=images, text=text)


if __name__ == '__main__':
    app.run(debug=True)


