# 📷 Telecentric CoreXY AutoBoard Analyzer

An automated board inspection system combining **telecentric imaging**, **CoreXY motion**, and **AI-powered analysis** via ChatGPT.  
The system captures high-resolution PCB images, merges them, detects board features (ICs, screw holes, contours), and provides a **web interface** for visualization and interaction with ChatGPT to help identify board models.

---

## 🔧 Features

- **High-Precision Telecentric Imaging**  
  Capture four distortion-free images and stitch them into one large board image.

- **Automated CoreXY Scanning Platform**  
  Controlled by stepper motors via Raspberry Pi Pico (or similar), moves camera accurately.

- **Contour and Feature Detection**  
  Detects IC boundaries, holes, and board edges. Output can be saved as DXF files.

- **Web Visualization & Control**  
  Flask-based interface with real-time video feed and parameter adjustment.

- **ChatGPT Integration**  
  After image processing, the system sends a prompt to ChatGPT asking for board identification.

---

## 📁 Project Structure

```
.
├── A_low_level.py        # CoreXY movement control (via GPIO / Raspberry Pi Pico)
├── B_cam_serial.py       # Captures images based on serial signal
├── BC_merge_image.py     # Combines 4 images into 1 and applies Gaussian blur
├── C_web_image.py        # Flask app for UI, feature detection, and DXF export
├── D_chat.py             # Automates ChatGPT web interface interaction
├── /save/sub_image/      # Folder for temporary image tiles
├── /save/full_image.jpg  # Merged board image
├── /search/board.jpg     # Image sent to ChatGPT
├── output.dxf            # Contour export
```

---

## 🛠️ Hardware Requirements

- CoreXY platform (custom built or kit)
- 2x stepper motors + drivers
- Raspberry Pi Pico / Arduino (controls XY motion)
- Basler Telecentric Industrial Camera
- PC with Windows (for camera & AI interaction)
- USB Serial interface

---

## 🧪 Software Requirements

- Python 3.8+
- [pypylon](https://github.com/basler/pypylon) (Basler SDK)
- OpenCV
- Flask
- pyserial
- pyautogui
- ezdxf

Install dependencies:
```bash
pip install opencv-python flask pyserial pyautogui ezdxf
```

---

## 🚀 How to Run

1. **Connect Hardware**
   - USB: Camera and MCU
   - Ensure camera is working and recognized by pypylon

2. **Run Motion Control (MCU script)**
   ```bash
   python A_low_level.py
   ```

3. **Start Image Capture**
   ```bash
   python B_cam_serial.py
   ```

4. **Merge Images**
   ```bash
   python BC_merge_image.py
   ```

5. **Launch Web Interface**
   ```bash
   python C_web_image.py
   ```
   - Open browser at `http://localhost:5000`

6. **Enable ChatGPT Auto Query (Optional)**
   ```bash
   python D_chat.py
   ```

---

## 🧠 ChatGPT Integration

After stitching and processing, `board.jpg` is created and:
- Mouse automation types "what is this board" into ChatGPT (web)
- AI suggests board type, model, or IC family
- User gets real-time response without manual typing

> 🔒 *Future version may switch to API-based GPT interaction*

---

## 📤 Output Files

| File | Description |
|------|-------------|
| `image_1.png` to `image_4.png` | Captured sub-images |
| `full_image.jpg` | Merged board image |
| `board.jpg` | Image for ChatGPT |
| `output.dxf` | DXF file with contours and circles |

---

## 📌 Future Improvements

- Add automatic Z-height focus control
- Switch to OpenAI API for cleaner integration
- Add part number recognition (OCR)
- PDF report export with DXF overlay

---

## 👤 Author

**Weerapat Supapornopas**  
Control Engineering, Chulalongkorn University  
📧 Contact: [Your Email]

---

## 📝 License

This project is intended for **research and prototyping** only.  
Please contact the author for permission if used commercially.
