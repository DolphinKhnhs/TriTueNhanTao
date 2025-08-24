bang_diem = { 
     1112233: {"Tin ky thuat": 9.2, "An toan dien": 8.9, "The duc": 4.1}, 
     1112244: {"Tin ky thuat": 3.7, "The duc": 9.0, "Toan1": 4.9},
     1112255: {"Nhap mon Lap Trinh": 7.0, "Dai so Tuyen Tinh": 5.0, "Thuong mai dien tu": 9.0} 
}

def diem_duoi_5(MSV):
     if MSV in bang_diem:
          monhoc = bang_diem[MSV]
          for tenmon, diem in monhoc.items():
               if diem < 5:
                    print(f"MSV: {MSV}, Môn: {tenmon}, Điểm: {diem}")
     else:
          print ("Ma sinh vien khong ton tai")

diem_duoi_5(1112233)
diem_duoi_5(1112244)
diem_duoi_5(1112255)
