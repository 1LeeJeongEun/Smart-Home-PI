#-*- coding:utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
 
import recorder
import jsonTolist
import transCurl
 
from time import ctime
import time
import os
from gtts import gTTS
 
import pyaudio
import wave
 
#GPIO setup
import RPi.GPIO as GPIO
import time
 
GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.OUT)
GPIO.output(23, False)
GPIO.setup(24, GPIO.OUT)
GPIO.output(24, False)
GPIO.setup(18, GPIO.OUT)
GPIO.output(18, False)
 
#Record voice
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 1024
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "voice_record.wav"
 
audio = pyaudio.PyAudio()
 
def speak(audioString):
    print(audioString)
    tts = gTTS(text=audioString, lang='ko')
    tts.save("audio.mp3")
    os.system("mpg321 audio.mp3")
 
def voice_record():
    # start Recording
    stream = audio.open(format=pyaudio.paInt16, 
        channels=CHANNELS, 
        rate=RATE, 
        input=True, 
        input_device_index=2,
        frames_per_buffer=CHUNK)
    print "recording..."
    frames = []
 
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    print "finished recording"
     
    # stop Recording
    stream.stop_stream()
    stream.close()
    audio.terminate()
     
    waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()
    
 
def requestGoogle():
    # save wave file
    recSet = recorder.Recorder()
    rec = recSet.open()
    rec.record(3)
    rec.close()
    # send goolge server with curl command
    transCurl.PyCurl().performPyCurl()
 
    # compare to json data
    jlist = jsonTolist.JsonTolist()
    jlist.save()
    json_list = jlist.retJsonList()
    return json_list
 
def start():
    K = 1
    speak('프로그램을 시작합니다.')
    os.system("rm -rf audio.mp3")
    while K:
       # command = raw_input("Name : ")
        command = 'Start'
        speak('말해주세요')
        if command == 'Start':
            json_li = requestGoogle()
          
            # print json_list
            text = 'LED'
            red = '빨간색'
            yellow = '노란색'
            green = '초록색'
            kimchi = '사진'
            ledoff = '불 꺼 줘'
            ledon = '불 켜 줘'
            record = '녹음'
            play = '재생'
            bye = '빠이'
            
            try :
                for x in json_li:
                    if text.find(x) != -1:
                        speak("엘이디 제어 화면 입니다. 어떤 불을 켜드릴까요?")
                        json_li = requestGoogle()
                        for x in json_li:
                             if red.find(x) != -1:
                                    speak("빨간불을 킬게요")
                                    GPIO.output(23, True)
                                    time.sleep(1)
                                    break
                             elif yellow.find(x) != -1:
                                    speak("노란불을 킬게요")
                                    GPIO.output(24, True)
                                    time.sleep(1)
                                    break
                             elif green.find(x) != -1:
                                    speak("초록불을 킬게요")
                                    GPIO.output(18, True)
                                    time.sleep(1)
                                    break
                             elif ledoff.find(x) != -1:
                                    speak("모든 불을 끌게요")
                                    GPIO.output(23, False)
                                    GPIO.output(24, False)
                                    GPIO.output(18, False)
                                    time.sleep(1)
                                    break
                             elif ledon.find(x) != -1:
                                    speak("모든 불을 켤게요")
                                    GPIO.output(23, True)
                                    GPIO.output(24, True)
                                    GPIO.output(18, True)
                                    time.sleep(1)
                                    break                                  
                             break 
                    elif kimchi.find(x) !=-1:
                        speak('사진을 찍습니다.')
                        os.system('fswebcam --fps 15 -S 8 image.jpg')
                    elif record.find(x) !=-1:
                        speak('녹음을 시작합니다.')
                        voice_record()
                    elif play.find(x) !=-1:
                        speak('녹음파일을 들려드릴게요.')
                        os.system('aplay voice_record.wav')
                    elif bye.find(x) !=-1:
                        speak('안녕히 계세요. 다음에 또 만나요 빠이 빠이')
                        K = 0
            except:
                speak("입력된 명령어가 없습니다.")
 
if __name__ == "__main__":
    start()
    sys.exit()