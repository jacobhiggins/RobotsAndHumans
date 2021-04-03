from naoqi import ALProxy

IP = "192.168.86.55"
tts = ALProxy("ALTextToSpeech", IP, 9559)

# Example: Sends a string to the text-to-speech module
tts.say("Python")