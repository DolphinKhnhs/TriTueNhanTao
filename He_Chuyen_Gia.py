from tkinter import *
from tkinter import messagebox

def Create_Label(main):
    labels = [
        ("Thời tiết:", 40),
        ("Sức khỏe:", 70),
        ("Bài kiểm tra:", 100),
        ("Số buổi vắng >= 3?:", 130),
        ("Vui lòng chọn 1 trong 2 lựa chọn!", 10)
    ]
    for text, y in labels:
        Label(main, text=text, font=("Arial", 10, "bold")).place(x=10,y=y)

def SuyLuan():
    if KiemTra1.get(): 
      return "Nên đi học!"
    if SoBuoiVang1.get(): 
        return "Nên đi học!"
    if SucKhoe2.get():
      return "Không nên đi học!"
    if ThoiTiet2.get():   
        return "Không nên đi học!"
    return "Nên đi học!"

def Ketqua():
   ketqua = SuyLuan()
   messagebox.showinfo("Kết Luận", ketqua)

def ChonMot(var1, var2):
    if var1.get():
        var2.set(False)

MAIN = Tk()
MAIN.title("Simple Expert System")
MAIN.geometry("500x250")
MAIN.resizable(False, False)

Create_Label(MAIN)

ThoiTiet1 = BooleanVar()
ThoiTiet2 = BooleanVar()
SucKhoe1  = BooleanVar()
SucKhoe2 = BooleanVar()
KiemTra1    = BooleanVar()
KiemTra2    = BooleanVar()
SoBuoiVang1  = BooleanVar()
SoBuoiVang2  = BooleanVar()

cb = [
    ("Đẹp", 200, 40, ThoiTiet1, ThoiTiet2),
    ("Xấu", 350, 40, ThoiTiet2, ThoiTiet1),
    ("Bình thường", 200, 70, SucKhoe1, SucKhoe2),
    ("Mệt mỏi", 350, 70, SucKhoe2, SucKhoe1),
    ("Có", 200, 100, KiemTra1, KiemTra2),
    ("Không", 350, 100, KiemTra2, KiemTra1),
    ("Có", 200, 130, SoBuoiVang1, SoBuoiVang2),
    ("Không", 350, 130, SoBuoiVang2, SoBuoiVang1)
    ]
for text, x, y, opt1,opt2  in cb:
  Checkbutton(MAIN, text=text, font=("Arial", 10), variable=opt1, command=ChonMot(opt1, opt2)).place(x=x,y=y)

Button(MAIN, text="Kết luận", font=("Arial", 12, "bold"), command=Ketqua).place(x=200,y=170)
MAIN.mainloop()
