import StringIO
import os.path
import pycurl
from mercurial.patch import fsbackend
 
 
 
class PyCurl(object):
    def __init__(self, filename='risa.wav', lang='ko-kr', output='json',
                key=None, url=None):
        self.filename = filename
        self.lang = lang
        self.output = output
        self.key = 'AIzaSyBOti4mM-6x9WDnZIjIeyEU21OpBXqWBgw'
 
        self.url = 'https://www.google.com/speech-api/v2/recognize?output='
 
    def performPyCurl(self):
        apiUrl =''
        apiUrl +=self.url + self.output + '&lang=' + self.lang + '&key=' + self.key
        c = pycurl.Curl()
        c.setopt(pycurl.VERBOSE, 1)
        c.setopt(pycurl.URL, apiUrl)
        fout = StringIO.StringIO()
        c.setopt(pycurl.WRITEFUNCTION, fout.write)
 
        c.setopt(pycurl.POST, 1)
        c.setopt(pycurl.HTTPHEADER,
                 ['Content-Type : audio/l16 ; rate=16000;'])
 
        filesize = os.path.getsize(self.filename)
        c.setopt(pycurl.POSTFIELDSIZE, filesize)
        fin = open(self.filename, 'rb')
        c.setopt(pycurl.READFUNCTION, fin.read)
        c.perform()
        response_code = c.getinfo(pycurl.RESPONSE_CODE)
        response_data = fout.getvalue()
        # print response_code
        print response_data
 
        # json file saved
        fsave = open('return.json', 'wb')
        fsave.write(response_data)
        c.close()
    def __enter__(self):
        return self
 
    def __exit__(self, exception, value, traceback):
        self.close()
 
 