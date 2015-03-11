"""
This comes from a tutorial found here:
https://www.youtube.com/watch?v=i1SW4q9yUEs

I want to create a queue so that LIDAR data can be captured
independently from any drawing. I'm worried the drawing
will slow down the reading and data points will be dropped

I initially thought to use RabbitMQ or ZeroMQ but this seemed
like I was thinking in the wrong direction. I think threads
are the way to go. If we decide to process offline from the 
bot itself then I will switch back to the Queue
"""

import threading, time, random
try:
    import Queue
except:
    import queue as Queue

class Producer:
    def __init__(self):
        self.food = ["ham", "soup", "salad"]
        self.nextTime = 0
    
    def run(self):
        global q
        while (time.clock() < 10):
            if(self.nextTime < time.clock()):
                f = self.food[random.randrange(len(self.food))]
                q.put(f)
                print("Adding " + f)
                self.nextTime += random.random()

class Consumer:
    def __init__(self):
        self.nextTime = 0
    def run(self):
        global q
        while (time.clock() < 10):
            if (self.nextTime < time.clock() and not q.empty()):
                f = q.get()
                print("Removing " + f)
                self.nextTime += random.random() * 2

if __name__ == '__main__':
    q = Queue.Queue(10)
    
    p = Producer()
    c = Consumer()
    pt = threading.Thread(target=p.run, args=())
    ct = threading.Thread(target=c.run, args=())
    pt.start()
    ct.start()
            

