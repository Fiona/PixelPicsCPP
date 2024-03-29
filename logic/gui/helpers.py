"""
PixelPics - Nonogram game
Copyright (c) 2014 Stompy Blondie Games http://stompyblondie.com
"""

# python imports
import os
import json
import urllib2

if os.name == 'nt':
    import urllib
    import threading
else:
    import multiprocessing
    
# Game engine imports
from core import *



def lerp(i, speed, start, end, smooth = True):
    speed -= 1
    p = 1.0/speed*i
    if smooth:
        p = ((p) * (p) * (3 - 2 * (p)))
    return start + (end - start) * p


def inverse_sequare_lerp(i, speed, start, end):
    speed -= 1
    p = 1.0/speed*i
    p = 1 - ((1 - p) * (1 - p))
    return start + (end - start) * p


def reverse_enumerate(l):
   for index in reversed(xrange(len(l))):
      yield index, l[index]



if os.name == 'nt':
   
    class FakeQueue(object):
        items = []
        def __init__(self):
            self.items = []
        def put(self, item):
            self.items.append(item)
        def get(self):
            return self.items.pop()



    class ThreadForNT(threading.Thread):
        def __init__(self, url, data, queue):
            self.url = url
            self.data = data
            self.queue = queue
            threading.Thread.__init__(self)

        def run(self):
            url = self.url
            data = self.data
            queue = self.queue
            if DEBUG:
                print "Opening request"
            data = json.dumps(data)
            response = None
            try:
                #import urllib
                f = urllib.urlopen(url, data)
                response = f.read()
                queue.put(response)
                f.close()
            except Exception, e:
                if DEBUG:            
                    print "Got exception %s" % e
                queue.put(None)                
            if DEBUG:
                print "Request complete response was: ", response
                print "----------------"
            return
        
        def terminate(self):
            pass



class Net_Process_POST(object):
    finished = False
    response = None

    def __init__(self, url, data):
        self.finished = False
        self.url = url
        self.data = data
        self.response = None
        self.running = False
        self.got_error = False

        if os.name == 'nt':
            self.data_queue = FakeQueue()
            self.process = ThreadForNT(self.url, self.data, self.data_queue)
        else:
            self.data_queue = multiprocessing.Queue() 
            self.process = multiprocessing.Process(target = self.run, args = (self.url, self.data, self.data_queue))
        if DEBUG:
            print "----------------"
            print "Starting POST net thread to: ", self.url
            print "Sending: ", self.data
        self.running = True        
        self.process.start()


    def is_complete(self):
        if self.process is None:
            return True
        
        self.finished = not self.process.is_alive()
        
        if self.finished and self.running:
            self.response = self.data_queue.get()
            self.process.terminate()
            self.process = None
            self.running = False

            if self.response is None:
                self.got_error = True
            else:
                self.response = json.loads(self.response)
            
        return self.finished


    def run(self, url, data, queue):
        if DEBUG:
            print "Opening request"
        data = json.dumps(data)
        response = None
        try:
            debuglevel = 2 if DEBUG else 0
            req = urllib2.Request(url, data, {'Content-Type': 'application/json'})
            opener = urllib2.build_opener(urllib2.HTTPHandler(debuglevel=debuglevel))
            f = opener.open(req)
            response = f.read()
            queue.put(response)
            f.close()
        except Exception, e:
            if DEBUG:            
                print "Got exception %s" % e
            queue.put(None)                
        if DEBUG:
            print "Request complete response was: ", response
            print "----------------"
        return


