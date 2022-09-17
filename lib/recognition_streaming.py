import time
import os
import wave
import speech_recognition
import json
import requests
import subprocess

# vars
SAMPLERATE = 44100
API_ADDR = 'http://ec2co-ecsel-17isx9yimwb9h-755813027.ap-northeast-1.elb.amazonaws.com:8080/api/'


class RecognitionStreaming:

    def __init__(self, stream_id):
        self.stream_id = stream_id
        self.ffmpeg_process = None

    def recognition_stream(self, stream_status):
        progress_file = '.' + self.stream_id + '_progressing'

        print(stream_status)

        if stream_status == 'stop':
            if not os.path.isfile(progress_file):
                return 'Not Started Yet'
            os.remove(progress_file)
            return 'Job Accepted'
        elif os.path.isfile(progress_file):
            return 'Already Started'

        global sprec
        sprec = speech_recognition.Recognizer()
        filename = self.stream_id + '_output.wav'

        try:
            wf = wave.open(filename, 'r')
        except FileNotFoundError:
            return '[Error 404] No such file or directory: ' + filename

        index = 0

        duration = 2
        chunk = SAMPLERATE * duration
        data = wf.readframes(chunk)

        # create progress file
        f = open(progress_file, 'w')
        f.write('')
        f.close()

        while data != '':
            if os.path.getsize(filename) < chunk * index:
                time.sleep(0.2)
            elif not os.path.isfile(progress_file):
                self.ffmpeg_process.kill
                break
            else:
                index += 1
                self.recognition_data(data)
                data = wf.readframes(chunk)
        return 0

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
        json_data = json.dumps(obj).encode('utf-8')
        headers = {'Content-Type': 'application/json'}
        response = requests.post(
            url=API_ADDR + 'post/add/keywords',
            data=json_data,
            headers=headers)
        if response.status_code != 200:
            print(response.status_code)

    def stream_to_wav(self):
        cmd = 'ffmpeg -i rtmp://54.250.156.152/stream/live -vn -y -ar 44100 -ac 1' + \
            self.stream_id + '_output.wav'
        self.ffmpeg_process = subprocess.Popen('exec ' + cmd, shell=True)
