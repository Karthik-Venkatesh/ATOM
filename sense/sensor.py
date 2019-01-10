from vision.computer_vision import ComputerVision
from listener.voice_listener import VoiceListener


class Sensor:

    vision: ComputerVision
    listener: VoiceListener

    def start_senses(self):
        self.vision = ComputerVision()
        self.vision.start_recording()

        self.listener = VoiceListener()
        self.listener.sensor = self
        self.listener.record()

    def trigger_add_face(self, label: [str]):
        if self.vision is not None:
            self.vision.add_face(label)
        else:
            print("Computer vision not available...")
