from ultralytics import YOLO

def main():

    # Carrega a arquitetura limpa, sem pesos COCO
    # Isso garante que NÃO existam classes como "bed", "car", "dog" etc.
    model = YOLO("yolov8n.yaml")  # ou yolov8s.pt se tiver mais GPU

    model.train(
        data="deteccao_epi/data.yaml",
        epochs=200,
        imgsz=640,
        batch=4,
        device=0,
        pretrained=False,
        patience=20,       # para se parar de evoluir antes do fim
        save_period=10,    # salva pesos a cada 10 épocas
    )
if __name__ == "__main__":
    main()
