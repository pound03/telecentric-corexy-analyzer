from pypylon import pylon
import cv2
import serial
import time

# 1. เชื่อมต่อกล้อง
camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
camera.Open()
name = 1
try:
# ตั้งค่าตามภาพ
    camera.Width.SetValue(2592)
    camera.Height.SetValue(1944)
    camera.PixelFormat.SetValue("BGR8")

    # camera.ExposureAuto.SetValue("Continuous")
    # camera.GainAuto.SetValue("Continuous")

    camera.ExposureAuto.SetValue("Off")
    camera.GainAuto.SetValue("Off")
    camera.ExposureTime.SetValue(26000.0)  # ลดจาก 20000 หรือ 50000 → เร็วขึ้น
    camera.Gain.SetValue(5.0)              # ค่าปานกลาง

except:
    print("กล้องไม่รองรับการตั้งค่า ROI")

ser = serial.Serial('COM5', 115200, timeout=1)


# 5. เริ่มจับภาพ
camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)
converter = pylon.ImageFormatConverter()
converter.OutputPixelFormat = pylon.PixelType_BGR8packed
converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned

# 6. วนลูปแสดงภาพ พร้อมกลับแกน XY
print("กด 'q' เพื่อออกจากโปรแกรม")
time_now = time.time()
while camera.IsGrabbing():
    # if ser income data
    grabResult = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
    if grabResult.GrabSucceeded():
        image = converter.Convert(grabResult)
        img_flipped = image.GetArray()
        # print("image_size:", img_flipped.shape)

        # offset 40 pixel all sides
        size = 0
        # img_flipped = img_flipped[size+2:-(size+2), size+1:-(size+1)]
        # set black left side shape / 16 
        img_flipped = img_flipped[:, int(img_flipped.shape[1] / 16):]

        # add red line from top to bottom
        # cv2.line(img_flipped, (int(img_flipped.shape[1] / 16), 0), (int(img_flipped.shape[1] / 16), img_flipped.shape[0]), (0, 0, 255), 5)
        # add red line from left to right
        # cv2.line(img_flipped, (0, int(img_flipped.shape[0] / 2)), (img_flipped.shape[1], int(img_flipped.shape[0] / 2)), (0, 0, 255), 5)

        # q to quit program
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            if line:
                name_file = f"image_{line}.png"
                cv2.imwrite(name_file, img_flipped)
                print(f"Saved: {name_file}")

        # add hz to img_flipped
        img_flipped = cv2.resize(img_flipped, (0, 0), fx=0.25, fy=0.25)
        cv2.putText(img_flipped, f"Hz: {int(1/(time.time()-time_now))}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        time_now = time.time()
        cv2.imshow('Basler (Flipped & Zoomed Out)', img_flipped)
    grabResult.Release()

# 7. ปิดกล้อง
camera.StopGrabbing()
camera.Close()
cv2.destroyAllWindows()
