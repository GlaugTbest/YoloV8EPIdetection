from ultralytics import YOLO
import cv2
import os

# CAMINHO DO MODELO TREINADO
model_path = r"C:\Users\glaug\Desktop\glaugYoloV8\runs\detect\train6\weights\best.pt"

# MODELO EXISTE?
if not os.path.exists(model_path):
    raise FileNotFoundError(f"Modelo não encontrado em: {model_path}")


model = YOLO(model_path)


cap = cv2.VideoCapture(0)

if not cap.isOpened():
    raise IOError("Não foi possível acessar a webcam")


while True:
    ret, frame = cap.read()
    if not ret:
        print("Falha ao capturar frame da webcam")
        break

  
    results = model.track(source=frame, conf=0.25, verbose=False)


    annotated_frame = results[0].plot()
    cv2.imshow("Detecção EPI - Webcam", annotated_frame)

   #PRESSIONE Q PRA FECHAR A TELA
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Finaliza recursos
cap.release()
cv2.destroyAllWindows()
