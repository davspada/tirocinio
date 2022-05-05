import queue
from random import randint
import threading
import time
from numpy import empty

def produce(queue,index,lock):
        #global counter
        #print("in thread {} name is {} and data is : {}".format(threading.current_thread(),index, counter))
        new_counter = randint(0,10)
        print("THREAD "+str(index)+" ha creato :"+str(new_counter))
        time.sleep(3)
        #lock.acquire()
        with lock:
            queue.put(new_counter)
            print("-----thread"+str(index)+" inserisce "+str(new_counter))
        #lock.release()
        #print("data is {} id(data) is {}".format(data,id(data)))

def consume(queue,lock):
    
    print("---CONSUMER STARTED---")
    while(True):
        #lock.acquire()
        with lock:
            if(not queue.empty()):
                item = queue.get()
                print("in consumer {} value is {}".format(threading.current_thread(),item))
        #lock.release()
        time.sleep(1)
    
#potrei controllare se ogni thread ha finito, magari contare quelli finiti e in quel caso chiudere il consumer
        #print("in thread {} name is {}".format(threading.current_thread(),index))
    print("---CONSUMER ENDED---")



if __name__ == '__main__':
    #counter = 0
    lock = threading.Lock()
    q = queue.Queue()
    th_list = []
    
    c = threading.Thread(target=consume, args=(q, lock))
    
    for i in range(5):
        th = threading.Thread(target=produce,args=(q, i,lock))
        th_list.append(th)
        th.start() 

    c.start()

    for i in th_list:
        i.join()
        #print(i+i.is_alive)

    c.join()



    # WAIT E NOTIFY PER UCCIDERE IL CONSUMATORE????