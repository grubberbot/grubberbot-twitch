import os

import pyttsx3
from dotenv import load_dotenv
from twitchobserver import Observer

# for the tts
load_dotenv()
TWITCH_TOKEN = os.getenv("TWITCH_TOKEN")

# TODO get list of mods instead of hard-coding mod usernames
CHANNEL = "pawngrubber"
MODS = [
    "rkmartin1",
    #'bec4use',
    "eccentrichorse11",
    "gurkiratsingh17",
    "acuddlypuppie",
    #'harappa234',
    "sfdc_mike",
    "monichess12",
    "hamsterham88",
    "punkcoreyoda",
    "vitothemonkey",
    "venuschess",
    "soham_slp",
    "krapig",
    "pawngrubber",
    "thefuxia",
    "smarterchess",
    "streamlabs",
    "grubberbot",
    "lalizig",
    "paradajzcity",
    "duellinksguy",
    "thewretch2",
    "vietd",
    "poitaoforpresident",
    "chesscomchris",
    "mynameislegyon",
    "f0rgetaboutit",
    "zuname",
    "rakshakthetall",
    "drittman13",
    "expired_febreeze",
    "strance_02",
    "marko_sreck",
    "flyingseverus",
]

SKIP = [
    "harappa234",
]


class TTS:
    def __init__(self):
        self.engine = self.build_engine()

    def build_engine(self):
        engine = pyttsx3.init()
        engine.setProperty("rate", 150)
        engine.setProperty("voice", engine.getProperty("voices")[-2].id)
        return engine

    def chat_speak(self, message, nickname):
        self.engine.setProperty("voice", self.engine.getProperty("voices")[-1].id)
        self.engine.setProperty("volume", 0.25)
        self.speak(message, nickname)

    def mod_speak(self, message, nickname):
        self.engine.setProperty("voice", self.engine.getProperty("voices")[-2].id)
        self.engine.setProperty("volume", 1.0)
        self.speak(message, nickname)

    def speak(self, message, nickname):
        if "!tts" in message:
            text = message.lstrip("!tts")
            filename = "tts.txt"
            with open(filename, "w") as f:
                print(f"{nickname}: {text}", file=f)
            self.engine.say(text)
            self.engine.runAndWait()


def main():
    tts = TTS()

    with Observer("username", TWITCH_TOKEN) as observer:
        observer.join_channel(CHANNEL)
        print("Joined channel", CHANNEL)
        print(
            "Press Ctrl+C to quit, you might have to close the terminal window sometimes."
        )

        while True:
            try:
                for event in observer.get_events():
                    if event.type == "TWITCHCHATMESSAGE":
                        message = event.message

                        if event.nickname in MODS:
                            tts.mod_speak(message, event.nickname)
                        elif event.nickname not in SKIP:
                            tts.chat_speak(message, event.nickname)

            except Exception as e:
                print(e)
                observer.leave_channel(CHANNEL)
                observer.stop()
                quit()


if __name__ == "__main__":
    main()
