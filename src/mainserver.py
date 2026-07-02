import cv2
import mediapipe as mp
import asyncio
import websockets
import numpy as np
import math

# --- MediaPipe Setup ---
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# --- Global Motor States ---
current_pan_angle = 90  
current_tilt_angle = 90 
current_gripper_angle = 90 # Start open

async def process_camera():
    global current_pan_angle, current_tilt_angle, current_gripper_angle
    cap = cv2.VideoCapture(0) # Try 0 if 1 doesn't work

    while cap.isOpened():
        success, img = cap.read()
        if not success: break

        img = cv2.flip(img, 1)
        h, w, c = img.shape
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        result = hands.process(img_rgb)

        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # --- 1. GET WRIST FOR PAN/TILT ---
                wrist = hand_landmarks.landmark[0]
                wx, wy = wrist.x, wrist.y

                current_tilt_angle = int(np.interp(wy, [0.2, 0.8], [180, 0]))
                current_pan_angle = int(np.interp(wx, [0.2, 0.8], [180, 0]))

                # --- 2. GET FINGERS FOR GRIPPER ---
                thumb_tip = hand_landmarks.landmark[4]
                index_tip = hand_landmarks.landmark[8]

                # Calculate the exact distance between Thumb and Index tip
                # We multiply by 100 just to make the decimals easier to read
                pinch_distance = math.hypot(index_tip.x - thumb_tip.x, index_tip.y - thumb_tip.y) * 100

                # Map the pinch distance to a servo angle
                # If distance is < 3.0 (fingers touching), send 0
                # If distance is > 10.0 (fingers open), send 90
                current_gripper_angle = int(np.interp(pinch_distance, [3.0, 10.0], [0, 90]))

                # --- Display the Data on Screen ---
                cv2.putText(img, f"PAN: {current_pan_angle}", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                cv2.putText(img, f"TILT: {current_tilt_angle}", (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                cv2.putText(img, f"GRIPPER: {current_gripper_angle}", (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 165, 255), 2)
                
                # Draw a line between thumb and index so you can see the pinch working!
                cx, cy = int(thumb_tip.x * w), int(thumb_tip.y * h)
                ix, iy = int(index_tip.x * w), int(index_tip.y * h)
                cv2.line(img, (cx, cy), (ix, iy), (255, 0, 255), 3)

        cv2.imshow("Robot Arm & Gripper", img)
        if cv2.waitKey(1) & 0xFF == ord('q'): break
        await asyncio.sleep(0.01)

    cap.release()
    cv2.destroyAllWindows()

async def websocket_handler(websocket):
    print("\n[SUCCESS] ESP32 Connected!")
    try:
        while True:
            # We now send THREE variables: Pan, Tilt, and Gripper (G)
            message = f"P:{current_pan_angle},T:{current_tilt_angle},G:{current_gripper_angle}"
            await websocket.send(message)
            await asyncio.sleep(0.05) 
    except websockets.exceptions.ConnectionClosed:
        print("\n[WARNING] ESP32 Disconnected.")

async def main():
    server = await websockets.serve(websocket_handler, "0.0.0.0", 8765, ping_interval=None, ping_timeout=None)
    print("Server Started! Waiting for ESP32...")
    await process_camera()

if __name__ == "__main__":
    asyncio.run(main())