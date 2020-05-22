############################################################
#
# NAVER WEBTOON DOWNLOAD V_PRO
# 
# (c) www.webtoon.ga & www.sites.ga
#
# More Info https://blog.naver.com/the3countrys/221970042824
#
# Donation Bitcoin: 3JmNLneiLvvNtcxGrnBjuemuqJbT44fzdq
#
#############################################################
import tkinter
from bs4 import BeautifulSoup
import requests
from PIL import Image as PILImage
import os
import tkinter.simpledialog

window = tkinter.Tk()
window.title("Webtoon Download")

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

#Frame
Frame_1 = tkinter.Frame()
Frame_1.pack()

Frame_2 = tkinter.Frame()
Frame_2.pack()

#
Start = tkinter.StringVar()
End = tkinter.StringVar()
Titleld = tkinter.StringVar()
Path = tkinter.StringVar()
result = tkinter.StringVar()

download_setting = "1"
type_of_webtoon = "0"
webtoon_type = "webtoon"
NID_AUT = ""
NID_SES = ""

def download_webtoon():
    try:
        global headers, download_setting, webtoon_type
        if type_of_webtoon == "0":
            webtoon_type = "webtoon"
        elif type_of_webtoon == "1":
            webtoon_type = "bestChallenge"
        elif type_of_webtoon == "2":
            webtoon_type = "challenge"
        for i in range(int(Start.get()),int(End.get())+1):
            c=1
            image_list = []
            img_name = []
            full_width, full_height = 0, 0
            response = requests.get(f'https://comic.naver.com/{webtoon_type}/detail.nhn?titleId={Titleld.get()}&no={i}', cookies = {"NID_AUT": NID_AUT, "NID_SES" : NID_SES,}).text
            soup = BeautifulSoup(response, 'html.parser')
            for anchor in soup.select('.wt_viewer img'):
                if anchor.get('src', '/')[:31] == "https://image-comic.pstatic.net":
                    url = anchor.get('src', '/')
                    img_data = requests.get(url, headers=headers).content
                    img_name.append(f'{Path.get()}{Titleld.get()}_{i}-{c}.jpg')
                    with open(img_name[-1], 'wb') as handler:
                        c+=1
                        handler.write(img_data)
                        if download_setting == "1" or download_setting == "2":
                            image_list.append(img_name[-1])
                        
            if download_setting == "1" or download_setting == "2":
                for f in image_list:
                    im = PILImage.open(f)
                    width, height = im.size
                    full_width = max(full_width, width)
                    full_height += height
                
                canvas = PILImage.new('RGB', (full_width, full_height), 'white')
                output_height = 0
                for im in image_list:
                    im= PILImage.open(im)
                    width, height = im.size
                    canvas.paste(im, (0, output_height))
                    output_height += height
                canvas.save(f"{Path.get()}{Titleld.get()}_{i}.jpg")
            if download_setting == "2":
                for f in img_name:
                    os.remove(f)
        result.set("Successfully download")
    except:
        result.set("Error")

    
    
def setting_type_of_webtoon(window=window):
    global type_of_webtoon
    d = tkinter.simpledialog.SimpleDialog(window,
                 text="Change the type of Naver Webtoon\n",
                 buttons=["Webtoon", "bestChallenge", "challenge"],
                 title="Test Dialog")
    type_of_webtoon = str(d.go())

def setting_download(window=window):
    global download_setting
    d = tkinter.simpledialog.SimpleDialog(window,
                 text="Change the download setting\n",
                 buttons=["Each of page", "Each of page and combine together", "Combine together"],
                 title="Test Dialog")
    download_setting = str(d.go())

def setting_adult_webtoon(window=window):
    global NID_SES, NID_AUT
    NID_SES = tkinter.simpledialog.askstring("Input", "What is your cookie of NID_SES?", parent=window)
    NID_AUT = tkinter.simpledialog.askstring("Input", "What is your cookie of NID_AUT?", parent=window)


menubar = tkinter.Menu(window)

filemenu = tkinter.Menu(menubar, tearoff=0)
filemenu.add_command(label="Download Setting", command=setting_download)
filemenu.add_command(label="Webtoon type Setting", command=setting_type_of_webtoon)
filemenu.add_command(label="Adult Webtoon Setting", command=setting_adult_webtoon)
menubar.add_cascade(label="Setting", menu=filemenu)

#menubar.add_command(label="Exit", command=window.quit)
window.config(menu=menubar)

#
Titleld_Label = tkinter.Label(Frame_1, text="Webtoon Titleld")
Titleld_Label.grid(row=0,column=0)

Titleld_Input = tkinter.Entry(Frame_1, textvariable=Titleld)
Titleld_Input.grid(row=0,column=1)

#
Path_Label = tkinter.Label(Frame_1, text="Path of download file")
Path_Label.grid(row=1,column=0)

Path_Input = tkinter.Entry(Frame_1, textvariable=Path)
Path_Input.grid(row=1,column=1)

#
Start_Label = tkinter.Label(Frame_1, text="Start Page")
Start_Label.grid(row=2,column=0)

Start_Input = tkinter.Entry(Frame_1, textvariable=Start)
Start_Input.grid(row=2,column=1)

End_Label = tkinter.Label(Frame_1, text="End Page")
End_Label.grid(row=3,column=0)

End_Input = tkinter.Entry(Frame_1, textvariable=End)
End_Input.grid(row=3,column=1)

#
Add_Button = tkinter.Button(Frame_2, text="Download", command=download_webtoon)
Add_Button.grid(row=0,column=0)

Label = tkinter.Label(Frame_2, textvariable=result)
Label.grid(row=1,column=0)

window.mainloop()
