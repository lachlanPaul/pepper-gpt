"""
    This is the main file where Pepper will communicate with a server.

    First, Pepper will send an audio file it's recorded of someone speaking. The server will then return that audio
    after it has been turned to text, and given to an AI model instructed to be Pepper.
    Pepper will then say the response, and the cycle will repeat, until the AI believes the conversation has ended.

    Each AI response will be tied to an emotion and depending on this emotion, Pepper will randomly select from a list,
    an animation to perform based on this emotion.

    The hardest part of this is the way Pepper determines when someone has finished talking.
    To do this, Pepper will keep recording until the volume of the audio it's picking up is below a certain level for
    around 3 - 5 seconds.

    Lachlan Paul, 2024
"""
import os
import random
import sys
import time

import naoqi
import requests
from naoqi import ALProxy, ALBroker
from dotenv import load_dotenv


class PepperGPT(naoqi.ALModule):
    def __init__(self, ip, port, param):
        self.ip = ip
        self.port = port
        self.recording_location = "home/nao/PepperGPT/temp_recording/temp.wav"
        # This should be the link to your server where the text is transcribed and then fed to GPT.
        self.transcription_gpt_server = "http://127.0.0.1:5000/upload"

        load_dotenv()
        self.SERVER_PASSCODE = os.getenv("PASSCODE")

        self.broker = ALBroker("broker", "0.0.0.0", 0, self.ip, int(self.port))
        naoqi.ALModule.__init__(self, param)

        self.memory = ALProxy("ALMemory")
        self.speech_recognition = ALProxy("ALSpeechRecognition", self.ip, self.port)
        self.audio_recorder = ALProxy("ALAudioRecorder", self.ip, self.port)

        # TODO: Fil the Big-Fat-List-Of-Animation-Names(tm) with animation names (what else?)
        # Big-Fat-List-Of-Animation-Names(tm)
        self.EMOTIONS = {
            "HAPPY": ["placeholder"],
            "SAD": ["placeholder"],
            "CONFUSED": ["placeholder"],
            "SORRY": ["placeholder"],
            "ANGRY": ["placeholder"],
            "GREETING": ["placeholder"],
            "END": ["placeholder"]
        }

    def start(self):
        # A current limitation is that Pepper only begins recording after they hear speech,
        # so it will wait for the current speech to stop, then start recording.
        # I have not yet figured out a workaround for this.
        self.speech_recognition.subscribe("Test_ASR")
        self.memory.subscribeToEvent("WordRecognized", self.getName(), "processRemote")
        print("---Started!---")

    def stop(self):
        self.speech_recognition.unsubscribe("Test_ASR")
        self.broker.shutdown()
        self.memory.unsubscribeToEvent("WordRecognized", self.getName())
        print("---Stopped!---")

    def run(self):
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("Interrupted by user, shutting down")
            self.stop()
            sys.exit(0)

    def processRemote(self, signalName, message):
        self.record_audio()
        response = self.upload_audio()
        self.say_response(response)

    def record_audio(self):
        # TODO: Make this record for as long as it can detect sound above a certain level.
        print("---Recording audio---")
        self.audio_recorder.startMicrophonesRecording(self.recording_location, "wav", 16000, (0, 0, 1, 0))
        time.sleep(10)

        print("---Finished recording audio---")
        self.audio_recorder.stopMicrophonesRecording()

    def upload_audio(self):
        # Uploads the audio file to the server url set in the init phase
        with open(self.recording_location, 'rb') as audio_file:
            files = {"audio_file": audio_file}

            # My server has a passcode, and yours should too, to avoid people leeching off of your GPT API.
            # Make sure to hide the passcode in a .env file.
            headers = {"Passcode": self.SERVER_PASSCODE}

            # Gets the text response from the server
            return requests.post(self.transcription_gpt_server, files=files, headers=headers).text

    def say_response(self, response):
        """
            Says the text, and if found, plays an animation related to an animation.
            :param response: the text to say. should have an emotion tied to the end, eg; "I am happy! | HAPPY"
        """
        try:
            emotion, response = response.split("|")

            for feeling in self.EMOTIONS.keys():
                if feeling == emotion:
                    animation_to_play = random.choice(self.EMOTIONS[feeling])

                    # TODO: Make this the correct path
                    # self.ANIMATION.run(animation_to_play)
                    self.TTS.say(response)
        except RuntimeError:
            # TODO: Place animation here. Thinking or shrugging
            self.TTS.say("Hmm, it seems I'm not connected to the internet, check my wifi connection, or let my "
                         "programmer know.")


if __name__ == "__main__":
    pepper_gpt = PepperGPT("10.174.154.14", 9559, "pepper_gpt")
    pepper_gpt.start()
    pepper_gpt.run()
