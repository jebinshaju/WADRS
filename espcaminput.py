import cv2
import numpy as np
import pygame
from ultralytics import YOLO
import telegram
import asyncio
import tempfile
import os
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv()
telegram_token = os.getenv('TELEGRAM_TOKEN')
chat_id = os.getenv('TELEGRAM_CHAT_ID')
sound_file_path = os.getenv('SOUND_FILE_PATH')
yolo_model_path = os.getenv('YOLO_MODEL_PATH')

# Initialize Telegram bot and YOLO model
bot = telegram.Bot(token=telegram_token)
model = YOLO(yolo_model_path)
pygame.mixer.init()

# Connect to ESP32-CAM stream
esp32_cam_url = "http://192.168.195.187/capture.jpg"
dangerous_animals = ['dog', 'elephant', 'wild elephant', 'lion', 'tiger', 'bear', 'pig']
animal_in_frame = False

# Function to send Telegram alerts
async def send_telegram_message(message, image_path=None):
    async with bot:
        if image_path:
            with open(image_path, 'rb') as img:
                await bot.send_photo(chat_id=chat_id, photo=img, caption=message)
        else:
            await bot.send_message(chat_id=chat_id, text=message)

# Main detection loop
async def main_loop():
    global animal_in_frame
    while True:
        try:
            # Capture image from ESP32-CAM
            resp = requests.get(esp32_cam_url, timeout=5)
            resp.raise_for_status()
            img_np = np.frombuffer(resp.content, np.uint8)
            frame = cv2.imdecode(img_np, cv2.IMREAD_COLOR)
        except (requests.RequestException, cv2.error) as e:
            print(f"Camera connection issue: {e}")
            continue

        # Detect animals in frame
        results = model(frame)
        detected_animals = []

        for result in results:
            for box in result.boxes:
                class_id = int(box.cls[0])
                label = model.names[class_id]
                confidence = box.conf[0].item()

                if confidence > 0.5 and label in dangerous_animals:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                    cv2.putText(frame, f'{label} {confidence:.2f}',
                                (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX,
                                0.5, (0, 0, 255), 2)
                    detected_animals.append(label)

        # Alert if dangerous animals are detected
        if detected_animals and not animal_in_frame:
            message = f"Danger detected: {', '.join(detected_animals)}."
            with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as img_file:
                cv2.imwrite(img_file.name, frame)
                img_path = img_file.name

            pygame.mixer.music.load(sound_file_path)
            pygame.mixer.music.play()

            try:
                await send_telegram_message(message, img_path)
            except telegram.error.TelegramError as e:
                print(f"Telegram error: {e}")
            finally:
                if os.path.exists(img_path):
                    os.remove(img_path)

            animal_in_frame = True

        # Reset flag if no animals detected
        if not detected_animals:
            animal_in_frame = False

        # Display frame
        cv2.imshow('Animal Detection', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()

# Run detection loop
if __name__ == "__main__":
    asyncio.run(main_loop())

