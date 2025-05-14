from machine import Pin, PWM
import time

# กำหนดพินสำหรับมอเตอร์ 1
st1 = Pin(26, Pin.OUT)
dr1 = Pin(27, Pin.OUT)
en1 = Pin(19, Pin.OUT)

# กำหนดพินสำหรับมอเตอร์ 2
st2 = Pin(17, Pin.OUT)
dr2 = Pin(18, Pin.OUT)
en2 = Pin(16, Pin.OUT)

# กำหนดพินสำหรับปุ่มควบคุม
btn1 = Pin(12, Pin.IN, Pin.PULL_UP)
btn2 = Pin(11, Pin.IN, Pin.PULL_UP)
btn3 = Pin(20, Pin.IN, Pin.PULL_UP)
btn4 = Pin(21, Pin.IN, Pin.PULL_UP)
btn5 = Pin(22, Pin.IN, Pin.PULL_UP)

step = 400
stop_flag = False  # ตัวแปรหยุดทุกลูป

sleep = 0.5
def run(pin):
    global stop_flag
    if stop_flag:
        return
    pin.on()
    time.sleep(0.001)
    pin.off()
    time.sleep(0.001)

def right():
    dr2.off()
    run(st2)

def left():
    dr2.on()
    run(st2)

def forward():
    dr1.on()
    run(st1)

def backward():
    dr1.off()
    run(st1)

def set_up():
    global stop_flag,sleep
    while btn1.value() and not stop_flag:
        backward()
    while btn2.value() and not stop_flag:
        left()
    for i in range(1100):
        if stop_flag: return
        right()

    for i in range(1000):
        if stop_flag: return
        forward()

def move_motor():
    global stop_flag
    y = 550
    x = 775
    dt = 0.002
    time.sleep(0.5)
    print("2")
    time.sleep(sleep)
    for i in range(580):
        if stop_flag: return
        forward()
        time.sleep(dt)
    for i in range(5):
        if stop_flag: return
        right()
        time.sleep(dt)
    time.sleep(0.5)
    print("4")
    time.sleep(sleep)
    for i in range(710):
        if stop_flag: return
        right()
        time.sleep(dt)
    for i in range(25):
        if stop_flag: return
        backward()
        time.sleep(dt)
    time.sleep(0.5)
    print("3")
    time.sleep(sleep)
    for i in range(575):
        if stop_flag: return
        backward()
        time.sleep(dt)
    for i in range(5):
        if stop_flag: return
        left()
        time.sleep(dt)
    time.sleep(0.5)
    print("1")
    time.sleep(sleep)
set_up()

while True:
    if not btn5.value():
        stop_flag = True
        print("stop")
        break

    stop_flag = False
    if not btn3.value():
        set_up()
    if not btn4.value():
        move_motor()
        set_up()

