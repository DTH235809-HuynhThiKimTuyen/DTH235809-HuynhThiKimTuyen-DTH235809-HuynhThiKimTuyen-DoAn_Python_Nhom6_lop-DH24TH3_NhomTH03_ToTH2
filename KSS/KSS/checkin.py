import tkinter as tk
from tkinter import ttk, messagebox
from database import fetch_all, execute_query


# Hàm này bắt buộc phải có tên là 'show' và nhận 1 tham số (callback_refresh)
def show(callback_refresh):
    win = tk.Toplevel()
    win.title("Check-in (Nhận Phòng)")
    win.geometry("500x400")

    tk.Label(win, text="KHÁCH NHẬN PHÒNG", font=("Arial", 16, "bold"), fg="#27ae60").pack(pady=15)
    frm = tk.Frame(win);
    frm.pack(pady=10)

    # Chỉ lấy phòng Trống
    tk.Label(frm, text="Chọn Phòng:").grid(row=0, column=0, pady=5)
    cbo = ttk.Combobox(frm, state="readonly", width=25)
    cbo.grid(row=0, column=1, pady=5)

    # Load danh sách phòng trống từ database
    phongs = fetch_all("SELECT MaPhong, LoaiPhong, GiaNgay FROM phong WHERE TrangThai='Trong'")

    # Tạo dictionary để ánh xạ "Tên hiển thị" -> "Mã phòng"
    p_map = {f"P{r['MaPhong']} ({r['LoaiPhong']})": r['MaPhong'] for r in phongs}
    cbo['values'] = list(p_map.keys())

    tk.Label(frm, text="Tên Khách:").grid(row=1, column=0, pady=5)
    e_ten = tk.Entry(frm, width=28);
    e_ten.grid(row=1, column=1, pady=5)

    tk.Label(frm, text="CCCD/CMND:").grid(row=2, column=0, pady=5)
    e_cccd = tk.Entry(frm, width=28);
    e_cccd.grid(row=2, column=1, pady=5)

    def luu():
        # Kiểm tra nhập liệu
        if not cbo.get() or not e_ten.get():
            messagebox.showwarning("Thiếu thông tin", "Vui lòng chọn phòng và nhập tên khách!")
            return

        # Lấy mã phòng từ combobox
        mp = p_map[cbo.get()]

        # Thêm vào bảng đặt phòng
        sql = "INSERT INTO datphong (MaPhong, TenKhach, CCCD, NgayVao) VALUES (%s, %s, %s, NOW())"
        if execute_query(sql, (mp, e_ten.get(), e_cccd.get())):
            # Cập nhật trạng thái phòng thành 'CoKhach'
            execute_query("UPDATE phong SET TrangThai='CoKhach' WHERE MaPhong=%s", (mp,))

            messagebox.showinfo("Thành công", "Check-in thành công!")

            # Gọi hàm làm mới giao diện bên main.py (đổi màu phòng sang đỏ)
            callback_refresh()
            win.destroy()

    tk.Button(win, text="XÁC NHẬN", bg="green", fg="white", font=("Arial", 10, "bold"), command=luu).pack(pady=10)