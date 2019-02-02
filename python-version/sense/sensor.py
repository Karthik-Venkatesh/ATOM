#
#  sensor.py
#  ATOM
#
#  Created by Karthik V.
#  Updated copyright on 16/1/19 5:55 PM.
#
#  Copyright © 2019 Karthik Venkatesh. All rights reserved.
#

from vision.computer_vision import ComputerVision
from listener.voice_listener import VoiceListener


class Sensor:

    vision: ComputerVision
    listener: VoiceListener

    def start_senses(self):
        self.listener = VoiceListener()
        self.listener.sensor = self
        self.listener.listen()

        self.vision = ComputerVision()
        self.vision.start_recording()

    def trigger_add_face(self, label: [str]):
        if self.vision is not None:
            self.vision.add_face(label)
        else:
            print("Computer vision not available...")
