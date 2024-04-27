import cv2
import numpy as np
import pygetwindow as gw
import pyautogui
import time

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

# โหลดภาพ spacecheck.png
spacecheck_image = cv2.imread("spacecheck.png", cv2.IMREAD_COLOR)  # อ่านเป็นภาพสีแท้

# สร้างหน้าต่าง OpenCV เพื่อแสดงผลภาพเรียลไทม์
cv2.namedWindow("Image", cv2.WINDOW_NORMAL)

initial_y = None
initial_x = None
previous_y = None
previous_x = None
detected_x_values = []
detected_buttons = []

start_time = time.time()

unique_data = []
next_index_to_press = None

count_detection = 0

while True:
    if len(unique_data) == 6:
        for i, (x, button) in enumerate(unique_data):
            if button == "arrowup.png":
                pyautogui.press('up')
                print("Pressed: up")
            elif button == "arrowdown.png":
                pyautogui.press('down')
                print("Pressed: down")
            elif button == "arrowleft.png":
                pyautogui.press('left')
                print("Pressed: left")
            elif button == "arrowright.png":
                pyautogui.press('right')

        # ตรวจสอบเงื่อนไขเพื่อกำหนดค่าดีเลย์
        if time.time() - start_time > 9.61:
            delay = 1.16
            print("Time Top 9.6:", time.time() - start_time)
        elif time.time() - start_time > 9.51:
            delay = 1.2
            print("Time Top 9.5:", time.time() - start_time)
        elif time.time() - start_time < 9.2:
            if time.time() - start_time >= 9.18:
                delay = 1.49
            else:
                delay = 1.53
            print("Time Top 9.2:", time.time() - start_time)  
        elif time.time() - start_time < 9.3:
            delay = 1.4
            print("Time Top 9.3:", time.time() - start_time)
        elif time.time() - start_time > 9.3 and time.time() - start_time < 9.32:
            if time.time() - start_time > 9.30 and time.time() - start_time < 9.316:
                delay = 1.39
            else:
                delay = 1.44
            print("Time Top 9.3 - 9.32:", time.time() - start_time)
        elif time.time() - start_time > 9.32 and time.time() - start_time < 9.395:
            delay = 1.32
            print("Time Top 9.32 - 9.39:", time.time() - start_time)  
        else:
            delay = 1.25
            print("Time Top Else:", time.time() - start_time)  

        # นอนดีเลย์ตามที่กำหนด
        time.sleep(delay)

        pyautogui.press('space')
        print("Pressed: space")
        initial_y = None
        initial_x = None
        previous_y = None
        previous_x = None
        detected_x_values = []
        detected_buttons = []
        start_time = time.time()
        unique_data = []
        next_index_to_press = None
        count_detection = 0
        print("Reset all data")
        continue

    screenshot = pyautogui.screenshot(region=(window.left, window.top, window.width, window.height))
    img = np.array(screenshot)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    # ทำ Template Matching กับทุกภาพลูกศร
    for arrow_file, arrow_image in arrow_images.items():
        arrow_image_resized = cv2.resize(arrow_image, (30, 30))
        res = cv2.matchTemplate(img, arrow_image_resized, cv2.TM_CCOEFF_NORMED)
        threshold = 0.8
        loc = np.where(res >= threshold)

        for pt in zip(*loc[::-1]):
            x, y = pt[0] + 30 // 2, pt[1] + 30 // 2

            if len(detected_x_values) > 0 and abs(x - detected_x_values[-1]) <= 20:
                continue

            cv2.rectangle(img, (pt[0], pt[1]), (pt[0] + 30, pt[1] + 30), (0, 255, 0), 2)
            print("Arrow Detected at:", (x, y))

            detected_x_values.append(x)
            detected_buttons.append(arrow_file)

            count_detection += 1
            print("CountDetect", count_detection)

            sorted_data = sorted(zip(detected_x_values, detected_buttons))
            if sorted_data:
                unique_data = [sorted_data[0]]
                for i in range(1, len(sorted_data)):
                    if sorted_data[i][0] - unique_data[-1][0] > 10:
                        unique_data.append(sorted_data[i])
                print("Sorted Data:", unique_data)
                # start_time = time.time()
                # print("Time:", start_time)

            if len(unique_data) == 6:
                next_index_to_press = 1

            if count_detection >= 50 or len(unique_data) == 6:
                print("Time:", start_time)
                print("Detected 50 times.")
                break
  
        if count_detection >= 50 or len(unique_data) == 6:
            break 

    # def detect_color(image, color_lower, color_upper):
    #     # แปลงภาพให้เป็นรูปแบบ HSV
    #     hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    #     # สร้าง mask เพื่อกรองสีที่ตรงตามช่วงที่กำหนด
    #     mask = cv2.inRange(hsv, color_lower, color_upper)

    #     # ค้นหา contour ในภาพ mask
    #     contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    #     return contours
    # # กำหนดช่วงของสีที่ต้องการตรวจจับ (ในรูปแบบ HSV)   
    # color_lower = np.array([1, 49, 43])  # สี rgba(91,72,43,255) ในรูปแบบ HSV
    # color_upper = np.array([7, 68, 54])  # สี rgba(136,57,48,255) ในรูปแบบ HSV

         
    # contours = detect_color(img,color_lower,color_upper) 

    # # หากพบสีที่ตรงตามช่วงที่กำหนด 
    # if contours:
    #     pyautogui.press('space')
    #     print("Pressed: space")


    # # ทำการค้นหา spacecheck.png ในภาพ
    # res_spacecheck = cv2.matchTemplate(img, spacecheck_image, cv2.TM_CCOEFF_NORMED)
    # threshold_spacecheck = 0.8
    # loc_spacecheck = np.where(res_spacecheck >= threshold_spacecheck)
    # # กำหนดขนาดที่ต้องการให้ spacecheck_image
    # new_width = 100  # กำหนดความกว้างใหม่ 
    # new_height = 100  # กำหนดความสูงใหม่

    # # ทำการ resize spacecheck_image
    # spacecheck_image_resized = cv2.resize(spacecheck_image, (new_width, new_height))


    # # หากพบภาพ spacecheck.png ในภาพ
    # if loc_spacecheck[0].size > 0:
    #     pyautogui.press('space')
    #     print("Pressed Fund: space")

    cv2.imshow("Image", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
