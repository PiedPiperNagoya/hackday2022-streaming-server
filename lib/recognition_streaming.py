import time
import os
import wave
import speech_recognition
import json
import requests

# vars
SAMPLERATE = 44100
API_ADDR = 'http://ec2co-ecsel-17isx9yimwb9h-755813027.ap-northeast-1.elb.amazonaws.com:8080/api/'


class RecognitionStreaming:

    def __init__(self, stream_id):
        self.stream_id = stream_id

    def recognition_stream(self):
        global sprec
        sprec = speech_recognition.Recognizer()
        filename = "output.wav"

        try:
            wf = wave.open(filename, "r")
        except FileNotFoundError:
            print("[Error 404] No such file or directory: " + filename)
            return 0

        index = 0

        duration = 2
        chunk = SAMPLERATE * duration
        data = wf.readframes(chunk)
        while data != '':
            if os.path.getsize(filename) < chunk * index:
                time.sleep(0.2)
            else:
                index += 1
                self.recognition_data(data)
                data = wf.readframes(chunk)

    def recognition_data(self, in_data):
        global sprec
        try:
            audiodata = speech_recognition.AudioData(in_data, SAMPLERATE, 2)
            sprec_text = sprec.recognize_google(audiodata, language='ja-JP')
            self.send_api(sprec_text)
        except speech_recognition.UnknownValueError:
            pass
        except speech_recognition.RequestError as e:
            pass
        finally:
            return 0

    def send_api(self, text):
        obj = {
            'sentence': text
        }
        json_data = json.dumps(obj).encode("utf-8")
        headers = {"Content-Type": "application/json"}
        response = requests.post(
            url=API_ADDR + 'post/add/keywords',
            data=json_data,
            headers=headers)
        if response.status_code != 200:
            print(response.status_code)