"""
PixelPics - Nonogram game
(c) Stompy Blondie 2011/2012 http://stompyblondie.com
"""

# python imports
from itertools import izip
import os, urllib2, json

if os.name == 'nt':
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


def reverse_enumerate(l):
    return izip(xrange(len(l)-1, -1, -1), reversed(l))



if os.name == 'nt':
    class FakeQueue(object):
        items = []
        def __init__(self):
            self.items = []
        def put(self, item):
            self.items.append(item)
        def get(self):
            self.items.pop()



    class ThreadForNT(threading.Thread):
        def __init__(self, url, data, queue):
            threading.Thread.__init__(self)
            self.url = url
            self.data = data
            self.queue = queue

        def run(self):
            url = self.url
            data = self.data
            queue = self.queue
            if DEBUG:
                print "Opening request"
            data = json.dumps(data)
            response = None
            try:
                req = urllib2.Request(url, data, {'Content-Type': 'application/json'})
                opener = urllib2.build_opener(urllib2.HTTPHandler(debuglevel=2))
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
        self.running = True
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


    def run(url, data, queue):
        if DEBUG:
            print "Opening request"
        data = json.dumps(data)
        response = None
        try:
            req = urllib2.Request(url, data, {'Content-Type': 'application/json'})
            opener = urllib2.build_opener(urllib2.HTTPHandler(debuglevel=2))
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


