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
    speak('���α׷��� �����մϴ�.')
    os.system("rm -rf audio.mp3")
    while K:
       # command = raw_input("Name : ")
        command = 'Start'
        speak('�����ּ���')
        if command == 'Start':
            json_li = requestGoogle()
          
            # print json_list
            text = 'LED'
            red = '������'
            yellow = '�����'
            green = '�ʷϻ�'
            kimchi = '����'
            ledoff = '�� �� ��'
            ledon = '�� �� ��'
            record = '����'
            play = '���'
            bye = '����'
            
            try :
                for x in json_li:
                    if text.find(x) != -1:
                        speak("���̵� ���� ȭ�� �Դϴ�. � ���� �ѵ帱���?")
                        json_li = requestGoogle()
                        for x in json_li:
                             if red.find(x) != -1:
                                    speak("�������� ų�Կ�")
                                    GPIO.output(23, True)
                                    time.sleep(1)
                                    break
                             elif yellow.find(x) != -1:
                                    speak("������� ų�Կ�")
                                    GPIO.output(24, True)
                                    time.sleep(1)
                                    break
                             elif green.find(x) != -1:
                                    speak("�ʷϺ��� ų�Կ�")
                                    GPIO.output(18, True)
                                    time.sleep(1)
                                    break
                             elif ledoff.find(x) != -1:
                                    speak("��� ���� ���Կ�")
                                    GPIO.output(23, False)
                                    GPIO.output(24, False)
                                    GPIO.output(18, False)
                                    time.sleep(1)
                                    break
                             elif ledon.find(x) != -1:
                                    speak("��� ���� �ӰԿ�")
                                    GPIO.output(23, True)
                                    GPIO.output(24, True)
                                    GPIO.output(18, True)
                                    time.sleep(1)
                                    break                                  
                             break 
                    elif kimchi.find(x) !=-1:
                        speak('������ ����ϴ�.')
                        os.system('fswebcam --fps 15 -S 8 image.jpg')
                    elif record.find(x) !=-1:
                        speak('������ �����մϴ�.')
                        voice_record()
                    elif play.find(x) !=-1:
                        speak('���������� ����帱�Կ�.')
                        os.system('aplay voice_record.wav')
                    elif bye.find(x) !=-1:
                        speak('�ȳ��� �輼��. ������ �� ������ ���� ����')
                        K = 0
            except:
                speak("�Էµ� ��ɾ �����ϴ�.")
 
if __name__ == "__main__":
    start()
    sys.exit()