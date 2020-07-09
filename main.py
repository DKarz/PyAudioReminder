import os
import time
import playsound
import speech_recognition as sr
from gtts import gTTS
import pyttsx3
from interruptingcow import timeout


messages = {}

def speak(text):
    tts = gTTS(text=text, lang="en")
    filename = "voice.mp3"
    tts.save(filename)
    playsound.playsound(filename)


def speak_ru(message):
    engine=pyttsx3.init()
    rate=engine.getProperty('rate')
    ru_voice_id = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_RU-RU_IRINA_11.0"
    engine.setProperty('voice', ru_voice_id)
    engine.setProperty('rate',rate-10)
    engine.say('{}'.format(message))
    engine.runAndWait()

def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("LISTENING")
        audio = r.listen(source, timeout=3)
        said = ""
        try:
            said = r.recognize_google(audio, language = 'en')
            print(said)
        except Exception as e:
            said = "ERROR"
            print("Exception: " + str(e))

    return said

def posible_time():
    pass

def listening():
    try:
        #with timeout(20.0, Outer):
            print(" $ start $")
            time_now = time.localtime()
            time_now_str = time.strftime("%H:%M", time_now)
            print("time: ", time_now_str)

            if time_now_str in messages.keys():
                read = messages[time_now_str]
                print("WEDIDIT " + read)
                speak(read)
                del messages[time_now_str]
                #speak(read + " . Повторяю ." + time_now_str +" . " + read)

            try:
                text = get_audio()
            except:
                text = " "
            said = text.split()
            if said[-1] == "stop":
                print(text)
            if "reminder" in said:
                sign = ""
                if "in" in said:
                    del said[1]
                    print("del", said)
                print(said[1])
                said[1].replace("-", "")
                if not ":" in said[1]:
                    sign = ":"
                tm = said[1][:2] + sign + said[1][2:]
                tm.replace("-", "")
                my_msg = ""
                try:
                    for word in said[2:]:
                        my_msg += word + ' '
                except: pass
                messages[tm] = my_msg
                print("OK. " + tm + " " + my_msg)
                speak("OK. " + tm + " " + my_msg)
            #print("HEREWEGO", messages)

    except Exception as E:
        print(E)

if __name__ == '__main__':
    while True:
        try:
            listening()
        except:
            print("BIG ERROR")
