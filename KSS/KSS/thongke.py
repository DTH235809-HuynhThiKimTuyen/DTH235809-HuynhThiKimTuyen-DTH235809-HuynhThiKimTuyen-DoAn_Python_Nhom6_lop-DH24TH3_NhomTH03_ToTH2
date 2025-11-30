import tkinter as tk
from tkinter import ttk
from database import fetch_all


def show():
    win = tk.Toplevel()
    win.title("Báo Cáo Doanh Thu")
    win.geometry("900x500")

    tk.Label(win, text="DANH SÁCH HÓA ĐƠN ĐÃ THANH TOÁN", font=("Arial", 16, "bold"), fg="#2980b9").pack(pady=15)

    # Bảng hiển thị
    cols = ("ID", "Phong", "Khach", "NgayRa", "TienPhong", "TienDV", "Tong")
    tree = ttk.Treeview(win, columns=cols, show="headings")

    tree.heading("ID", text="Mã HĐ");
    tree.column("ID", width=50)
    tree.heading("Phong", text="Phòng");
    tree.column("Phong", width=60)
    tree.heading("Khach", text="Khách Hàng");
    tree.column("Khach", width=150)
    tree.heading("NgayRa", text="Ngày Thanh Toán");
    tree.column("NgayRa", width=120)
    tree.heading("TienPhong", text="Tiền Phòng");
    tree.heading("TienDV", text="Dịch Vụ");
    tree.heading("Tong", text="TỔNG TIỀN");

    tree.pack(fill="both", expand=True, padx=10, pady=10)

    # Load dữ liệu
    rows = fetch_all("SELECT * FROM hoadon ORDER BY MaHD DESC")
    total_revenue = 0

    for r in rows:
        total_revenue += float(r['TongTien'])
        tree.insert("", "end", values=(
            r['MaHD'], r['MaPhong'], r['TenKhach'], str(r['NgayRa'])[:16],
            f"{r['TienPhong']:,.0f}", f"{r['TienDichVu']:,.0f}", f"{r['TongTien']:,.0f}"
        ))

    tk.Label(win, text=f"TỔNG DOANH THU: {total_revenue:,.0f} VNĐ", font=("Arial", 14, "bold"), fg="red",
             bg="#ecf0f1").pack(pady=10, fill="x")