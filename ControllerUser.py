from ViewUser import *

class ControllerUser:
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
        self.view.buttons["EXIT"].config(command=self.exit_btn)

    def exit_btn(self):
       exit()

    def LoadNV(self,maNV):
        result=self.model.layThongTinNhanVien(f"{maNV}")
        self.view.MaNV.set(result['maNV'])
        self.view.name.set(result['hoTen'])
        self.view.Dchi.set(result['diaChi'])
        self.view.NgSinh.set(result['ngSinh'])
        self.view.LuongCB.set(result['luongCoBan'])
        result2 = self.model.layThongTinChamCong(f"{maNV}")
        self.view.LoaiNV.set(result2['loaiNV'])



