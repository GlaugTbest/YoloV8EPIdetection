from ultralytics import YOLO

def main():

    # Carrega a arquitetura limpa, sem pesos COCO
    # Isso garante que NÃO existam classes como "bed", "car", "dog" etc.
    model = YOLO("yolov8n.yaml")  

    model.train(
        data="deteccao_epi/data.yaml",  # caminho do dataset
        epochs=100,                     # recomendado para EPIs
        imgsz=640,
        batch=16,                       # aumenta a estabilidade do treino
        device=0,                       # GPU (GTX 1660 Super)
        workers=4,                      # acelera o carregamento
        pretrained=False                # impede pesos COCO
    )

if __name__ == "__main__":
    main()
