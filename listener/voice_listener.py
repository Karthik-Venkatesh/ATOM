
import speech_recognition as sr
from utills import reachability
from nlp.name_extractor import NameExtractor


class VoiceListener:

    recognizer = sr.Recognizer()

    def __init__(self):
        print("Voice Listener Instantiated...")

    def record(self):
        while True:
            with sr.Microphone() as source:
                print("Speak into mic")
                audio = self.recognizer.listen(source)

            try:
                # Getting transcription from google when internet is available.
                # Otherwise getting transcription from CMUSphinx.
                # NOTE: CMUSphinx not giving correct text while i am speaking
                if reachability.is_connected():
                    voice_text = self.recognizer.recognize_google(audio)
                else:
                    voice_text = self.recognizer.recognize_google(audio)
                print("Transcription: " + voice_text)
                names: [] = NameExtractor.extract_names(voice_text)
                print("Names: ", names)
            except sr.UnknownValueError:
                print("Audio unitelligible")
            except sr.RequestError as e:
                print("Cannot obtain results: {0}".format(e))
