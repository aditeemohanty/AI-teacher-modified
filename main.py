import cvzone
import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np
import google.generativeai as genai
from PIL import Image
import streamlit as st

# Initialize the HandDetector globally
detector = HandDetector(staticMode=False, maxHands=1, modelComplexity=1, detectionCon=0.7, minTrackCon=0.5)

def run_math_gesture():
    try:
        st.set_page_config(layout="wide")
        st.image('maths gesture.png')
        
        col1, col2 = st.columns([3, 2])
        with col1:
            run = st.checkbox('Run', value=True)
            FRAME_WINDOW = st.image([])

        with col2:
            st.title("Answer")
            output_text_area = st.subheader("")

        genai.configure(api_key="YOUR-API-KEY")
        model = genai.GenerativeModel('gemini-1.5-flash')

        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            st.error("Could not open webcam. Please check your camera connection.")
            return

        cap.set(3, 1280)
        cap.set(4, 720)

        prev_pos = None
        canvas = None
        image_combined = None
        output_text = ""

        while run:
            success, img = cap.read()
            if not success:
                break
            
            img = cv2.flip(img, 1)

            if canvas is None:
                canvas = np.zeros_like(img)

            info = getHandInfo(img)
            if info:
                fingers, lmList = info
                prev_pos, canvas = draw(info, prev_pos, canvas, img)
                output_text = sendToAI(model, canvas, fingers)

            image_combined = cv2.addWeighted(img, 0.7, canvas, 0.3, 0)
            FRAME_WINDOW.image(image_combined, channels="BGR")

            if output_text:
                output_text_area.text(output_text)

            cv2.waitKey(1)

        cap.release()

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        if 'cap' in locals():
            cap.release()

def getHandInfo(img):
    # Find hands in the current frame
    # The 'draw' parameter draws landmarks and hand outlines on the image if set to True
    # The 'flipType' parameter flips the image, making it easier for some detections
    hands, img = detector.findHands(img, draw=False, flipType=True)

    # Check if any hands are detected
    if hands:
        # Information for the first hand detected
        hand = hands[0]  # Get the first hand detected
        lmList = hand["lmList"]  # List of 21 landmarks for the first hand
        # Count the number of fingers up for the first hand
        fingers = detector.fingersUp(hand)
        print(fingers)
        return fingers, lmList
    else:
        return None


def draw(info, prev_pos, canvas, img):
    fingers, lmList = info
    current_pos = None
    if fingers == [0, 1, 0, 0, 0]:
        current_pos = lmList[8][0:2]
        if prev_pos is None: prev_pos = current_pos
        cv2.line(canvas, current_pos, prev_pos, (255, 0, 255), 10)
    elif fingers == [1, 0, 0, 0, 0]:
        canvas = np.zeros_like(img)

    return current_pos, canvas


def sendToAI(model, canvas, fingers):
    if fingers == [1, 1, 1, 1, 0]:
        pil_image = Image.fromarray(canvas)
        response = model.generate_content(["Solve this math problem", pil_image])
        return response.text


if __name__ == "__main__":
    run_math_gesture()
