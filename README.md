EPI Detection System using YOLOv8
A real-time Personal Protective Equipment (PPE) detection system designed for industrial environments, specifically targeting water bottling and food processing facilities. This application uses YOLOv8 for computer vision tasks and provides a modern graphical interface for monitoring compliance with safety equipment regulations.
Features

Real-time Detection: Monitors live webcam feed for PPE compliance
Multi-class Detection: Identifies 9 different PPE categories including:

Person detection
Helmet (present/absent)
Safety goggles (present/absent)
Ear protection (present/absent)
Hairnet/cap (present/absent)


Selective Monitoring: Choose which PPE items to track via checkbox interface
Event Logging: Real-time log system displaying all detection events with timestamps
Modern UI: Clean, dark-themed interface built with Tkinter

Technical Details

Model: YOLOv8 custom-trained model
Framework: Ultralytics YOLO
Interface: Python Tkinter
Computer Vision: OpenCV (cv2)
Confidence Threshold: 0.30
IOU Threshold: 0.5

Model Architecture
The system uses a custom YOLOv8 model trained on industrial PPE datasets. The model includes class fusion logic where vest detections are automatically merged with person detections for simplified tracking.
Requirements
ultralytics
opencv-python
tkinter (included with Python)
Usage

Ensure your trained YOLOv8 model is placed at the specified path
Run the application
Select which PPE items you want to monitor
Click "Start Detection" to begin real-time monitoring
Press 'Q' in the video window to stop detection

Model Training
The model was trained using YOLOv8's training pipeline with custom annotations for industrial safety equipment. Training parameters and dataset details can be found in the training configuration files.
Use Cases

Manufacturing facility safety compliance
Food processing plant monitoring
Construction site safety verification
Warehouse safety auditing
Real-time safety protocol enforcement
