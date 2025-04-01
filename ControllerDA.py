from reportlab.pdfgen import canvas

from connectDB import CnnDatabase
from tkinter import messagebox, filedialog
import tkinter as tk
from PIL import Image, ImageTk
import os
from shutil import copyfile
import subprocess
import win32print
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import letter

class ControllerDA:
    def __init__(self, view, model, server, database, username=None, password=None):
        self.view = view
        self.model = model
        super().__init__()
        self.base_name = ""
        self.file_extension = ""
        self.ma_hinh = None
        self.file_path = None

        self.ket_noi = CnnDatabase(server, database, username, password)
        self.ds = []
        self.view.buttons["LOAD"].config(command=self.load_nhan_vien_callback)
        self.view.buttons["CALCULATE"].config(command=self.tinh_luong_hang_thang)
        self.view.buttons["ADD"].config(command=self.them_nhan_vien_callback)
        self.view.buttons["RESET"].config(command=self.reset_callback)
        self.view.buttons["DISPLAY"].config(command=self.display_btn)
        self.view.buttons["EXIT"].config(command=self.exit_btn)
        self.view.buttons["UPLOAD"].config(command=self.upload_image)
        self.view.treeview.bind('<ButtonRelease-1>', self.on_treeview_select)
        self.view.buttons["UPDATE"].config(command=self.update_nhan_vien_callback)
        self.view.buttons["DELETE"].config(command=self.delete_nhan_vien_callback)
        self.view.buttons["EXPORT"].config(command=self.xuat_thong_tin_nhan_vien_callback)
        self.view.buttons["SEARCH"].config(command=self.perform_search)
        self.view.buttons["PRINT"].config(command=self.PRINT_btn)

    def PRINT_btn(self):
        # Lấy dữ liệu từ Treeview
        data = []
        for item in self.view.treeview.get_children():
            data.append(self.view.treeview.item(item, 'values'))

        # Mở hộp thoại in và chờ người dùng chọn máy in và tùy chọn in
        print_dialog = win32print.GetDefaultPrinter()
        handle = win32print.OpenPrinter(print_dialog)

        try:
            # Tạo tệp PDF và thiết lập font
            pdf_filename = "bao_cao_nhan_vien.pdf"
            pdf_canvas = canvas.Canvas(pdf_filename, pagesize=letter,
                                       bottomup=0)  # Chuyển bottomup=0 để điều chỉnh hệ thống lên

            # Sử dụng font mặc định không cần cài đặt
            pdfmetrics.registerFont(TTFont('defaultFont', 'arial.ttf'))
            pdf_canvas.setFont('defaultFont', 12)

            # Bắt đầu tài liệu in
            win32print.StartDocPrinter(handle, 1, ("Báo cáo Nhân viên", None, "RAW"))

            try:
                # Bắt đầu trang in
                win32print.StartPagePrinter(handle)

                # Tính toán chiều cao của trang
                page_height = pdf_canvas._pagesize[1]

                # Tính toán chiều cao của mỗi dòng và khoảng cách giữa chúng
                line_height = 14
                total_height = len(data) * line_height
                gap = (page_height - total_height) / 2

                # Bắt đầu vẽ dữ liệu
                y_position = page_height - gap  # Bắt đầu từ phía trên cùng của trang
                for row in data:
                    for item in row:
                        pdf_canvas.drawString(100, y_position, str(item))
                        y_position -= line_height

                # Kết thúc trang in
                win32print.EndPagePrinter(handle)

            finally:
                # Kết thúc tài liệu in
                win32print.EndDocPrinter(handle)

                # Đóng tệp PDF
                pdf_canvas.save()

        finally:
            # Đóng máy in
            win32print.ClosePrinter(handle)

            # Mở tệp PDF
            subprocess.run(["start", "", pdf_filename], shell=True)
    def perform_search(self):
        try:
            # Xóa hết các dòng hiện tại trong Treeview
            for row in self.view.treeview.get_children():
                self.view.treeview.delete(row)

            # Lấy từ khóa tìm kiếm
            search_text = self.view.Search_entry.get().lower()

            # Lọc dữ liệu và hiển thị kết quả trong Treeview
            for index, nv in enumerate(self.model.ds, start=1):
                if (
                        search_text in nv._MaNhanVien.lower()
                        or search_text in nv._HoTen.lower()
                        or search_text in nv._DiaChi.lower()
                        or (isinstance(nv._NgSinh, str) and search_text in nv._NgSinh.lower())
                        or search_text in nv._TenHinh.lower()
                        or search_text in nv._LoaiNhanVien.lower()
                        or search_text in str(nv._LuongCoBan).lower()
                        or search_text in str(nv._LuongHT).lower()
                ):
                    self.view.treeview.insert('', 'end', values=(
                        index, nv._MaNhanVien, nv._HoTen, nv._DiaChi, nv._NgSinh, nv._TenHinh, nv._LoaiNhanVien,
                        nv._LuongCoBan, nv._LuongHT))
        except Exception as e:
            print(f"Error in perform_search: {e}")

    def on_treeview_select(self, event):
        print("Treeview selected!")
        selected_items = self.view.treeview.selection()

        if selected_items:
            selected_item = selected_items[0]
            values = self.view.treeview.item(selected_item, 'values')

            if values and len(values) >= 5:
                self.view.IDnv.set(values[1] if values[1] else '')  # Mã NV
                self.view.name.set(values[2] if values[2] else '')  # Họ tên
                self.view.place.set(values[3] if values[3] else '')  # Địa chỉ
                self.view.date.set(values[4] if values[4] else '')  # Ngày sinh
                self.view.LoaiNV.set(values[6] if values[6] else '')  # Loại NV
                self.view.salaryCB.set(values[7] if values[7] else '')  # Lương cơ bản
                self.view.totalSalary.set(values[8] if values[8] else '')  # Lương hàng tháng

                ten_hinh = values[5] if values[5] else ''
                self.display_image(ten_hinh)
            else:
                self.view.IDnv.set('')
                self.view.name.set('')
                self.view.place.set('')
                self.view.date.set('')
                self.view.salaryCB.set('')
                self.view.LoaiNV.set('')
                self.view.totalSalary.set(0)

    def display_image(self, ten_hinh):
        try:
            duong_dan_day_du = self.model.layDuongDanHinhNhanVien(ten_hinh)

            if duong_dan_day_du:
                img = Image.open(duong_dan_day_du)

                # Lấy chiều rộng và chiều cao của tiện ích Canvas
                canvas_width = self.view.Imgfrm.winfo_reqwidth()
                canvas_height = self.view.Imgfrm.winfo_reqheight()

                # Tính tỷ lệ khung hình của ảnh
                aspect_ratio = img.width / img.height

                # Tính chiều rộng và chiều cao mới để vừa với Canvas và vẫn giữ tỷ lệ khung hình
                if canvas_width / aspect_ratio < canvas_height:
                    new_width = int(canvas_width)
                    new_height = int(canvas_width / aspect_ratio)
                else:
                    new_width = int(canvas_height * aspect_ratio)
                    new_height = int(canvas_height)

                # Thay đổi kích thước ảnh
                img = img.resize((new_width, new_height), Image.ANTIALIAS)

                # Tạo một PhotoImage từ ảnh đã thay đổi kích thước
                photo = ImageTk.PhotoImage(img)

                # Cấu hình Canvas với ảnh mới
                self.view.Imgfrm.config(width=new_width, height=new_height)
                self.view.Imgfrm.create_image(new_width // 2, new_height // 2, anchor="center", image=photo)
                self.view.Imgfrm.photo = photo
        except Exception as e:
            print(f"Lỗi khi hiển thị hình ảnh: {e}")

    def reset_callback(self):
        self.view.IDnv.set('')
        self.view.name.set('')
        self.view.place.set('')
        self.view.date.set('')
        self.view.salaryCB.set('')
        self.view.LoaiNV.set('')
        self.view.totalSalary.set('')
        # Remove the image from Imgfrm
        self.view.Imgfrm.config(image=None)
        self.view.Imgfrm.photo = None

        self.view.Info.delete(1.0, tk.END)
    def exit_btn(self):
        exit()

    def upload_image(self):
        try:
            self.file_path = filedialog.askopenfilename(
                title="Chọn hình ảnh",
                filetypes=[("Tệp hình ảnh", "*.png;*.jpg;*.jpeg")]
            )

            if self.file_path:
                img = Image.open(self.file_path)

                # Lấy chiều rộng và chiều cao của tiện ích Canvas
                canvas_width = self.view.Imgfrm.winfo_reqwidth()
                canvas_height = self.view.Imgfrm.winfo_reqheight()

                # Tính tỷ lệ khung hình của ảnh
                aspect_ratio = img.width / img.height

                # Tính chiều rộng và chiều cao mới để vừa với Canvas và vẫn giữ tỷ lệ khung hình
                if canvas_width / aspect_ratio < canvas_height:
                    new_width = int(canvas_width)
                    new_height = int(canvas_width / aspect_ratio)
                else:
                    new_width = int(canvas_height * aspect_ratio)
                    new_height = int(canvas_height)

                # Thay đổi kích thước ảnh
                img = img.resize((new_width, new_height), Image.ANTIALIAS)

                # Tạo một PhotoImage từ ảnh đã thay đổi kích thước
                photo = ImageTk.PhotoImage(img)

                # Cấu hình Canvas với ảnh mới
                self.view.Imgfrm.config(width=new_width, height=new_height)
                self.view.Imgfrm.create_image(new_width // 2, new_height // 2, anchor="center", image=photo)
                self.view.Imgfrm.photo = photo
                self.view.Imgfrm.image = img

                file_name = os.path.basename(self.file_path)
                self.base_name, self.file_extension = os.path.splitext(file_name)  # Cập nhật ở cấp độ của lớp

                # Hiển thị trong info
                self.view.Info.delete(1.0, tk.END)
                self.view.Info.insert(tk.END,
                                      f"Tên hình ảnh: {self.base_name}{self.file_extension}\n\nĐường dẫn hình ảnh: {self.file_path}")

        except Exception as e:
            print(e)

    def get_image_info(self):
        result = f"{self.base_name}{self.file_extension}"
        print(f"Đã nhận được thông tin hình ảnh: {result}")
        return result
    def display_btn(self):
        print("display clicked!")
        selected_items = self.view.treeview.selection()

        if selected_items:
            selected_item = selected_items[0]
            values = self.view.treeview.item(selected_item, 'values')

            # Lấy thông tin từ dòng được chọn và hiển thị trên Frame 2
            if values and len(values) >= 5:
                info_text = f"Chi tiết:\n\nMã NV: {values[1]}\nHọ tên: {values[2]}\nĐịa chỉ: {values[3]}\nNgày sinh: {values[4]}\nHình: {values[5]}\nLoại nhân viên: {values[6]}\nLương cơ bản: {values[7]}\nLương hàng tháng: {values[7]}"
                self.view.Info.delete('1.0', tk.END)
                self.view.Info.insert(tk.END, info_text)
            else:
                messagebox.showwarning("Thông báo", "Vui lòng chọn một nhân viên trước khi hiển thị thông tin.")
        else:
            messagebox.showwarning("Thông báo", "Vui lòng chọn một nhân viên trước khi hiển thị thông tin.")

    def load_nhan_vien_callback(self):
        try:
            # Load Nhân viên từ cơ sở dữ liệu
            self.model.loadNV()

            # Xóa dữ liệu cũ trong Treeview (nếu có)
            for row in self.view.treeview.get_children():
                self.view.treeview.delete(row)

            # Hiển thị dữ liệu mới trong Treeview
            for index, nv in enumerate(self.model.ds, start=1):
                self.view.treeview.insert('', 'end', values=(index, nv._MaNhanVien, nv._HoTen, nv._DiaChi, nv._NgSinh, nv._TenHinh, nv._LoaiNhanVien, nv._LuongCoBan, nv._LuongHT))

            # Cập nhật dữ liệu trong Treeview
            self.cap_nhat_du_lieu_treeview()

            messagebox.showinfo("Thành công", "Load Nhân viên thành công.")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Error: {e}")

    def tinh_luong_hang_thang(self):
        try:
            # Tính lương hàng tháng
            self.model.tinhluongHT()

            # Cập nhật dữ liệu trong Treeview sau khi tính lương
            for row in self.view.treeview.get_children():
                self.view.treeview.delete(row)

            for index, nv in enumerate(self.model.ds, start=1):
                self.view.treeview.insert('', 'end', values=(index, nv._MaNhanVien, nv._HoTen, nv._DiaChi, nv._NgSinh, nv._TenHinh, nv._LoaiNhanVien, nv._LuongCoBan, nv._LuongHT))

            messagebox.showinfo("Thành công", "Tính lương hàng tháng thành công.")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Error: {e}")

    def cap_nhat_du_lieu_treeview(self):
        print("Cập nhật dữ liệu trong Treeview")
        # Xóa dữ liệu cũ trong Treeview
        for row in self.view.treeview.get_children():
            self.view.treeview.delete(row)

        # Hiển thị dữ liệu mới trong Treeview
        for index, nv in enumerate(self.model.ds, start=1):
            print(
                f"Thêm dữ liệu mới vào Treeview: {nv._MaNhanVien}, {nv._HoTen},{nv._DiaChi}, {nv._NgSinh}, {nv._TenHinh}, {nv._LoaiNhanVien}, {nv._LuongCoBan}, {nv._LuongHT}")
            self.view.treeview.insert('', 'end', values=(
            index, nv._MaNhanVien, nv._HoTen, nv._DiaChi, nv._NgSinh, nv._TenHinh, nv._LoaiNhanVien, nv._LuongCoBan, nv._LuongHT))

    def them_nhan_vien_callback(self):
        try:
            maNV = self.view.IDnv_entry.get()
            hoTen = self.view.name_entry.get()
            diaChi = self.view.place_entry.get()
            ngSinh = self.view.Date_entry.get()
            tenHinh = self.get_image_info()  # Gán giá trị cho tenHinh
            luongCoBan = float(self.view.salaryCB_entry.get())
            loaiNV = self.view.LoaiNV_entry.get()

            # Kiểm tra xem nhân viên với mã đã tồn tại hay chưa
            if self.model.kiemTraTonTaiMaNhanVien(maNV):
                messagebox.showwarning("Cảnh báo", f"Nhân viên với mã {maNV} đã tồn tại.")
                return

            if self.view.LoaiNV_entry.get() == "Văn Phòng":
                loaiNV = "Văn Phòng"
            elif self.view.LoaiNV_entry.get() == "Bán Hàng":
                loaiNV = "Bán Hàng"
            elif self.view.LoaiNV_entry.get() == "Admin":
                loaiNV = "Admin"
            elif self.view.LoaiNV_entry.get() == " ":
                loaiNV = "Không Loại"

                # Lấy thông tin hình cũ từ cơ sở dữ liệu
                query_hinh_cu = "SELECT TenHinh FROM HinhAnh WHERE MaHinh = ?"
                result = self.ket_noi.select(query_hinh_cu, (maNV,))

                # Kiểm tra xem có đường dẫn ảnh mới không
                if self.file_path is not None:
                    # Lấy tên file của ảnh mới
                    new_image_name = f"{maNV}{os.path.splitext(os.path.basename(self.file_path))[1]}"

                    # Lấy đường dẫn đầy đủ của ảnh mới trong thư mục HinhNV
                    hinh_nv_path = os.path.join("HinhNV", new_image_name)

                    print(f"Đường dẫn ảnh mới: {hinh_nv_path}")

                    # Xóa ảnh cũ nếu tồn tại
                    if result and result[0][0] != new_image_name:
                        old_image_path = os.path.join("HinhNV", result[0][0])
                        if os.path.exists(old_image_path):
                            os.remove(old_image_path)
                            print("Đã xóa ảnh cũ thành công")
                        else:
                            print("Không tìm thấy ảnh cũ")
                    else:
                        print("Không cần xóa ảnh cũ")

                    # Sử dụng shutil.copyfile để sao chép ảnh mới từ đường dẫn tạm thời vào thư mục HinhNV
                    copyfile(self.file_path, hinh_nv_path)

                    # Cập nhật tên ảnh mới vào biến tenHinh
                    tenHinh = new_image_name
                else:
                    tenHinh = result[0][0] if result else ''

            # Thêm nhân viên bằng cách gọi hàm themNhanVien
            self.model.themNhanVien(maNV, hoTen, diaChi, ngSinh, tenHinh, luongCoBan, loaiNV)

            # Load lại dữ liệu sau khi thêm Nhân viên
            self.load_nhan_vien_callback()

            # Cập nhật dữ liệu trong Treeview
            self.cap_nhat_du_lieu_treeview()
            # Cập nhật xuống cơ sở dữ liệu
            self.model.ket_noi.commit()

            messagebox.showinfo("Thành công", "Thêm nhân viên thành công.")
        except Exception as e:
            self.ket_noi.rollback()  # Rollback changes if an error occurs
            messagebox.showerror("Lỗi", f"Error: {e}")
            print(f"Lỗi khi thêm nhân viên {maNV}: {e}")

    def update_nhan_vien_callback(self):
        try:
            # Get the selected item from the Treeview
            selected_item = self.view.treeview.selection()

            # Ensure that an item is selected
            if not selected_item:
                messagebox.showwarning("Cảnh báo", "Vui lòng chọn một nhân viên để cập nhật.")
                return

            # Lấy thông tin từ giao diện người dùng
            maNV = self.view.IDnv_entry.get()
            hoTen = self.view.name_entry.get()
            diaChi = self.view.place_entry.get()
            ngSinh = self.view.Date_entry.get()
            luongCoBan = float(self.view.salaryCB_entry.get())
            loaiNV = self.view.LoaiNV_entry.get()
            tenHinh = self.get_image_info()

            if not self.model.kiemTraTonTaiMaNhanVien(maNV):
                raise ValueError(f"Mã nhân viên {maNV} không tồn tại. Không thể cập nhật.")

            if self.view.LoaiNV_entry.get() == "Văn Phòng":
                loaiNV = "Văn Phòng"
            elif self.view.LoaiNV_entry.get() == "Bán Hàng":
                loaiNV = "Bán Hàng"
            elif self.view.LoaiNV_entry.get() == "Admin":
                loaiNV = "Admin"
            elif self.view.LoaiNV_entry.get() == " ":
                loaiNV = "Không Loại"

            # Lấy thông tin hình cũ từ cơ sở dữ liệu
            query_hinh_cu = "SELECT TenHinh FROM HinhAnh WHERE MaHinh = ?"
            result = self.ket_noi.select(query_hinh_cu, (maNV,))

            # Kiểm tra xem có đường dẫn ảnh mới không
            if self.file_path is not None:
                # Lấy tên file của ảnh mới
                new_image_name = f"{maNV}{os.path.splitext(os.path.basename(self.file_path))[1]}"

                # Lấy đường dẫn đầy đủ của ảnh mới trong thư mục HinhNV
                hinh_nv_path = os.path.join("HinhNV", new_image_name)

                print(f"Đường dẫn ảnh mới: {hinh_nv_path}")

                # Xóa ảnh cũ nếu tồn tại
                if result and result[0][0] != new_image_name:
                    old_image_path = os.path.join("HinhNV", result[0][0])
                    if os.path.exists(old_image_path):
                        os.remove(old_image_path)
                        print("Đã xóa ảnh cũ thành công")
                    else:
                        print("Không tìm thấy ảnh cũ")
                else:
                    print("Không cần xóa ảnh cũ")

                # Sử dụng shutil.copyfile để sao chép ảnh mới từ đường dẫn tạm thời vào thư mục HinhNV
                copyfile(self.file_path, hinh_nv_path)

                # Cập nhật tên ảnh mới vào biến tenHinh
                tenHinh = new_image_name
            else:
                tenHinh = result[0][0] if result else ''

            # Gọi hàm cập nhật nhân viên
            self.model.cap_nhat_nhan_vien(maNV, hoTen, diaChi, ngSinh, tenHinh, luongCoBan, loaiNV)

            self.model.tinhluongHT()

            # Load lại dữ liệu sau khi cập nhật Nhân viên
            self.load_nhan_vien_callback()

            # Cập nhật dữ liệu trong Treeview
            self.cap_nhat_du_lieu_treeview()

            messagebox.showinfo("Thành công", "Cập nhật nhân viên thành công.")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Error: {e}")
            print(f"Lỗi khi cập nhật nhân viên {maNV}: {e}")
    def delete_nhan_vien_callback(self):
        # Lấy mã nhân viên từ dòng được chọn trong Treeview
        selected_item = self.view.treeview.selection()
        if not selected_item:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một nhân viên để xóa.")
            return

        selected_values = self.view.treeview.item(selected_item, 'values')
        if selected_values and len(selected_values) >= 2:
            maNV = selected_values[1]

            # Gọi hàm xóa nhân viên từ Model
            self.model.xoaNhanVien(maNV)

            # Xóa dòng khỏi Treeview
            self.view.treeview.delete(selected_item)

            messagebox.showinfo("Thành công", f"Xóa nhân viên {maNV} thành công.")
        else:
            messagebox.showwarning("Cảnh báo", "Không tìm thấy mã nhân viên để xóa.")

    def xuat_thong_tin_nhan_vien_callback(self):
        try:
            # Hiển thị hộp thoại lưu file để người dùng chọn nơi lưu file
            file_path = filedialog.asksaveasfilename(defaultextension=".csv",
                                                       filetypes=[("CSV Files", "*.csv"), ("Excel Files", "*.xlsx")])

            if file_path:
                # Lấy đuôi mở rộng của file để xác định định dạng
                file_format = file_path.split('.')[-1]

                # Gọi hàm xuất thông tin nhân viên từ Model
                self.model.xuatThongTinNhanVienRaFile(file_path, file_format)

                messagebox.showinfo("Thành công", f"Xuất thông tin nhân viên ra file {file_path} thành công.")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Error: {e}")
            print(f"Lỗi khi xuất thông tin nhân viên: {e}")