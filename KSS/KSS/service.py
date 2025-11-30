import tkinter as tk
from tkinter import ttk, messagebox
from database import fetch_all, execute_query

def show():
    win = tk.Toplevel()
    win.title("Dịch Vụ Phòng")
    win.geometry("600x500")

    tk.Label(win, text="THÊM DỊCH VỤ", font=("Arial", 16, "bold"), fg="#e67e22").pack(pady=10)
    frm = tk.Frame(win); frm.pack()

    # Chỉ lấy phòng Đang Có Khách
    tk.Label(frm, text="Phòng đang ở:").grid(row=0, column=0)
    cbo_phong = ttk.Combobox(frm, state="readonly", width=30)
    cbo_phong.grid(row=0, column=1)

    stays = fetch_all("SELECT p.MaPhong, d.MaDP, d.TenKhach FROM phong p JOIN datphong d ON p.MaPhong=d.MaPhong WHERE p.TrangThai='CoKhach'")
    stay_map = {f"P{r['MaPhong']} - {r['TenKhach']}": r['MaDP'] for r in stays}
    cbo_phong['values'] = list(stay_map.keys())

    tk.Label(frm, text="Chọn món:").grid(row=1, column=0)
    cbo_dv = ttk.Combobox(frm, state="readonly", width=30)
    cbo_dv.grid(row=1, column=1)

    dvs = fetch_all("SELECT * FROM dichvu")
    dv_map = {f"{r['TenDV']} ({r['DonGia']:,.0f}đ)": r['MaDV'] for r in dvs}
    cbo_dv['values'] = list(dv_map.keys())

    tk.Label(frm, text="Số lượng:").grid(row=2, column=0)
    sp_sl = tk.Spinbox(frm, from_=1, to=20, width=5); sp_sl.grid(row=2, column=1)

    # Bảng hiển thị lịch sử gọi món
    tree = ttk.Treeview(win, columns=("Ten", "SL", "Gia"), show="headings", height=8)
    tree.heading("Ten", text="Dịch Vụ"); tree.heading("SL", text="SL"); tree.heading("Gia", text="Thành Tiền")
    tree.pack(fill="both", expand=True, padx=10, pady=10)

    def load_ls(ma_dp):
        tree.delete(*tree.get_children())
        sql = "SELECT d.TenDV, s.SoLuong, (d.DonGia*s.SoLuong) as T FROM sudungdv s JOIN dichvu d ON s.MaDV=d.MaDV WHERE s.MaDP=%s"
        for r in fetch_all(sql, (ma_dp,)):
            tree.insert("", "end", values=(r['TenDV'], r['SoLuong'], f"{r['T']:,.0f}"))

    def them():
        if not cbo_phong.get() or not cbo_dv.get(): return
        mdp = stay_map[cbo_phong.get()]
        mdv = dv_map[cbo_dv.get()]
        execute_query("INSERT INTO sudungdv(MaDP, MaDV, SoLuong) VALUES(%s,%s,%s)", (mdp, mdv, sp_sl.get()))
        messagebox.showinfo("OK", "Đã gọi món!")
        load_ls(mdp)

    tk.Button(frm, text="Gọi Món", bg="orange", command=them).grid(row=3, columnspan=2, pady=10)
    cbo_phong.bind("<<ComboboxSelected>>", lambda e: load_ls(stay_map[cbo_phong.get()]))