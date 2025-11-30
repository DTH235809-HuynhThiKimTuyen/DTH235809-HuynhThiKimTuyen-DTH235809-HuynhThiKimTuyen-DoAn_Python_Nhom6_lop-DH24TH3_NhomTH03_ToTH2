import tkinter as tk
from tkinter import ttk, messagebox
from database import fetch_all, execute_query
from datetime import datetime


def show(callback_refresh):
    win = tk.Toplevel()
    win.title("Thanh Toán & Trả Phòng")
    win.geometry("700x650")

    tk.Label(win, text="HÓA ĐƠN THANH TOÁN", font=("Arial", 18, "bold"), fg="#c0392b").pack(pady=10)

    frm = tk.Frame(win);
    frm.pack()
    tk.Label(frm, text="Chọn Phòng Trả:").pack(side="left")
    cbo = ttk.Combobox(frm, state="readonly", width=35);
    cbo.pack(side="left", padx=5)

    # Load danh sách phòng đang có khách
    stays = fetch_all(
        "SELECT p.MaPhong, d.MaDP, d.TenKhach, d.NgayVao, p.GiaNgay FROM phong p JOIN datphong d ON p.MaPhong=d.MaPhong WHERE p.TrangThai='CoKhach'")
    stay_map = {f"P{r['MaPhong']} - {r['TenKhach']}": r for r in stays}
    cbo['values'] = list(stay_map.keys())

    txt_bill = tk.Text(win, width=60, height=20, font=("Courier New", 10))
    txt_bill.pack(pady=10)

    lbl_total = tk.Label(win, text="TỔNG TIỀN: 0 VNĐ", font=("Arial", 16, "bold"), fg="red")
    lbl_total.pack()

    # Biến lưu trữ tạm
    current_data = {}

    def tinh_tien(event=None):
        val = cbo.get()
        if not val: return

        data = stay_map[val]
        curr_mp = data['MaPhong']
        curr_mdp = data['MaDP']
        gia = float(data['GiaNgay'])

        # Tính ngày ở
        vao = data['NgayVao']
        ra = datetime.now()
        delta = ra - vao
        # Tính theo giờ hoặc ngày (ở đây làm tròn ngày, tối thiểu 1 ngày)
        ngay_o = delta.days if delta.days > 0 else 1

        tien_phong = ngay_o * gia

        # Tiền dịch vụ
        svs = fetch_all(
            "SELECT d.TenDV, s.SoLuong, d.DonGia FROM sudungdv s JOIN dichvu d ON s.MaDV=d.MaDV WHERE s.MaDP=%s",
            (curr_mdp,))
        tien_dv = sum([s['SoLuong'] * float(s['DonGia']) for s in svs])
        tong = tien_phong + tien_dv

        # Lưu thông tin để dùng khi bấm nút Thanh Toán
        current_data['MaPhong'] = curr_mp
        current_data['TenKhach'] = data['TenKhach']
        current_data['MaDP'] = curr_mdp
        current_data['NgayVao'] = vao
        current_data['NgayRa'] = ra
        current_data['TienPhong'] = tien_phong
        current_data['TienDichVu'] = tien_dv
        current_data['TongTien'] = tong

        # In Bill ra màn hình
        bill = f"{'=' * 40}\n"
        bill += f"      HÓA ĐƠN KHÁCH SẠN SKY\n"
        bill += f"{'=' * 40}\n"
        bill += f"Phòng: {curr_mp}\n"
        bill += f"Khách hàng: {data['TenKhach']}\n"
        bill += f"Check-in:   {vao}\n"
        bill += f"Check-out:  {ra.strftime('%Y-%m-%d %H:%M:%S')}\n"
        bill += f"Thời gian:  {ngay_o} ngày\n"
        bill += f"{'-' * 40}\n"
        bill += f"1. TIỀN PHÒNG:\n"
        bill += f"   {gia:,.0f} x {ngay_o} ngày = {tien_phong:,.0f}\n\n"
        bill += f"2. DỊCH VỤ:\n"
        if not svs: bill += "   (Không sử dụng dịch vụ)\n"
        for s in svs:
            thanh_tien = s['SoLuong'] * float(s['DonGia'])
            bill += f"   - {s['TenDV']:<20} x{s['SoLuong']:<3} = {thanh_tien:,.0f}\n"
        bill += f"{'-' * 40}\n"
        bill += f"TỔNG CỘNG: {tong:,.0f} VNĐ\n"
        bill += f"{'=' * 40}"

        txt_bill.delete(1.0, tk.END)
        txt_bill.insert(tk.END, bill)
        lbl_total.config(text=f"TỔNG TIỀN: {tong:,.0f} VNĐ")

    cbo.bind("<<ComboboxSelected>>", tinh_tien)

    def thanh_toan():
        if not current_data: return

        if messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn thanh toán và lưu hóa đơn?"):
            # 1. LƯU VÀO LỊCH SỬ (Bảng hoadon)
            sql_insert = """
                INSERT INTO hoadon (MaPhong, TenKhach, NgayVao, NgayRa, TienPhong, TienDichVu, TongTien)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            params = (
                current_data['MaPhong'], current_data['TenKhach'],
                current_data['NgayVao'], current_data['NgayRa'],
                current_data['TienPhong'], current_data['TienDichVu'], current_data['TongTien']
            )
            execute_query(sql_insert, params)

            # 2. XÓA DỮ LIỆU ĐẶT PHÒNG
            mdp = current_data['MaDP']
            execute_query("DELETE FROM sudungdv WHERE MaDP=%s", (mdp,))
            execute_query("DELETE FROM datphong WHERE MaDP=%s", (mdp,))
            execute_query("UPDATE phong SET TrangThai='Trong' WHERE MaPhong=%s", (current_data['MaPhong'],))

            messagebox.showinfo("Thành công", "Đã thanh toán và lưu hóa đơn!")
            callback_refresh()
            win.destroy()

    tk.Button(win, text="THANH TOÁN & IN BILL", bg="#c0392b", fg="white", font=("Arial", 12, "bold"),
              command=thanh_toan).pack(pady=10)