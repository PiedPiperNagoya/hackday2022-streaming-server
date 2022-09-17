import time
import os
import speech_recognition
import wave

SAMPLERATE = 44100


def recognition_data(in_data):
    global sprec
    try:
        audiodata = speech_recognition.AudioData(in_data, SAMPLERATE, 2)
        sprec_text = sprec.recognize_google(audiodata, language='ja-JP')
        print(sprec_text)
    except speech_recognition.UnknownValueError:
        pass
    except speech_recognition.RequestError as e:
        pass
    finally:
        return 0


def main():
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
            recognition_data(data)
            data = wf.readframes(chunk)


if __name__ == '__main__':
    main()
