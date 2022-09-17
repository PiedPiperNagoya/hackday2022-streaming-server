import time
import speech_recognition
import pyaudio
import soundfile as sf

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

    # read stream file
    filename = "output.wav"
    data, rate = sf.read(filename)

    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=1,
                    rate=rate,
                    output=True)
    stream.start_stream()
    while stream.is_active():
        time.sleep(0.1)

    stream.stop_stream()
    stream.close()
    audio.terminate()


if __name__ == '__main__':
    main()
