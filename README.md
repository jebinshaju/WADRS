

# Wild Animal Detection and Repellent System

**Disclaimer:** This is a **dummy project** created for college purposes. It demonstrates setting up a basic wild animal detection and repellent system using YOLOv8, a webcam, and a Telegram bot for notifications. The system is not intended for real-world deployment.

## Project Overview

The Wild Animal Detection and Repellent System uses a YOLOv8 model to detect wild animals in real-time through a webcam feed. When a wild animal is detected, the system sends an alert to a specified Telegram chat and plays a warning sound to repel the animal.

## Features

- **Real-time detection:** Detects wild animals such as elephants, lions, tigers, and more using a webcam feed.
- **Alerts:** Sends an alert message and photo to a Telegram chat if a wild animal is detected.
- **Sound Repellent:** Plays a warning sound when an animal is detected to repel it.
- **Runs on Raspberry Pi:** Optimized to run on Raspberry Pi for real-time processing and alerting.

## Prerequisites

Make sure you have the following installed on your system:

- Python 3.x
- OpenCV
- PyGame
- Ultralytics YOLO
- Telegram Python SDK
- python-dotenv
- asyncio
- YOLOv8 model weights (`yolov8l.pt`)

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/wild-animal-detection-system.git
cd wild-animal-detection-system
```

### 2. Install the Required Packages

```bash
pip install -r requirements.txt
```

### 3. Create and Configure `.env` File

Create a `.env` file in the project directory with the following content:

```env
# Telegram Bot Configuration
TELEGRAM_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_telegram_chat_id

# YOLO Model Path
YOLO_MODEL_PATH=yolov8l.pt

# Sound File Path
SOUND_FILE_PATH=tiger_roar.mp3
```

Replace `your_telegram_bot_token` and `your_telegram_chat_id` with your actual Telegram bot token and chat ID. 

### 4. Set Up the YOLOv8 Model

You can download the YOLOv8 models from the Ultralytics repository. Make sure to place the model file (`yolov8l.pt`) in the project directory.

| Model Version | Download Link                                                                                          | Model Size | Suitable for         |
|---------------|-------------------------------------------------------------------------------------------------------|------------|-----------------------|
| YOLOv8n       | [Download](https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8n.pt)                 | 6.2 MB     | Raspberry Pi          |
| YOLOv8s       | [Download](https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8s.pt)                 | 14.5 MB    | Raspberry Pi          |
| YOLOv8m       | [Download](https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8m.pt)                 | 25.9 MB    | More capable systems  |
| YOLOv8l       | [Download](https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8l.pt)                 | 46.2 MB    | High performance      |
| YOLOv8x       | [Download](https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8x.pt)                 | 88.7 MB    | High performance      |

**Note:** For Raspberry Pi, it is recommended to use `yolov8n.pt` or `yolov8s.pt` for faster performance due to limited resources.

### 5. Prepare the Sound File

Make sure to have a sound file (`tiger_roar.mp3`) placed in the project directory. This sound will play whenever a wild animal is detected to help repel it.

### 6. Running the Script

Run the following command to start the application:

```bash
python wild_animal_detection.py
```

The script will start accessing your webcam feed, and upon detecting any wild animal, it will play the warning sound and send an alert message to your configured Telegram chat.

## Running on Raspberry Pi

To run this application on a Raspberry Pi, you need to:

1. Install OpenCV on Raspberry Pi using the following guide: [Install OpenCV on Raspberry Pi](https://www.pyimagesearch.com/2018/09/19/pip-install-opencv/)
2. Choose a smaller model version (`yolov8n.pt` or `yolov8s.pt`) to ensure faster processing on Raspberry Pi.
3. Use the following command to install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

**Note:** Ensure that your Raspberry Pi has the required dependencies installed, and it is recommended to use a Raspberry Pi 4 or better for this real-time detection application.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE)
