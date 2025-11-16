from ultralytics import YOLO

model = YOLO(r"C:\Users\glaug\Desktop\glaugYoloV8\runs\detect\train8\weights\best.pt")
print(model.names)