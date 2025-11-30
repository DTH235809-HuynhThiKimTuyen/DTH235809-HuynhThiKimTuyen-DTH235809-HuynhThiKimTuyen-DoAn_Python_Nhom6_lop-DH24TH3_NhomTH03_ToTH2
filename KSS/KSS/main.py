from tkinter import *
from tkinter import messagebox, ttk
from database import fetch_all
from login_view import login
import checkin, service, checkout ,thongke


class HotelApp:
    def __init__(self, root, user):
        self.root = root
        self.user = user
        self.root.title("QUẢN LÝ KHÁCH SẠN PRO")
        self.root.geometry("1100x750")
        self.root.configure(bg="#ecf0f1")

        # --- THÊM ĐOẠN NÀY ĐỂ HIỆN CỬA SỔ LÊN TRÊN CÙNG ---
        self.root.attributes('-topmost', True)  # Đưa lên trên cùng
        self.root.update()
        self.root.attributes('-topmost', False)  # Trả lại bình thường
        self.root.focus_force()  # Bắt buộc lấy tiêu điểm
        # --- 1. HEADER & THỐNG KÊ ---
        self.create_header()

        # --- 2. THANH CÔNG CỤ (TOOLBAR) ---
        self.create_toolbar()

        # --- 3. KHU VỰC SƠ ĐỒ PHÒNG ---
        self.body = Frame(root, bg="#ecf0f1")
        self.body.pack(fill=BOTH, expand=True, padx=20, pady=10)

        # Tiêu đề nhỏ
        lbl_sodo = Label(self.body, text="SƠ ĐỒ TRẠNG THÁI PHÒNG", bg="#ecf0f1", fg="#7f8c8d",
                         font=("Arial", 12, "bold"))
        lbl_sodo.pack(anchor="w", pady=(0, 10))

        # Khung chứa các ô phòng (Grid)
        self.grid_frame = Frame(self.body, bg="#ecf0f1")
        self.grid_frame.pack()

        self.load_map()

    def create_header(self):
        head = Frame(self.root, bg="#2c3e50", height=80)
        head.pack(fill=X)

        # Logo / Tên
        Label(head, text="🏨 SKY HOTEL MANAGER", font=("Verdana", 20, "bold"), fg="#ecf0f1", bg="#2c3e50").pack(
            side=LEFT, padx=30)

        # Thông tin User
        user_info = f"👤 {self.user['FullName']} | 🛡️ {self.user['Role']}"
        Label(head, text=user_info, font=("Arial", 11), fg="#f1c40f", bg="#2c3e50").pack(side=RIGHT, padx=30)

        # Thanh thống kê nhanh (Dashboard mini)
        self.lbl_stats = Label(head, text="Loading...", font=("Arial", 11, "bold"), fg="#2ecc71", bg="#2c3e50")
        self.lbl_stats.pack(side=RIGHT, padx=20)

    def create_toolbar(self):
        tool = Frame(self.root, bg="white", bd=1, relief=RAISED)
        tool.pack(fill=X, pady=2)

        # Style cho nút bấm đẹp hơn
        def make_btn(text, color, cmd):
            return Button(tool, text=text, bg=color, fg="white", font=("Arial", 10, "bold"),
                          relief=FLAT, padx=20, pady=8, cursor="hand2", command=cmd)

        make_btn("➕ NHẬN PHÒNG", "#27ae60", self.mo_checkin).pack(side=LEFT, padx=10, pady=10)
        make_btn("🍽️ DỊCH VỤ", "#e67e22", service.show).pack(side=LEFT, padx=10, pady=10)
        make_btn("💰 TRẢ PHÒNG", "#c0392b", self.mo_checkout).pack(side=LEFT, padx=10, pady=10)
        make_btn("📊 DOANH THU", "#8e44ad", self.xem_doanh_thu).pack(side=LEFT, padx=10, pady=10)

        Button(tool, text="🚪 Đăng Xuất", font=("Arial", 10), command=self.logout).pack(side=RIGHT, padx=20)

    def load_map(self):
        # Xóa cũ
        for w in self.grid_frame.winfo_children(): w.destroy()

        phongs = fetch_all("SELECT * FROM phong")

        # Cập nhật thống kê nhanh trên Header
        total = len(phongs)
        occupied = len([p for p in phongs if p['TrangThai'] == 'CoKhach'])
        empty = total - occupied
        self.lbl_stats.config(text=f"Tổng: {total} | Trống: {empty} | Có khách: {occupied}")

        COL_NUM = 4  # Số cột

        for i, p in enumerate(phongs):
            r = i // COL_NUM
            c = i % COL_NUM

            # Xử lý Giao diện thẻ phòng
            state = p['TrangThai']
            is_vip = "VIP" in p['LoaiPhong'] or "Tổng Thống" in p['LoaiPhong']

            # Màu nền: Xanh (Trống), Đỏ (Có Khách)
            bg_color = "#2ecc71" if state == 'Trong' else "#e74c3c"
            # Viền: Vàng nếu là VIP, Trắng nếu thường
            border_color = "#f1c40f" if is_vip else "white"
            border_width = 4 if is_vip else 2

            # Khung thẻ phòng (Card)
            card = Frame(self.grid_frame, bg=bg_color, width=200, height=130,
                         highlightbackground=border_color, highlightthickness=border_width)
            card.grid(row=r, column=c, padx=15, pady=15)
            card.pack_propagate(False)

            # Icon trạng thái
            icon = "🛏️" if state == 'Trong' else "👤"

            # Nội dung thẻ
            Label(card, text=f"{icon} P.{p['MaPhong']}", bg=bg_color, fg="white", font=("Arial", 18, "bold")).pack(
                pady=(15, 5))

            # Badge loại phòng
            lbl_loai = Label(card, text=p['LoaiPhong'].upper(), bg="white", fg="#333", font=("Arial", 8, "bold"),
                             padx=5)
            lbl_loai.pack(pady=2)

            # Trạng thái
            status_text = "SẴN SÀNG" if state == 'Trong' else "ĐANG Ở"
            Label(card, text=status_text, bg=bg_color, fg="white", font=("Arial", 10)).pack(side=BOTTOM, pady=10)

    def xem_doanh_thu(self):
        # Đây là chỗ bạn có thể mở rộng sau này để vẽ biểu đồ
        # Hiện tại mình thông báo đơn giản
        messagebox.showinfo("Tính năng nâng cao",
                            "Chức năng Báo cáo Doanh thu cần tạo thêm bảng 'Lịch sử hóa đơn' để lưu lại các đơn đã thanh toán thay vì xóa đi.")

    def mo_checkin(self):
        checkin.show(self.load_map)

    def mo_checkout(self):
        checkout.show(self.load_map)

    def logout(self):
        self.root.destroy()
        login()

    def xem_doanh_thu(self):
        thongke.show()

def main_view(user):
    root = Tk()
    app = HotelApp(root, user)
    root.mainloop()