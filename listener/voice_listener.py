
import speech_recognition as sr
from utills import reachability
from nlp.name_extractor import NameExtractor


class VoiceListener:

    recognizer = sr.Recognizer()
    sensor = None

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
                if "i am" in voice_text.lower():
                    names: [str] = NameExtractor.extract_names(voice_text)
                    print("Names: ", names)
                    self.add_face(names)
            except sr.UnknownValueError:
                print("Audio unitelligible")
            except sr.RequestError as e:
                print("Cannot obtain results: {0}".format(e))

    def add_face(self, labels: [str]):
        if len(labels) > 0:
            if self.sensor is not None:
                self.sensor.trigger_add_face(labels[0])
