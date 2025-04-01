from connectDB import CnnDatabase
from abc import ABC, abstractmethod
import csv
import xlsxwriter
import os
import shutil

class abcNV(ABC):
    @abstractmethod
    def tinhluongHT(self):
        pass

class NV(abcNV):
    def __init__(self, MaNhanVien, HoTen, DiaChi,  NgSinh, TenHinh, LoaiNhanVien, LuongCoBan):
        self._MaNhanVien = MaNhanVien
        self._HoTen = HoTen
        self._DiaChi = DiaChi
        self._NgSinh = NgSinh
        self._TenHinh = TenHinh
        self._LoaiNhanVien = LoaiNhanVien
        self._LuongCoBan = LuongCoBan
        self._LuongHT = 0

    def __str__(self):
        return str([self._MaNhanVien, self._HoTen, self._NgSinh, self._TenHinh, self._LoaiNhanVien, self._LuongCoBan, self._LuongHT])

class NVVP(NV):
    def __init__(self, MaNhanVien, HoTen, DiaChi, NgSinh, TenHinh, LoaiNhanVien, LuongCoBan, SoNgayLam):
        NV.__init__(self, MaNhanVien, HoTen, DiaChi, NgSinh, TenHinh, LoaiNhanVien, LuongCoBan)
        self.__SoNgayLam = SoNgayLam

    def tinhluongHT(self):
        if self.__SoNgayLam is not None:
            luong = self._LuongCoBan + self.__SoNgayLam * 180_000
            self._LuongHT = luong
            return luong
        else:
            return 0

class NVSX(NV):
    def __init__(self, MaNhanVien, HoTen, DiaChi, NgSinh, TenHinh, LoaiNhanVien, LuongCoBan, SoSanPham):
        NV.__init__(self, MaNhanVien, HoTen, DiaChi, NgSinh, TenHinh, LoaiNhanVien, LuongCoBan)
        self.__SoSanPham = SoSanPham

    def tinhluongHT(self):
        if self.__SoSanPham is not None:
            luong = self._LuongCoBan + self.__SoSanPham * 18_000
            self._LuongHT = luong
            return luong
        else:
            return 0
class ModelUser:
    def __init__(self, server, database, username=None, password=None):
        # Kết nối đến SQL Server
        self.ket_noi = CnnDatabase(server, database, username, password)
        self.ds = []
        self.file_path = None

    def loadNV(self):
        try:
            query = """
                SELECT NhanVien.MaNhanVien, HoTen, DiaChi, NgSinh, TenHinh, LoaiNhanVien, LuongCoBan, SoNgayLam, SoSanPham
                FROM NhanVien
                LEFT JOIN ChamCongTongHop ON NhanVien.MaNhanVien = ChamCongTongHop.MaNhanVien
                LEFT JOIN HinhAnh ON NhanVien.MaNhanVien = HinhAnh.MaHinh
            """
            result = self.ket_noi.execute_query(query).fetchall()

            self.ds = []
            for row in result:
                MaNhanVien, HoTen, DiaChi, NgSinh, TenHinh, LoaiNhanVien, LuongCoBan, soNgayLam, soSanPham = row
                if soNgayLam is not None:
                    nv = NVVP(MaNhanVien, HoTen, DiaChi, NgSinh, TenHinh, LoaiNhanVien, LuongCoBan, soNgayLam)
                elif soSanPham is not None:
                    nv = NVSX(MaNhanVien, HoTen, DiaChi, NgSinh, TenHinh, LoaiNhanVien, LuongCoBan, soSanPham)
                else:
                    nv = NV(MaNhanVien, HoTen, DiaChi, NgSinh, TenHinh, LoaiNhanVien, LuongCoBan)
                self.ds.append(nv)

            print("Nạp dữ liệu nhân viên thành công.")
            print("Số lượng nhân viên đã nạp:", len(self.ds))
            for nv in self.ds:
                print(nv)
        except Exception as e:
            print(f"Lỗi khi nạp dữ liệu nhân viên: {e}")

    def tinhluongHT(self):
        try:
            for nv in self.ds:
                nv.tinhluongHT()

            print("Calculate salaries successfully.")

        except Exception as e:
            print(f"Error calculating salaries: {e}")

    def themNhanVien(self, ma_nv, ho_ten, dia_chi, ng_sinh, ten_hinh, luong_co_ban, loai_nv, pass_word=None,
                     so_ngay_lam=0, so_san_pham=0):
        try:
            # Kiểm tra nếu mã nhân viên đã tồn tại
            if self.kiemTraTonTaiMaNhanVien(ma_nv):
                raise ValueError(f"Mã nhân viên {ma_nv} đã tồn tại. Không thể thêm.")

            # Kiểm tra nếu hình ảnh không tồn tại
            if ten_hinh is None:
                raise ValueError("Hình ảnh không tồn tại. Không thể thêm nhân viên.")

            # Thêm vào bảng NhanVien
            query_nhan_vien = "INSERT INTO NhanVien (MaNhanVien, HoTen, DiaChi, NgSinh, LuongCoBan) VALUES (?, ?, ?, ?, ?)"
            self.ket_noi.insert_(query_nhan_vien, (ma_nv, ho_ten, dia_chi, ng_sinh, luong_co_ban))

            # Thêm vào bảng HinhAnh
            query_load_hinh = "INSERT INTO HinhAnh (MaHinh, TenHinh) VALUES (?, ?)"
            self.ket_noi.insert_(query_load_hinh, (ma_nv, ten_hinh))

            # Thêm vào bảng ThongTinLogin
            if pass_word is not None:
                query_login = "INSERT INTO ThongTinLogin (Username, Pass) VALUES (?, ?)"
                self.ket_noi.insert_(query_login, (ma_nv, pass_word))

            # Thêm vào bảng ChamCongTongHop
            query_cham_cong = "INSERT INTO ChamCongTongHop (MaNhanVien, LoaiNhanVien, SoNgayLam, SoSanPham) VALUES (?, ?, ?, ?)"
            self.ket_noi.insert_(query_cham_cong, (ma_nv, loai_nv, so_ngay_lam, so_san_pham))

            # Kiểm tra xem đường dẫn tạm thời của hình ảnh có tồn tại không
            if self.file_path is not None:
                # Lấy đường dẫn đầy đủ của hình ảnh trong thư mục HinhNV
                hinh_nv_path = os.path.join("HinhNV", ten_hinh)

                # Sử dụng shutil.copyfile để sao chép hình ảnh từ đường dẫn tạm thời vào thư mục HinhNV
                shutil.copyfile(self.file_path, hinh_nv_path)

                # Cập nhật xuống cơ sở dữ liệu
            self.ket_noi.commit()

            print(f"Thêm nhân viên {ma_nv} thành công.")
        except Exception as e:
            print(f"Lỗi khi thêm nhân viên {ma_nv}: {e}")

    def layThongTinNhanVien(self, ma_nv):
        try:
            query = "SELECT * FROM NhanVien WHERE MaNhanVien = ?"
            result = self.ket_noi.fetch_one(query, (ma_nv,))
            query2 = "SELECT * FROM ChamCongTongHop WHERE MaNhanVien = ?"
            result2= self.ket_noi.fetch_one(query, (ma_nv,))
            if result and len(result) >= 5:
                return {
                    'maNV': result[0],
                    'hoTen': result[1],
                    'diaChi': result[2],
                    'ngSinh': result[3],
                    'luongCoBan': result[4]
                }
            else:
                raise ValueError(f"Không tìm thấy nhân viên có mã {ma_nv}.")
        except Exception as e:
            print(f"Lỗi khi lấy thông tin nhân viên {ma_nv}: {e}")
            return None

    def layThongTinChamCong(self, ma_nv):
        try:
            query = "SELECT * FROM ChamCongTongHop WHERE MaNhanVien = ?"
            result= self.ket_noi.fetch_one(query, (ma_nv,))
            if result and len(result) >= 4:
                return {
                    'maNV': result[0],
                    'loaiNV': result[1],
                    'soNG': result[2],
                    'soSP': result[3]
                }
            else:
                raise ValueError(f"Không tìm thấy nhân viên có mã {ma_nv}.")
        except Exception as e:
            print(f"Lỗi khi lấy thông tin nhân viên {ma_nv}: {e}")
            return None

    def cap_nhat_nhan_vien(self, ma_nv, ho_ten, dia_chi, ng_sinh, ten_hinh, luong_co_ban, loai_nv, pass_word=None,
                           so_ngay_lam=0, so_san_pham=0):
        try:
            if not self.kiemTraTonTaiMaNhanVien(ma_nv):
                raise ValueError(f"Mã nhân viên {ma_nv} không tồn tại. Không thể cập nhật.")

            # Cập nhật thông tin trong bảng NhanVien
            query_nhan_vien = "UPDATE NhanVien SET HoTen=?, DiaChi=?, NgSinh=?, LuongCoBan=? WHERE MaNhanVien=?"
            self.ket_noi.update(query_nhan_vien, (ho_ten, dia_chi, ng_sinh, luong_co_ban, ma_nv))

            # Cập nhật thông tin trong bảng HinhAnh
            query_load_hinh = "UPDATE HinhAnh SET TenHinh=? WHERE MaHinh=?"
            self.ket_noi.update(query_load_hinh, (ten_hinh, ma_nv))

            # Cập nhật thông tin trong bảng ThongTinLogin
            if pass_word is not None:
                query_login = "UPDATE ThongTinLogin SET Pass=? WHERE Username=?"
                self.ket_noi.update(query_login, (pass_word, ma_nv))

            # Cập nhật thông tin trong bảng ChamCongTongHop
            query_cham_cong = "UPDATE ChamCongTongHop SET LoaiNhanVien=?, SoNgayLam=?, SoSanPham=? WHERE MaNhanVien=?"
            self.ket_noi.update(query_cham_cong, (loai_nv, so_ngay_lam, so_san_pham, ma_nv))

            # Cập nhật xuống cơ sở dữ liệu
            self.ket_noi.commit()

            print(f"Cập nhật nhân viên {ma_nv} thành công.")
        except Exception as e:
            print(f"Lỗi khi cập nhật nhân viên {ma_nv}: {e}")

    def xoaNhanVien(self, ma_nv):
        try:
            # Check if the employee exists
            if not self.kiemTraTonTaiMaNhanVien(ma_nv):
                raise ValueError(f"Không tìm thấy nhân viên có mã {ma_nv}. Không thể xóa.")

            # Delete the employee's image from the HinhAnh table
            query_hinh_anh = "DELETE FROM HinhAnh WHERE MaHinh=?"
            self.ket_noi.delete(query_hinh_anh, (ma_nv,))

            # Delete the employee's login information from the ThongTinLogin table
            query_login = "DELETE FROM ThongTinLogin WHERE Username=?"
            self.ket_noi.delete(query_login, (ma_nv,))

            # Delete the employee's attendance/production record from the ChamCongTongHop table
            query_cham_cong = "DELETE FROM ChamCongTongHop WHERE MaNhanVien=?"
            self.ket_noi.delete(query_cham_cong, (ma_nv,))

            # Delete the employee from the NhanVien table
            query_nhan_vien = "DELETE FROM NhanVien WHERE MaNhanVien=?"
            self.ket_noi.delete(query_nhan_vien, (ma_nv,))

            # Commit the changes to the database
            self.ket_noi.commit()

            print(f"Xóa nhân viên {ma_nv} thành công.")
        except Exception as e:
            print(f"Lỗi khi xóa nhân viên {ma_nv}: {e}")

    def kiemTraTonTaiMaNhanVien(self, ma_nv):
        query = "SELECT COUNT(*) FROM NhanVien WHERE MaNhanVien = ?"
        result = self.ket_noi.fetch_one(query, (ma_nv,))
        return result[0] > 0 if result else False
    def themCotLuongHangThang(self):
        try:
            # Thêm cột LuongHangThang vào bảng NhanVien
            add_column_query = """
                ALTER TABLE NhanVien
                ADD LuongHangThang DECIMAL(10, 2)
            """
            self.ket_noi.execute_query(add_column_query)
            self.ket_noi.commit()
            print("Column 'LuongHangThang' Thêm thành công.")

        except Exception as e:
            print(f"Error adding column 'LuongHangThang': {e}")

    def capNhatLuongHangThang(self):
        try:
            # Cập nhật giá trị của cột LuongHangThang
            for nv in self.ds:
                maNV = nv._MaNhanVien
                luong = nv._LuongHT

                update_query = f"""
                    UPDATE NhanVien
                    SET LuongHangThang = {luong}
                    WHERE MaNhanVien = '{maNV}'
                """
                self.ket_noi.execute_query(update_query)
                self.ket_noi.commit()

            print("Update 'LuongHangThang' successfully.")

        except Exception as e:
            print(f"Error updating 'LuongHangThang': {e}")

    def xuatThongTinNhanVienRaFile(self, file_path, file_format='csv'):
        try:
            if file_format == 'csv':
                self.xuatCSV(file_path)
            elif file_format == 'xlsx':
                self.xuatExcel(file_path)
            else:
                raise ValueError("Định dạng file không hỗ trợ.")
        except Exception as e:
            print(f"Lỗi khi xuất thông tin nhân viên ra file: {e}")

    def xuatCSV(self, file_path):
        with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
            csv_writer = csv.writer(csvfile)
            header = ['Mã NV', 'Họ tên', 'Địa chỉ', 'Ngày sinh', 'Hình', 'Lương cơ bản', 'Lương hàng tháng']
            csv_writer.writerow(header)

            for nv in self.ds:
                row = [nv._MaNhanVien, nv._HoTen, nv._DiaChi, nv._NgSinh, nv._TenHinh, nv._LuongCoBan, nv._LuongHT]
                csv_writer.writerow(row)

    def xuatExcel(self, file_path):
        workbook = xlsxwriter.Workbook(file_path)
        worksheet = workbook.add_worksheet()

        # Ghi header
        header_format = workbook.add_format({'bold': True, 'align': 'center', 'valign': 'vcenter'})
        header = ['Mã NV', 'Họ tên', 'Địa chỉ', 'Ngày sinh', 'Hình', 'Lương cơ bản', 'Lương hàng tháng']
        for col_num, col_value in enumerate(header):
            worksheet.write(0, col_num, col_value, header_format)

        # Ghi dữ liệu
        for row_num, nv in enumerate(self.ds, start=1):
            worksheet.write(row_num, 0, nv._MaNhanVien)
            worksheet.write(row_num, 1, nv._HoTen)
            worksheet.write(row_num, 2, nv._DiaChi)
            worksheet.write(row_num, 3, nv._NgSinh)
            worksheet.write(row_num, 4, nv._TenHinh)
            worksheet.write(row_num, 5, nv._LuongCoBan)
            worksheet.write(row_num, 6, nv._LuongHT)

        workbook.close()

    def layDuongDanHinhNhanVien(self, tenHinh):
        thu_muc_hinh = "HinhNV"
        duong_dan_day_du = os.path.join(thu_muc_hinh, tenHinh)

        if os.path.exists(duong_dan_day_du):
            return duong_dan_day_du
        else:
            print(f"Tệp hình ảnh '{tenHinh}' không tồn tại trong thư mục '{thu_muc_hinh}'.")
            return None

    def print(self):
        """In toàn bộ DS"""
        for nv in self.ds:
            print(nv)

server = 'LAPTOPSN\SQLEXPRESST'
database = 'qlnv'
ct = ModelUser(server, database)
ct.loadNV()
ct.tinhluongHT()
ct.themCotLuongHangThang()
ct.capNhatLuongHangThang()
ct.print()
