#!/bin/python3

import queue
import threading
import time
import random

exitFlag = 0

#Defining the over all process
class myThread (threading.Thread):
        def __init__(self, threadID, name, q):
                threading.Thread.__init__(self)
                self.threadID = threadID
                self.name = name
                self.q = q
        def run(self):
                print(self.name + " is open.")
                process_data(self.name, self.q)
                print(self.name + " is closed." )

#Defining the threads that will run.
def process_data(threadName, q):
        while not exitFlag:
                #Is a new customer coming into the line?
                new = random.randint(1,2)
                while len(nameList) != 0 and workqueue.qsize() <= 19 and new > 0:
                         #Yes? Lets let them in if there is space.
                         workqueue.put(nameList.pop(0))
                         new -= 1
                print("There are now ",workqueue.qsize()," customers in line.")
                queueLock.acquire()
                #If there are customers in line and a counter is open sent them to the counter.
                if not workqueue.empty():
                        data = q.get()
                        queueLock.release()
                        print( "%s is processing customer %s" % (threadName, data))
                        time.sleep(random.uniform(0,5))
                        print("There are now ",workqueue.qsize()," customers in line.")
                #If there are no customers waiting then do nothing
                elif len(nameList) != 0:
                        queueLock.release()
                time.sleep(1)
#How many coustomers are we planning on having today?
custotal = random.randint(20,100)

#Setting up the counters
threadList = ["Counter1", "Counter2", "Counter3"]

#Organizing and numbering the customers
count = 0
nameList = []
while count < custotal:
	count += 1
	cur=str(count)
	nameList.append(cur)
queueLock = threading.Lock()

#Defining the line as a queue
workqueue = queue.Queue(21)

#Initializing the threads
threads = []
threadID = 1

# Create new threads
for tName in threadList:
        thread = myThread(threadID, tName, workqueue)
        thread.start()
        threads.append(thread)
        threadID += 1

# Wait for queue to empty
while not workqueue.empty():
        pass

# Notify threads it's time to exit
exitFlag = 1

# Wait for all threads to complete
for t in threads:
        t.join()
print("All counters are closed. Please come back tomorrow.")
