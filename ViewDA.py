from connectDB import CnnDatabase
from ModelDA import ModelDA
from tkinter import *
from tkinter import ttk
from tkinter import Canvas
import tkinter as tk
from tkcalendar import DateEntry
from PIL import Image, ImageTk
import time

class ViewDA(tk.Tk):
    def __init__(self, server, database):
        super().__init__()
        self.title('HỆ THỐNG QUẢN LÝ NHÂN VIÊN')
        self.geometry('1350x750')
        self.config(bg='lightblue')
        self.stt_counter = 0

        self.ket_noi = CnnDatabase(server, database)
        self.ct = ModelDA(server, database, self.ket_noi)

        # ==================================================Variables=================================================
        self.IDnv = StringVar()
        self.name = StringVar()
        self.place = StringVar()
        self.date = StringVar()
        self.salaryCB = StringVar()
        self.LoaiNV = StringVar()
        self.totalSalary = DoubleVar()

        # ==================================================Frames===================================================
        Main_Frame = Frame(self.master, bg='lightblue')
        Main_Frame.grid()

        Title_Frame = LabelFrame(
            Main_Frame, width=1350, height=100, bg='lightblue', relief='ridge', bd=15)
        Title_Frame.pack(side=TOP)

        self.lblTitle = Label(Title_Frame, font=('arial', 40, 'bold'), text='QUẢN LÝ NHÂN VIÊN',
                              bg='lightblue', padx=13)
        self.lblTitle.grid(padx=550)

        # ==================================DATE TIME======================================================
        localtime = time.asctime(time.localtime(time.time()))
        lblInfo = Label(Title_Frame, font=('arial', 12, 'bold'), text=localtime, bd=10, anchor='w')
        lblInfo.grid(row=1, column=0)
        # ===================================================================================================

        Data_Frame = Frame(Main_Frame, width=1350, height=340,
                           bg='lightblue', relief='ridge', bd=15)
        Data_Frame.pack(side=TOP, padx=15)

        Frame_1 = LabelFrame(Data_Frame, width=850, height=330, bg='Navajo white', relief='ridge', bd=8,
                             text='THÔNG TIN', font=('arial', 15, 'bold'))
        Frame_1.pack(side=LEFT, padx=10)

        Display = LabelFrame(Data_Frame, width=495, height=330, bg='Navajo white', relief='ridge', bd=8,
                             text='Thông tin', font=('arial', 15, 'bold'))
        Display.pack(side=RIGHT, padx=10)

        Combined_Frame = Frame(Main_Frame, bg='lightblue')
        Combined_Frame.pack(side='top', padx=10)

        # Tạo List_Frame (khung bên trái)
        List_Frame = Frame(Combined_Frame, width=1800, height=200, bg='Navajo white', relief='ridge', bd=15)
        List_Frame.pack(side='left')

        # Tạo Image_Frame (khung bên phải)
        Image_Frame = Frame(Combined_Frame, width=190, height=220, bg='Navajo white', relief='ridge', bd=15)
        Image_Frame.pack(side='left', padx=10)
        Button_Frame = Frame(Main_Frame, width=1350, height=80,
                             bg='Navajo white', relief='ridge', bd=15)
        Button_Frame.pack(side=TOP)

        # ===================================================Labels================================================
        self.IDnv_label = Label(Frame_1, text='Mã nhân viên : ', font=(
            'arial', 14, 'bold'), bg='Navajo white')
        self.IDnv_label.grid(row=0, column=0, padx=15, sticky=W)

        self.name_label = Label(Frame_1, text='Họ tên : ', font=(
            'arial', 14, 'bold'), bg='Navajo white')
        self.name_label.grid(row=1, column=0, padx=15, sticky=W)

        self.place_label = Label(Frame_1, text='Địa chỉ : ', font=(
            'arial', 14, 'bold'), bg='Navajo white')
        self.place_label.grid(row=2, column=0, padx=15, sticky=W)

        self.Date_label = Label(Frame_1, text='Ngày sinh : ', font=(
            'arial', 14, 'bold'), bg='Navajo white')
        self.Date_label.grid(row=3, column=0, padx=15, sticky=W)

        self.salaryCB_label = Label(Frame_1, text='Lương cơ bản : ', font=(
            'arial', 14, 'bold'), bg='Navajo white')
        self.salaryCB_label.grid(row=4, column=0, padx=15, sticky=W)

        self.lbLoaiNV = Label(Frame_1, text="Loại NV:", font=(
            'arial', 14, 'bold'), bg='Navajo white')
        self.lbLoaiNV.grid(row=5, column=0, padx=15, sticky=W)

        self.totalSalary_label = Label(Frame_1, text='Lương HT: ', font=(
            'arial', 14, 'bold'), bg='Navajo white')
        self.totalSalary_label.grid(row=3, column=3, padx=5, sticky=W)

        self.Search_label = Label(Frame_1, text='Tìm kiếm: ', font=(
            'arial', 14, 'bold'), bg='Navajo white')
        self.Search_label.grid(row=5, column=3, padx=5, sticky=W)

        # ==================================================Entries================================================

        self.IDnv_entry = Entry(Frame_1, font=(
            'arial', 14), textvariable=self.IDnv)
        self.IDnv_entry.grid(row=0, column=1, padx=15, pady=5)

        self.name_entry = Entry(Frame_1, font=(
            'arial', 14), textvariable=self.name)
        self.name_entry.grid(row=1, column=1, padx=15, pady=5)

        self.place_entry = Entry(Frame_1, font=(
            'arial', 14), textvariable=self.place)
        self.place_entry.grid(row=2, column=1, padx=15, pady=5)

        self.date = tk.StringVar()
        self.Date_entry = DateEntry(Frame_1, font=('arial', 14), textvariable=self.date,
                                    date_pattern='dd/mm/yyyy')
        self.Date_entry.grid(row=3, column=1, padx=15, pady=5)

        self.salaryCB_entry = Entry(Frame_1, font=('arial', 14), textvariable=self.salaryCB)
        self.salaryCB_entry.grid(row=4, column=1, padx=15, pady=5)

        self.LoaiNV_entry = ttk.Combobox(Frame_1, values=(' ', 'Bán Hàng', 'Văn Phòng', 'Admin'),
                                         font=('arial', 14), width=19,
                                         textvariable=self.LoaiNV)
        self.LoaiNV_entry.grid(row=5, column=1, padx=15, pady=5)

        self.totalSalary_entry = Entry(Frame_1, font=(
            'arial', 14), width=13, textvariable=self.totalSalary, state='readonly')
        self.totalSalary_entry.grid(row=3, column=4, padx=8, pady=5)

        self.Search_entry = Entry(Frame_1, font=('arial', 14), width=20)
        self.Search_entry.grid(row=5, column=4, padx=8, pady=5)

        # ==================================================Frame_2=================================================
        self.Info = Text(Display, width=40, height=10,
                            font=('arial', 14, 'bold'))
        self.Info.grid(row=0, column=0, padx=3)

        self.Imgfrm = Canvas(Image_Frame, width=190, height=220, bg='white')
        self.Imgfrm.grid(row=0, column=0, padx=3)

        # =============================================List box and scrollbar===========================================
        sb = Scrollbar(List_Frame)

        self.treeview = ttk.Treeview(List_Frame,
                                     columns=('', 'MaNV', 'HoTen', 'DiaChi', 'NgSinh', 'TenHinh', 'LoaiNhanVien', 'LuongCoBan', 'LuongHangThang'),
                                     show=["headings"], yscrollcommand=sb.set)
        self.treeview.heading('', text='')
        self.treeview.heading('MaNV', text='Mã NV')
        self.treeview.heading('HoTen', text='Họ Tên')
        self.treeview.heading('DiaChi', text='Địa chỉ')
        self.treeview.heading('NgSinh', text='Ngày sinh')
        self.treeview.heading('TenHinh', text='Hình')
        self.treeview.heading('LoaiNhanVien', text='Loại NV')
        self.treeview.heading('LuongCoBan', text='Lương Cơ Bản')
        self.treeview.heading('LuongHangThang', text='Lương HT')

        self.treeview.column('', width=20, anchor=tk.CENTER)
        self.treeview.column('MaNV', width=50, anchor=tk.CENTER)
        self.treeview.column('HoTen', width=150, anchor=tk.CENTER)
        self.treeview.column('DiaChi', width=320, anchor=tk.CENTER)
        self.treeview.column('NgSinh', width=150, anchor=tk.CENTER)
        self.treeview.column('TenHinh', width=120, anchor=tk.CENTER)
        self.treeview.column('LoaiNhanVien', width=100, anchor=tk.CENTER)
        self.treeview.column('LuongCoBan', width=100, anchor=tk.CENTER)
        self.treeview.column('LuongHangThang', width=100, anchor=tk.CENTER)

        self.treeview.grid(row=7, column=0, columnspan=7)
        sb.grid(row=7, column=6, sticky='ns')
        sb.config(command=self.treeview.yview)

        # ==================================================Buttons=================================================
        self.buttons = {
            "LOAD": tk.Button(Button_Frame, text="  LOAD", font=('arial', 14, 'bold'), width=100),
            "RESET": tk.Button(Button_Frame, text="  RESET", font=('arial', 14, 'bold'), width=115),
            "CALCULATE": tk.Button(Button_Frame, text="  CALCULATE", font=('arial', 14, 'bold'), width=165),
            "DISPLAY": tk.Button(Button_Frame, text="  DISPLAY", font=('arial', 14, 'bold'), width=125),
            "ADD": tk.Button(Button_Frame, text="  ADD", font=('arial', 14, 'bold'), width=100),
            "UPDATE": tk.Button(Button_Frame, text="  UPDATE", font=('arial', 14, 'bold'), width=120),
            "DELETE": tk.Button(Button_Frame, text="  DELETE", font=('arial', 14, 'bold'), width=120),
            "EXIT": tk.Button(Button_Frame, text="  EXIT", font=('arial', 14, 'bold'), width=100),
            "EXPORT": tk.Button(Button_Frame, text="  EXPORT", font=('arial', 14, 'bold'), width=120),
            "UPLOAD": tk.Button(Image_Frame, text="  UPLOAD", font=('arial', 14, 'bold'), width=120),
            "PRINT": tk.Button(Button_Frame, text="  PRINT", font=('arial', 14, 'bold'), width=120),
            "SEARCH": tk.Button(Frame_1, text="", font=('arial', 10, 'bold'), width=30)
        }

        # self.buttons["Load"].grid(row=3, column=0)
        self.buttons["LOAD"].grid(row=0, column=1, padx=5, pady=5)
        self.buttons["RESET"].grid(row=0, column=2, padx=5, pady=5)
        self.buttons["CALCULATE"].grid(row=0, column=3, padx=5, pady=5)
        self.buttons["DISPLAY"].grid(row=0, column=4, padx=5, pady=5)
        self.buttons["ADD"].grid(row=0, column=5, padx=5, pady=5)
        self.buttons["UPDATE"].grid(row=0, column=6, padx=5, pady=5)
        self.buttons["DELETE"].grid(row=0, column=7, padx=5, pady=5)
        self.buttons["EXIT"].grid(row=0, column=8, padx=5, pady=5)
        self.buttons["PRINT"].grid(row=0, column=9, padx=5, pady=5)
        self.buttons["EXPORT"].grid(row=0, column=10, padx=5, pady=5)
        self.buttons["UPLOAD"].grid(row=1, column=0, padx=5, pady=5)
        self.buttons["SEARCH"].grid(row=5, column=5, padx=8, pady=5)


        img = Image.open("LOAD.png")
        img = img.resize((30, 30), Image.LANCZOS)
        img = ImageTk.PhotoImage(img)
        self.buttons["LOAD"].img = img
        self.buttons["LOAD"].config(image=img, compound=LEFT)

        img6 = Image.open("RESET.png")
        img6 = img6.resize((30, 30), Image.LANCZOS)
        img6 = ImageTk.PhotoImage(img6)
        self.buttons["RESET"].img6 = img6
        self.buttons["RESET"].config(image=img6, compound=LEFT)

        img0 = Image.open("CALCULATOR.png")
        img0 = img0.resize((30, 30), Image.LANCZOS)
        img0 = ImageTk.PhotoImage(img0)
        self.buttons["CALCULATE"].img0 = img0
        self.buttons["CALCULATE"].config(image=img0, compound=LEFT)

        img1 = Image.open("DISPLAY.png")
        img1 = img1.resize((30, 30), Image.LANCZOS)
        img1 = ImageTk.PhotoImage(img1)
        self.buttons["DISPLAY"].img1 = img1
        self.buttons["DISPLAY"].config(image=img1, compound=LEFT)

        img2 = Image.open("ADD.png")
        img2 = img2.resize((30, 30), Image.LANCZOS)
        img2 = ImageTk.PhotoImage(img2)
        self.buttons["ADD"].img2 = img2
        self.buttons["ADD"].config(image=img2, compound=LEFT)

        img3 = Image.open("UPDATE.png")
        img3 = img3.resize((30, 30), Image.LANCZOS)
        img3 = ImageTk.PhotoImage(img3)
        self.buttons["UPDATE"].img3 = img3
        self.buttons["UPDATE"].config(image=img3, compound=LEFT)

        ##button delete
        img4 = Image.open("DELETE.png")
        img4 = img4.resize((30, 30), Image.LANCZOS)
        img4 = ImageTk.PhotoImage(img4)
        self.buttons["DELETE"].img4 = img4
        self.buttons["DELETE"].config(image=img4, compound=LEFT)

        img5 = Image.open("EXIT.png")
        img5 = img5.resize((30, 30), Image.LANCZOS)
        img5 = ImageTk.PhotoImage(img5)
        self.buttons["EXIT"].img5 = img5
        self.buttons["EXIT"].config(image=img5, compound=LEFT)

        img7 = Image.open("UPLOAD.png")
        img7 = img7.resize((30, 30), Image.LANCZOS)
        img7 = ImageTk.PhotoImage(img7)
        self.buttons["UPLOAD"].img7 = img7
        self.buttons["UPLOAD"].config(image=img7, compound=LEFT)

        img8 = Image.open("EXPORT.png")
        img8 = img8.resize((30, 30), Image.LANCZOS)
        img8 = ImageTk.PhotoImage(img8)
        self.buttons["EXPORT"].img8 = img8
        self.buttons["EXPORT"].config(image=img8, compound=LEFT)

        img9 = Image.open("SEARCH.png")
        img9 = img9.resize((20, 20), Image.LANCZOS)
        img9 = ImageTk.PhotoImage(img9)
        self.buttons["SEARCH"].img9 = img9
        self.buttons["SEARCH"].config(image=img9, compound=LEFT)

        img10 = Image.open("PRINT.png")
        img10 = img10.resize((20, 20), Image.LANCZOS)
        img10 = ImageTk.PhotoImage(img10)
        self.buttons["PRINT"].img10 = img10
        self.buttons["PRINT"].config(image=img10, compound=LEFT)







