#
#  voice_listener.py
#  ATOM
#
#  Created by Karthik V.
#  Updated copyright on 16/1/19 5:54 PM.
#
#  Copyright © 2018 Karthik Venkatesh. All rights reserved.
#

import speech_recognition as sr
from utills import reachability
from nlp.name_extractor import NameExtractor


class VoiceListener:

    recognizer = sr.Recognizer()
    micro_phone = sr.Microphone()
    sensor = None
    stopper = None

    def __init__(self):
        print("Voice Listener Instantiated...")

    def listen(self):
        with self.micro_phone as source:
            # we only need to calibrate once, before we start listening
            self.recognizer.adjust_for_ambient_noise(source)

        # start listening in the background (note that we don't have to do this inside a `with` statement)
        self.stopper = self.recognizer.listen_in_background(self.micro_phone, self.listener_callback)

    def add_face(self, labels: [str]):
        if len(labels) > 0:
            if self.sensor is not None:
                self.sensor.trigger_add_face(labels[0])

    # this is called from the background thread
    def listener_callback(self, recognizer, audio):
        try:
            # Getting transcription from google when internet is available.
            # Otherwise getting transcription from CMUSphinx.
            # NOTE: CMUSphinx not giving correct text while i am speaking
            if reachability.is_connected():
                voice_text = recognizer.recognize_google(audio)
            else:
                voice_text = recognizer.recognize_sphinx(audio)
            print("Transcription: " + voice_text)
            if "i am" in voice_text.lower():
                names: [str] = NameExtractor.extract_names(voice_text)
                print("Names: ", names)
                self.add_face(names)
        except sr.UnknownValueError:
            print("Audio unitelligible")
        except sr.RequestError as e:
            print("Cannot obtain results: {0}".format(e))
