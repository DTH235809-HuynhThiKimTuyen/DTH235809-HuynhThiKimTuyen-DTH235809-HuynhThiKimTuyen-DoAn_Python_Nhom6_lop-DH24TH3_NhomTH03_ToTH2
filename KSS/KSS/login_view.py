from tkinter import *
from tkinter import messagebox
from database import dang_nhap  # Đảm bảo file database.py nằm cùng thư mục

print("[-] Đang khởi động giao diện...")  # In ra để kiểm tra


def login():
    # 1. Tạo cửa sổ
    root = Tk()
    root.title("Đăng Nhập Khách Sạn")
    root.geometry("400x350")
    root.configure(bg="#3f99ff")

    # 2. Vẽ giao diện
    Label(root, text="HOTEL LOGIN", font=("Arial", 20, "bold"), bg="#340BDB", fg="white").pack(pady=30)

    frame = Frame(root, bg="#2154fb")
    frame.pack()

    Label(frame, text="Tài khoản:", bg="#2302C7", fg="white", font=("Arial", 11)).grid(row=0, column=0, pady=10)
    e_user = Entry(frame, font=("Arial", 11))
    e_user.grid(row=0, column=1, pady=10)
    e_user.focus()

    Label(frame, text="Mật khẩu:", bg="#001dc4", fg="white", font=("Arial", 11)).grid(row=1, column=0, pady=10)
    e_pass = Entry(frame, show="*", font=("Arial", 11))
    e_pass.grid(row=1, column=1, pady=10)

    # Hàm xử lý khi bấm nút
    def xuly(event=None):
        u = e_user.get()
        p = e_pass.get()
        print(f"[-] Đang thử đăng nhập với: {u} / {p}")

        user_data = dang_nhap(u, p)

        if user_data:
            print("[-] Đăng nhập thành công!")
            messagebox.showinfo("Thành công", f"Xin chào {user_data['FullName']}")
            root.destroy()

            # Mở màn hình chính
            import main
            main.main_view(user_data)
        else:
            print("[-] Đăng nhập thất bại!")
            messagebox.showerror("Lỗi", "Sai tài khoản hoặc mật khẩu!\n(Thử: admin / admin)")

    # Nút bấm
    Button(root, text="ĐĂNG NHẬP", bg="#0e03d7", fg="white", font=("Arial", 12, "bold"), width=20, command=xuly).pack(
        pady=30)
    root.bind('<Return>', xuly)  # Cho phép bấm Enter để đăng nhập

    print("[-] Cửa sổ đã được tạo. Đang chờ người dùng...")

    # 3. DÒNG QUAN TRỌNG NHẤT: Giữ cửa sổ hiển thị
    root.mainloop()


# --- GỌI THẲNG HÀM LUÔN (KHÔNG DÙNG if __name__) ---
# Cách này đảm bảo 100% code sẽ chạy khi bạn bấm Run
login()