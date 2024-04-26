import cv2
import numpy as np
import pygetwindow as gw
import pyautogui

# ระบุชื่อหน้าต่างที่ต้องการจับ
window_title = "FiveM® by Cfx.re - CHANOM CITY"

# หาหน้าต่างที่ตรงกับชื่อ
window = gw.getWindowsWithTitle(window_title)[0]

# โหลดภาพของลูกศรทั้ง 4 รูป
arrow_images = {}
arrow_files = ["arrowup.png", "arrowdown.png", "arrowleft.png", "arrowright.png"]
for arrow_file in arrow_files:
    arrow_image = cv2.imread(arrow_file, cv2.IMREAD_COLOR)  # อ่านเป็นภาพสีแท้
    arrow_images[arrow_file] = arrow_image

# สร้างหน้าต่าง OpenCV เพื่อแสดงผลภาพเรียลไทม์
cv2.namedWindow("Image", cv2.WINDOW_NORMAL)

while True:
    # จับภาพหน้าจอของหน้าต่างที่เลือก
    screenshot = pyautogui.screenshot(region=(window.left, window.top, window.width, window.height))
    img = np.array(screenshot)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)  # แปลงสีจาก RGB เป็น BGR

    # ทำ Template Matching กับทุกภาพลูกศร
    for arrow_file, arrow_image in arrow_images.items():
        arrow_image_resized = cv2.resize(arrow_image, (30, 30))  # ปรับขนาดภาพเป็นขนาดเล็กลง
        res = cv2.matchTemplate(img, arrow_image_resized, cv2.TM_CCOEFF_NORMED)
        threshold = 0.8
        loc = np.where(res >= threshold)

        # วาดสี่เหลี่ยมรอบลูกศรที่ตรงกับ template บนภาพหน้าจอ
        for pt in zip(*loc[::-1]):
            x, y = pt[0] + 30 // 2, pt[1] + 30 // 2  # คำนวณหาจุดกึ่งกลางของสี่เหลี่ยม
            cv2.rectangle(img, (pt[0], pt[1]), (pt[0] + 30, pt[1] + 30), (0, 255, 0), 2)  # วาดสี่เหลี่ยมรอบลูกศร
            print("Arrow Detected at:", (x, y))  # พิมพ์พิกัดจุดกึ่งกลาง

            # กดปุ่มลูกศรตามที่ detect ได้
            if arrow_file == "arrowup.png":
                pyautogui.press('up')
            elif arrow_file == "arrowdown.png":
                pyautogui.press('down')
            elif arrow_file == "arrowleft.png":
                pyautogui.press('left')
            elif arrow_file == "arrowright.png":
                pyautogui.press('right')

    # แสดงผลภาพเรียลไทม์บนหน้าต่าง OpenCV
    cv2.imshow("Image", img)

    # รอการกด 'q' เพื่อออกจากโปรแกรม
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# ปิดหน้าต่าง OpenCV เมื่อออกจากโปรแกรม
cv2.destroyAllWindows()
