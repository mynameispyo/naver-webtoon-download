import tkinter
from bs4 import BeautifulSoup
import requests

window = tkinter.Tk()
window.title("Webtoon Download")

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
photo = tkinter.PhotoImage(file = "./img/download.ico")
window.iconphoto(False, photo)
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

def download_webtoon():
    try:
        global headers
        for i in range(int(Start.get()),int(End.get())+1):
            c=1
            response = requests.get(f'https://comic.naver.com/webtoon/detail.nhn?titleId={Titleld.get()}&no={i}').text
            soup = BeautifulSoup(response, 'html.parser')
            for anchor in soup.find_all('img'):
                if anchor.get('src', '/')[:31] == "https://image-comic.pstatic.net":
                    url = anchor.get('src', '/')

                    img_data = requests.get(url, headers=headers).content
                    with open(f'{Path.get()}{i}-{c}.jpg', 'wb') as handler:
                        handler.write(img_data)
                        c+=1
        result.set("Successfully download")
    except:
        result.set("Error")
                        

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
