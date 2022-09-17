import time
import speech_recognition
import pyaudio
import wave

SAMPLERATE = 44100


def callback(in_data, frame_count, time_info, status):
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
        return (None, pyaudio.paContinue)


def main():
    global sprec
    sprec = speech_recognition.Recognizer()
    filename = "output.wav"

    try:
        wf = wave.open(filename, "r")
    except FileNotFoundError:
        print("[Error 404] No such file or directory: " + Filename)
        return 0

    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
                    rate=SAMPLERATE,
                    channels=1,
                    input_device_index=1,
                    input=True,
                    frames_per_buffer=SAMPLERATE*2,
                    stream_callback=callback,
                    output=False)
    stream.start_stream()
    while stream.is_active():
        time.sleep(0.1)

    stream.stop_stream()
    stream.close()


if __name__ == '__main__':
    main()
