from flask import Flask, render_template, Response, request, jsonify
import cv2
import ezdxf
import numpy as np
import os
import time

app = Flask(__name__)
cap = cv2.VideoCapture(0)


screen = np.zeros((480, 640, 3), dtype=np.uint8)
cv2.putText(screen, "Waiting image", (50, 240), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

all_edges = None
storage_image = None
# เก็บค่าเริ่มต้นของ slider แต่ละตัว
params = {
    'dp_x10':   1,
    'conf':    10,
    'minR':     1,
    'maxR':     8,
    'minDist':  3,
    'fil_hole': 2,
    'fil_edge': 5,
    'con2':    10
}

def save_contours_to_dxf(filename="output.dxf"):
    global all_edges
    if all_edges is None:
        print("No contours to save.")
        return
    doc = ezdxf.new()
    msp = doc.modelspace()
    for contour in all_edges:
        points = contour.squeeze()
        if len(points.shape) != 2 or points.shape[0] < 2:
            continue
        for i in range(len(points)):
            start = tuple(points[i])
            end = tuple(points[(i + 1) % len(points)])
            msp.add_line(start, end)
    doc.saveas(filename)
    print(f"✅ Saved to {filename}")

    # save storage_image to "C:\\Users\\weera\\Desktop\\project\\code\\search\\board.jpg"
    cv2.imwrite("board.jpg", storage_image)


def detect_image():
    global screen, storage_image

    # ใช้ path จากโฟลเดอร์ปัจจุบัน
    current_dir = os.getcwd()
    image_path = os.path.join(current_dir, "full_image.jpg")

    if os.path.exists(image_path):
        image = cv2.imread(image_path)

        # Resize image เป็นขนาด 1/8
        image = cv2.resize(image, (image.shape[1] // 8, image.shape[0] // 8))

        storage_image = image.copy()
        print("✅ detect_image")

        os.remove(image_path)
    
def calimg():
    global screen , storage_image
    if storage_image is None:
        return
    # print("calimg")
    image = storage_image.copy()
    dp = max((5-params['dp_x10'])*0.1+1, 1)
    circle_thresh = int(np.interp(params['conf'], [0, 40], [10, 80]))
    minRadius = int(np.interp(params['minR'], [0, 20], [1, 20]))
    maxRadius = int(np.interp(params['maxR'], [0, 20], [5, 50]))
    minDist = int(np.interp(params['minDist'], [1, 20], [1, 100]))
    edge_thresh = int(np.interp(params['con2'], [0, 10], [30, 100]))
    filter_hole = (params['fil_hole'] + 1)*2+1
    filter_edge = (params['fil_edge'] + 1)*2+1

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (filter_hole, filter_hole), 0)

    circles = cv2.HoughCircles(
        blur,
        cv2.HOUGH_GRADIENT,
        dp=dp,
        minDist=minDist,
        param1=edge_thresh,
        param2=circle_thresh,
        minRadius=minRadius,
        maxRadius=maxRadius
    )

    blur = cv2.GaussianBlur(gray, (3, 3), 0)
    edges = cv2.Canny(blur, 50, 150)
    kernel = np.ones((filter_edge, filter_edge), np.uint8)
    edges_dilate = cv2.dilate(edges, kernel, iterations=1)
    edges_dilate = cv2.erode(edges_dilate, kernel, iterations=1)
    edges_dilate = cv2.GaussianBlur(edges_dilate, (filter_edge, filter_edge), 0)
    contour , _ = cv2.findContours(edges_dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    screen = image.copy()
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for (x, y, r) in circles[0, :]:
            cv2.circle(screen, (x, y), r, (255, 0, 0), 2)
            cv2.circle(screen, (x, y), 2, (0, 0, 255), 3)

    if contour :
        cv2.drawContours(screen, contour, -1, (0, 255, 0), 2)

    global all_edges
    all_edges = []
    #add contours to all_edges
    for cnt in contour:
        if len(cnt) > 0:
            all_edges.append(cnt)
    if circles is not None:
        circles = np.uint16(np.around(circles))
        #add circles to all_edges
        for (i, (x, y, r)) in enumerate(circles[0, :]):
            circle_contour = np.array([[[x + r * np.cos(theta), y + r * np.sin(theta)]] for theta in np.linspace(0, 2 * np.pi, 100)])
            all_edges.append(circle_contour)



def gen_frames():
    while True:
        # อ่านภาพจากกล้อง
        detect_image()
        if storage_image is not None:
            calimg()
        ret , buffer = cv2.imencode('.jpg', screen)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
        time.sleep(0.1)


@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

# รับค่าจาก slider มาอัปเดตใน dict
@app.route('/update_params', methods=['POST'])
def update_params():
    data = request.get_json()
    for k in params:
        if k in data:
            try:
                params[k] = int(data[k])
            except:
                pass
    return jsonify(success=True)

@app.route('/')
def index():
    return render_template('index.html', params=params)

@app.route('/save', methods=['POST'])
def toggle_save():
    save_contours_to_dxf()
    print("save")
    return ('', 204)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
