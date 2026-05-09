
#🎯 Ý tưởng bài toán
#Có 5 triết gia ngồi quanh bàn
#Có 5 chiếc đũa (mỗi người có 1 bên trái + 1 bên phải)
#Muốn ăn → phải lấy 2 chiếc đũa
#Sau khi ăn → đặt đũa xuống

#👉 Vấn đề:
#Nếu ai cũng cầm 1 chiếc → deadlock (kẹt cứng)

# ================== 1. IMPORT ==================
import threading
import time
import random

# ================== 2. THAM SỐ ==================
N = 5   # có thể đổi số triết gia tùy ý
EAT_TIMES = 3

# ================== 3. TRẠNG THÁI ==================
states = ["Thinking"] * N

def print_states():
    print(" | ".join([f"P{i}:{states[i]}" for i in range(N)]))
    print("-" * 50)

# ================== 4. TẠO ĐŨA ==================
chopsticks = [threading.Semaphore(1) for _ in range(N)]

# ================== 5. PHIÊN BẢN DEADLOCK ==================
def philosopher_deadlock(i):
    left = i
    right = (i + 1) % N

    for _ in range(EAT_TIMES):
        states[i] = "Thinking"
        print_states()
        time.sleep(random.uniform(0.5, 1.5))

        states[i] = "Waiting"
        print_states()

        # ❌ LẤY ĐŨA TRÁI TRƯỚC → dễ gây deadlock
        chopsticks[left].acquire()
        time.sleep(0.1)  # cố tình tạo điều kiện deadlock
        chopsticks[right].acquire()

        states[i] = "Eating"
        print_states()
        time.sleep(random.uniform(1, 2))

        chopsticks[left].release()
        chopsticks[right].release()

# ================== 6. PHIÊN BẢN TRÁNH DEADLOCK ==================
butler = threading.Semaphore(N - 1)

def philosopher_safe(i):
    left = i
    right = (i + 1) % N

    for _ in range(EAT_TIMES):
        states[i] = "Thinking"
        print_states()
        time.sleep(random.uniform(0.5, 1.5))

        states[i] = "Waiting"
        print_states()

        # ✅ Xin phép butler
        butler.acquire()

        # Lấy đũa
        chopsticks[left].acquire()
        chopsticks[right].acquire()

        states[i] = "Eating"
        print_states()
        time.sleep(random.uniform(1, 2))

        chopsticks[left].release()
        chopsticks[right].release()

        butler.release()

# ================== 7. CHẠY MÔ PHỎNG ==================
def run_simulation(mode="safe"):
    threads = []

    print(f"\n===== CHẠY CHẾ ĐỘ: {mode.upper()} =====\n")

    for i in range(N):
        if mode == "deadlock":
            t = threading.Thread(target=philosopher_deadlock, args=(i,))
        else:
            t = threading.Thread(target=philosopher_safe, args=(i,))
        threads.append(t)
        t.start()

    # timeout để tránh treo khi deadlock
    for t in threads:
        t.join(timeout=10)

    print("\n🎉 Kết thúc mô phỏng\n")

# ================== 8. CHẠY THỬ ==================
run_simulation("deadlock")   # có thể bị kẹt
run_simulation("safe")       # không bị kẹt