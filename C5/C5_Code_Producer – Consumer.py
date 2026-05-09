
#🎯 Ý tưởng thực tế
#Producer (nhà sản xuất) → tạo sản phẩm
#Consumer (người tiêu thụ) → lấy sản phẩm ra dùng
#Buffer (kho chứa) có giới hạn kích thước
#👉 Nếu:
#Kho đầy → Producer phải chờ
#Kho rỗng → Consumer phải chờ
#👉 Đây chính là ứng dụng của:
#Semaphore
#Đồng bộ hóa luồng

# ================== 1. IMPORT THƯ VIỆN ==================
import threading    # tạo luồng
import time         # tạo độ trễ
import random       # tạo dữ liệu ngẫu nhiên

# ================== 2. KHỞI TẠO BUFFER ==================
buffer = []              # kho chứa
BUFFER_SIZE = 5          # kích thước tối đa

# Semaphore
empty = threading.Semaphore(BUFFER_SIZE)  # số ô trống
full = threading.Semaphore(0)             # số ô đã có dữ liệu

# Mutex (khóa để tránh xung đột)
mutex = threading.Lock()

# ================== 3. PRODUCER ==================
def producer():
    for i in range(10):  # sản xuất 10 sản phẩm
        item = random.randint(1, 100)

        empty.acquire()   # chờ nếu buffer đầy
        mutex.acquire()   # khóa vùng tới hạn

        buffer.append(item)
        print(f"🟢 Producer tạo: {item} | Buffer: {buffer}")

        mutex.release()   # mở khóa
        full.release()    # báo có sản phẩm

        time.sleep(random.uniform(0.5, 1.5))


# ================== 4. CONSUMER ==================
def consumer():
    for i in range(10):  # tiêu thụ 10 sản phẩm
        full.acquire()    # chờ nếu buffer rỗng
        mutex.acquire()   # khóa vùng tới hạn

        item = buffer.pop(0)
        print(f"🔴 Consumer dùng: {item} | Buffer: {buffer}")

        mutex.release()   # mở khóa
        empty.release()   # báo có chỗ trống

        time.sleep(random.uniform(0.5, 2))


# ================== 5. TẠO LUỒNG ==================
t1 = threading.Thread(target=producer)
t2 = threading.Thread(target=consumer)

t1.start()
t2.start()

t1.join()
t2.join()

print("🎉 Hoàn thành Producer – Consumer")