print("")
print("#######################################")
print("")
print("             _______ ____  __  __      ")
print("          /\|__   __/ __ \|  \/  |     ")
print("         /  \  | | | |  | | \  / |     ")
print("        / /\ \ | | | |  | | |\/| |     ")
print("       / ____ \| | | |__| | |  | |     ")
print("      /_/    \_\_|  \____/|_|  |_|     ")
print("")
print("#######################################")
print("")




from vision.computer_vision import ComputerVision
from listener.voice_listener import VoiceListener

cv = ComputerVision()
cv.start_recording()

vl = VoiceListener()
vl.record()