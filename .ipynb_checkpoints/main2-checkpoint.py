import speech_recognition as sr
import numpy as np
import matplotlib.pyplot as plt
import cv2
from easygui import *
import os
from PIL import Image, ImageTk
from itertools import count
import tkinter as tk
import string


def display_sign_language(text, sign_type="ISL"):
    """Displays corresponding sign language images or GIFs based on input text."""
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
               'where is the bathroom', 'where is the police station', 'you are wrong']
    
    arr = list(string.ascii_lowercase)
    text = text.lower()
    
    for c in string.punctuation:
        text = text.replace(c, "")
    
    if text in isl_gif:
        class ImageLabel(tk.Label):
            def load(self, im):
                if isinstance(im, str):
                    im = Image.open(im)
                self.loc = 0
                self.frames = []
                try:
                    for i in count(1):
                        self.frames.append(ImageTk.PhotoImage(im.copy()))
                        im.seek(i)
                except EOFError:
                    pass
                self.delay = im.info.get('duration', 100)
                if len(self.frames) == 1:
                    self.config(image=self.frames[0])
                else:
                    self.next_frame()
            
            def next_frame(self):
                if self.frames:
                    self.loc = (self.loc + 1) % len(self.frames)
                    self.config(image=self.frames[self.loc])
                    self.after(self.delay, self.next_frame)
        
        root = tk.Tk()
        lbl = ImageLabel(root)
        lbl.pack()
        lbl.load(f'ISL_Gifs/{text}.gif')
        root.mainloop()
    else:
        for char in text:
            if char in arr:
                folder = 'letters' if sign_type == "ISL" else 'Aletters'
                ext = 'jpg' if sign_type == "ISL" else 'jpeg'
                image_address = f'{folder}/{char}.{ext}'
                image_itself = Image.open(image_address)
                image_numpy_format = np.asarray(image_itself)
                plt.imshow(image_numpy_format)
                plt.draw()
                plt.pause(0.8)
        plt.close()

def speech_to_sign_language(sign_type="ISL"):
    """Handles Speech-to-Sign Language Conversion."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        while True:
            print("I am Listening")
            audio = r.listen(source)
            try:
                text = r.recognize_google(audio)
                print('You Said: ' + text)
                if text.lower() in ('goodbye', 'good bye', 'bye'):
                    print("Oops! Time to say goodbye.")
                    break
                display_sign_language(text, sign_type)
            except Exception as e:
                print("Error recognizing speech: ", e)
            plt.close()

def text_to_sign_language(sign_type="ISL"):
    """Handles Text-to-Sign Language Conversion."""
    text = final_pred.predict()
    if text:
        display_sign_language(text, sign_type)

while True:
    image = "signlang.png"
    msg = "HEARING IMPAIRMENT ASSISTANT"
    choices = ["Speech to ISL", "Speech to ASL", "Text to ISL", "Text to ASL", "All Done!"]
    reply = buttonbox(msg, image=image, choices=choices)
    
    if reply == "Speech to ISL":
        speech_to_sign_language("ISL")
    elif reply == "Speech to ASL":
        speech_to_sign_language("ASL")
    elif reply == "Text to ISL":
        text_to_sign_language("ISL")
    elif reply == "Text to ASL":
        text_to_sign_language("ASL")
    elif reply == "All Done!":
        break
