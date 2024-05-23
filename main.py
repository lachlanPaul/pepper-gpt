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
import random
import time

from naoqi import ALProxy
import requests


class PepperGPT:
    def __init__(self):
        self.IP = "10.174.154.11"
        self.PORT = 9559
        self.RECORDING_PATH = "home/nao/lachlan/audio_recording/recording.wav"

        # animation = session.service("ALAnimationPlayer")
        self.ANIMATION = ALProxy("ALAnimationPlayer", self.IP, self.PORT)
        self.NETWORK = ALProxy("ALConnectionManager", self.IP, self.PORT)
        self.TTS = ALProxy("ALTextToSpeech", self.IP, self.PORT)
        self.AUDIORECORDER = ALProxy("ALAudioDevice", self.IP, self.PORT)
        self.SOUND_DETECT = ALProxy("ALSoundDetection", self.IP, self.PORT)
        self.MEMORY = ALProxy("ALMemory", self.IP, self.PORT)

        # TODO: Fil the Big-Fat-List-Of-Animation-Names(tm) with animation names (what else?)
        # Big-Fat-List-Of-Animation-Names(tm)
        self.EMOTIONS = {
            "HAPPY": ["placeholder"],
            "SAD": ["placeholder"],
            "CONFUSED": {"placeholder"},
            "SORRY": ["placeholder"],
            "ANGRY": ["placeholder"],
            "GREETING": ["placeholder"],
            "END": ["placeholder"]
        }

    def upload_audio(self, file_path, server_url):
        with open(file_path, 'rb') as audio_file:
            files = {"audio_file": audio_file}
            headers = {"Passcode": "p$T9wQz2a#R8fL!sE6hGn5vXyY3jU7iKo0bC1xZ4qJmO"}

            response = requests.post(server_url, files=files, headers=headers)

            # This should hopefully be the AI's response to the audio
            return response.text

    def record_audio(self):
        self.AUDIORECORDER.startMicrophonesRecording(self.RECORDING_PATH)
        time.sleep(10)
        self.AUDIORECORDER.stopMicrophonesRecording()

    def sound_detected(self, *args, **kwargs):
        if args[0] == 1:
            self.TTS.say("I heard something")
            print("I HEARD SOMETHING")

    def main(self):
        # self.SOUND_DETECT.setParameter("Sensitivity", 0.9)
        # self.SOUND_DETECT.subscribe("SoundDetected")
        # self.MEMORY.subscribeToEvent("SoundDetected", "main.py", "self.sound_detected")

        while True:
            self.SOUND_DETECT.setParameter("Sensitivity", 1.0)
            # self.SOUND_DETECT.subscribe("SoundDetected")
            # self.MEMORY.subscribeToEvent("SoundDetected", "PepperGPT", self.sound_detected)
            print(self.MEMORY.getData("SoundDetected"))
            print(len(self.MEMORY.getData("SoundDetected")))
            if len(self.MEMORY.getData("SoundDetected")) > 1:
                break
        try:
            print("helplo")
            self.AUDIORECORDER.startMicrophonesRecording(self.RECORDING_PATH)
            print("helload")
            time.sleep(5)
            self.AUDIORECORDER.stopMicrophonesRecording()
            print("hello")
            quit()
        except RuntimeError:
            pass
        # try:
        #     response = self.upload_audio(self.RECORDING_PATH, "http://127.0.0.1:5000/upload")
        #
        #     emotion, response = response.split("|")
        #
        #     for feeling in self.EMOTIONS.keys():
        #         if feeling == emotion:
        #             animation_to_play = random.choice(self.EMOTIONS[feeling])
        #
        #             # TODO: Make this the correct path
        #             self.ANIMATION.run(animation_to_play)
        #             self.TTS.say(response)
        # except RuntimeError:
        #     # TODO: Place animation here. Thinking or shrugging
        #     self.TTS.say("Hmm, it seems I'm not connected, check my wifi connection, or let my programmer know.")


if __name__ == '__main__':
    pepper_gpt = PepperGPT()
    pepper_gpt.main()
