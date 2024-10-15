import cv2
import numpy as np
import pygame
from ultralytics import YOLO
import telegram
import asyncio
import tempfile
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize Telegram bot using environment variables
telegram_token = os.getenv('TELEGRAM_TOKEN')
chat_id = os.getenv('TELEGRAM_CHAT_ID')
bot = telegram.Bot(token=telegram_token)

# Load the YOLO model
model = YOLO(os.getenv('YOLO_MODEL_PATH'))  # Load model path from .env

# Initialize Pygame for sound playback
pygame.mixer.init()

# Open webcam
cap = cv2.VideoCapture(0)

# Global variable to track if an animal is in the frame
animal_in_frame = False

# List of dangerous animals to detect
dangerous_animals = ['dog', 'elephant', 'wild elephant', 'lion', 'tiger', 'bear', 'pig']

async def send_telegram_message(message, image_path=None):
    async with bot:
        if image_path:
            with open(image_path, 'rb') as image_file:
                await bot.send_photo(chat_id=chat_id, photo=image_file, caption=message)
        else:
            await bot.send_message(chat_id=chat_id, text=message)

async def main_loop():
    global animal_in_frame
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        results = model(frame)

        for result in results:
            boxes = result.boxes.cpu().numpy()
            for box in boxes:
                class_id = int(box.cls[0])
                label = model.names[class_id]
                confidence = box.conf[0]

                if confidence > 0.5 and label in dangerous_animals:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                    cv2.putText(frame, f'{label} {confidence:.2f}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

                    if not animal_in_frame:
                        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as temp_image_file:
                            cv2.imwrite(temp_image_file.name, frame)
                            temp_image_path = temp_image_file.name

                        pygame.mixer.music.load(os.getenv('SOUND_FILE_PATH'))  # Load sound file from .env
                        pygame.mixer.music.play()  # Play sound

                        await send_telegram_message(f"Alert: A {label} has entered the premises.", temp_image_path)
                        print("\n\n\nMessage sent\n\n\n\n")
                        animal_in_frame = True

                        os.remove(temp_image_path)

        if animal_in_frame and not any(model.names[box.cls[0]] in dangerous_animals for box in result.boxes.cpu().numpy()):
            animal_in_frame = False

        cv2.imshow('Frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    asyncio.run(main_loop())

