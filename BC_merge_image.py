import os
import cv2
import numpy as np
import time

data = []

while True:
    # ใช้ path ปัจจุบัน
    current_dir = os.getcwd()
    image_paths = [os.path.join(current_dir, f"image_{i}.png") for i in range(1, 5)]

    # ตรวจสอบว่าไฟล์ทั้ง 4 มีอยู่จริง
    if all(os.path.exists(p) for p in image_paths):
        for path in image_paths:
            img = cv2.imread(path)
            if img is None:
                print(f"❌ Error reading: {path}")
                continue
            data.append(img)
            os.remove(path)  # ลบไฟล์หลังโหลด

        # ประมวลผลรวมภาพ 2x2
        h, w = data[0].shape[:2]
        new_image = np.zeros((h * 2, w * 2, 3), dtype=np.uint8)
        new_image[0:h, 0:w] = data[0]
        new_image[0:h, w:] = data[1]
        new_image[h:, 0:w] = data[2]
        new_image[h:, w:] = data[3]
        data = []

        # เบลอภาพ
        new_image = cv2.GaussianBlur(new_image, (0, 0), 10)

        # เซฟภาพรวม
        output_path = os.path.join(current_dir, "full_image.jpg")
        cv2.imwrite(output_path, new_image)
        print(f"✅ Saved merged image: {output_path} | Shape: {new_image.shape}")
    else:
        print("🕐 Waiting for image_1.png - image_4.png...")

    time.sleep(1)
