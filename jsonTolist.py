# -*- coding: utf-8 -*-
import json
import os
from pprint import pprint
 
 
CONFIG={}
 
 
 
class JsonTolist(object):
 
    CONFIG_FILE = "return.json"
    JSON_FILE = "return2.json"
 
    def __init__(self, filename='return.json',json_file = 'return2.json'):
        self.filename = filename
        self.json_file = json_file
 
    def save(self):
        file_size = os.path.getsize(self.filename)
        f = open(self.filename, 'rb')
 
        fr = open('return2.json', 'wb')
        fr.write('{')
        # print s
        for i in range(0, file_size):
            n = f.read(i)
 
            if i >= 6:
                # print n
                fr.write(n)
        fr.close()
        f.close()
 
    def retJsonList(self):
 
        try :
            with open(self.json_file) as data_file:
                data = json.load(data_file)
 
        except ValueError :
            print "¿¡·¯"
            return None
        list = []
        i = 0
        while True:
            try:
                text = data['result'][0]['alternative'][i]['transcript']
                i = i + 1
                print text
                list.append(text)
            except IndexError:
                break
 
        # list.append(text)
        return list
 