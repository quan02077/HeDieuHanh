#🎯 Ý tưởng thực tế
#Bãi đỗ xe có 5 chỗ
#Có 10 xe muốn vào
#Nếu bãi đầy → xe phải chờ
#Khi có xe rời đi → xe khác mới được vào
#👉 Đây chính là ứng dụng của Semaphore (giới hạn tài nguyên)

# ================== 1. IMPORT THƯ VIỆN ==================
import threading   # dùng để tạo nhiều luồng (xe)
import time        # dùng để tạo độ trễ (giả lập thời gian)
import random      # tạo thời gian ngẫu nhiên

# ================== 2. TẠO SEMAPHORE ==================
# Bãi đỗ xe có tối đa 5 chỗ
parking_lot = threading.Semaphore(5)

# ================== 3. HÀM MÔ PHỎNG XE ==================
def car(car_id):
    print(f"🚗 Xe {car_id} đang đến bãi...")

    # ===== XIN VÀO BÃI (ACQUIRE) =====
    parking_lot.acquire()
    print(f"✅ Xe {car_id} đã vào bãi")

    # ===== GIẢ LẬP THỜI GIAN ĐỖ XE =====
    parking_time = random.randint(2, 5)
    time.sleep(parking_time)

    print(f"🚙 Xe {car_id} rời bãi sau {parking_time} giây")

    # ===== RỜI BÃI (RELEASE) =====
    parking_lot.release()

# ================== 4. TẠO CÁC XE ==================
threads = []

for i in range(10):  # 10 xe
    t = threading.Thread(target=car, args=(i,))
    threads.append(t)
    t.start()

# ================== 5. CHỜ TẤT CẢ XE HOÀN THÀNH ==================
for t in threads:
    t.join()

print("🎉 Tất cả xe đã rời bãi")