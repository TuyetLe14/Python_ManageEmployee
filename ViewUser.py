from connectDB import CnnDatabase
from ModelUser import ModelUser
from tkinter import *
import tkinter as tk
from PIL import Image, ImageTk
class ViewUser(tk.Tk):
    def __init__(self, server, database):
        super().__init__()
        self.title('THÔNG TIN NHÂN VIÊN')
        self.geometry('1350x750')
        self.config(bg='lightblue')

        self.ket_noi = CnnDatabase(server, database)
        self.ct = ModelUser(server, database, self.ket_noi)

        # ==================================================Variables=================================================
        self.MaNV = StringVar()
        self.name = StringVar()
        self.Dchi = StringVar()
        self.NgSinh = StringVar()
        self.LuongCB = StringVar()
        self.LoaiNV = StringVar()
        self.LuongHT = StringVar()

        # Khung=====================================================================

        self.Main_Frame = LabelFrame(self.master, width=1300, height=500, font=('arial', 20, 'bold'),
                                     bg='lightblue', bd=15, relief='ridge')
        self.Main_Frame.grid(row=1, column=1, padx=10, pady=20)
        self.Frame_1 = LabelFrame(self.Main_Frame, width=600, height=400, font=('arial', 15, 'bold'),
                                  relief='ridge', bd=10, bg='lightblue', text='Thông Tin Cá Nhân ')
        self.Frame_1.grid(row=1, column=0, padx=10)

        self.Frame_3 = LabelFrame(self.master, width=1200, height=100, font=('arial', 10, 'bold'),
                                  bg='lightblue', relief='ridge', bd=13)
        self.Frame_3.grid(row=2, column=1, pady=10)

        # Label name========================================================
        self.Label_MaNV = Label(self.Frame_1, text='Mã Nhân Viên', font=('arial', 20, 'bold'), bg='lightblue')
        self.Label_MaNV.grid(row=0, column=0, sticky=W, padx=20, pady=10)
        self.Label_name = Label(self.Frame_1, text='Họ Và Tên', font=('arial', 20, 'bold'), bg='lightblue')
        self.Label_name.grid(row=1, column=0, sticky=W, padx=20)
        self.Label_Dchi = Label(self.Frame_1, text='Địa Chỉ', font=('arial', 20, 'bold'), bg='lightblue')
        self.Label_Dchi.grid(row=2, column=0, sticky=W, padx=20)
        self.Label_NgSinh = Label(self.Frame_1, text='Ngày Sinh', font=('arial', 20, 'bold'), bg='lightblue')
        self.Label_NgSinh.grid(row=3, column=0, sticky=W, padx=20)
        self.Label_LuongCB = Label(self.Frame_1, text='Lương Cơ Bản', font=('arial', 20, 'bold'), bg='lightblue')
        self.Label_LuongCB.grid(row=4, column=0, sticky=W, padx=20)
        self.Label_LoaiNV = Label(self.Frame_1, text='Loại Nhân Viên', font=('arial', 20, 'bold'), bg='lightblue')
        self.Label_LoaiNV.grid(row=5, column=0, sticky=W, padx=20)

        # Khung Label nhập========================================================
        self.Entry_MaNV = Entry(self.Frame_1, font=('arial', 17, 'bold'), textvariable=self.MaNV, state=DISABLED)
        self.Entry_MaNV.grid(row=0, column=1, padx=10, pady=5)
        self.Entry_name = Entry(self.Frame_1, font=('arial', 17, 'bold'), textvariable=self.name, state=DISABLED)
        self.Entry_name.grid(row=1, column=1, padx=10, pady=5)
        self.Entry_Dchi = Entry(self.Frame_1, font=('arial', 17, 'bold'), textvariable=self.Dchi, state=DISABLED)
        self.Entry_Dchi.grid(row=2, column=1, padx=10, pady=5)
        self.Entry_NgSinh = Entry(self.Frame_1, font=('arial', 17, 'bold'), textvariable=self.NgSinh, state=DISABLED)
        self.Entry_NgSinh.grid(row=3, column=1, padx=10, pady=5)
        self.Entry_LuongCB = Entry(self.Frame_1, font=('arial', 17, 'bold'), textvariable=self.LuongCB, state=DISABLED)
        self.Entry_LuongCB.grid(row=4, column=1, padx=10, pady=5)
        self.Entry_LoaiNV = Entry(self.Frame_1, font=('arial', 17, 'bold'), textvariable=self.LoaiNV, state=DISABLED)
        self.Entry_LoaiNV.grid(row=5, column=1, padx=10, pady=5)
        # Khung Button=========================================================
        self.buttons = {
            "EXIT": tk.Button(self.Frame_3, text="  EXIT", font=('arial', 17, 'bold'), width=100)
        }

        self.buttons["EXIT"].grid(row=0, column=6, padx=10, pady=10)


        img2 = Image.open("EXIT.png")
        img2 = img2.resize((30, 30), Image.LANCZOS)
        img2 = ImageTk.PhotoImage(img2)
        self.buttons["EXIT"].img2 = img2
        self.buttons["EXIT"].config(image=img2, compound=LEFT)


