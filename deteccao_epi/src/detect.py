import tkinter as tk
from tkinter import messagebox, scrolledtext
from ultralytics import YOLO
import cv2
import os
from datetime import datetime

# Caminho do modelo
MODEL_PATH = r"C:\Users\glaug\Desktop\glaugYoloV8\runs\detect\train8\weights\best.pt"

# Lista final de classes (vest agora é person)
CLASSES = ['earplug', 'goggles', 'hairnet', 'helmet', 'no_earplug', 'no_goggles',
           'no_hairnet', 'no_helmet', 'person']

VEST_CLASS_ID = 9  # posição original substituída por person

# Verifica modelo
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError("Modelo YOLO não encontrado!")

model = YOLO(MODEL_PATH)
model.names[VEST_CLASS_ID] = "person"

# Traduções + ícones visuais
CLASS_LABELS = {
    'person':      '👤 Pessoa',
    'helmet':      '⛑️ Capacete',
    'no_helmet':   '❌ Sem Capacete',
    'goggles':     '🥽 Óculos de Proteção',
    'no_goggles':  '❌ Sem Óculos',
    'earplug':     '🎧 Protetor Auricular',
    'no_earplug':  '❌ Sem Protetor Auricular',
    'hairnet':     '🧢 Touca/Rede',
    'no_hairnet':  '❌ Sem Touca/Rede'
}


# ---------------------- FUNÇÃO DE DETECÇÃO ----------------------
def iniciar_detect():
    selecionadas = [cl for cl, var in checkbox_vars.items() if var.get() == 1]
    if not selecionadas:
        messagebox.showwarning("Atenção", "Selecione ao menos um item para monitorar.")
        return

    registrar_log(f"▶ Iniciando detecção para: {', '.join(selecionadas)}")

    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        results = model.track(frame, conf=0.30, iou=0.5, persist=True, verbose=False)

        for r in results:
            if not hasattr(r, "boxes"):
                continue

            for box in r.boxes:
                cls_id = int(box.cls)
                cls_name = model.names[cls_id]

                if cls_id == VEST_CLASS_ID:
                    cls_name = "person"

                if cls_name in selecionadas:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(frame, cls_name, (x1, y1 - 5),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

                    registrar_log(f"✔ Detectado: {cls_name}")

        cv2.imshow("Monitoramento de EPIs - Pressione Q para sair", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            registrar_log("⏹ Detecção finalizada pelo usuário.")
            break

    cap.release()
    cv2.destroyAllWindows()


# ---------------------- SISTEMA DE LOG ----------------------
def registrar_log(msg):
    timestamp = datetime.now().strftime("%H:%M:%S")
    logs_box.insert(tk.END, f"[{timestamp}] {msg}\n")
    logs_box.see(tk.END)


# ---------------------- INTERFACE ----------------------
root = tk.Tk()
root.title("🛡 Monitoramento de EPIs - IA em Tempo Real")
root.geometry("880x690")
root.configure(bg="#0D1117")
root.resizable(False, False)

# HEADER
header = tk.Label(root, text="🛡 Monitoramento Inteligente de EPIs",
                  bg="#161B22", fg="#58A6FF",
                  font=("Segoe UI", 20, "bold"), pady=15)
header.pack(fill="x")

# FRAME PRINCIPAL
frame = tk.Frame(root, bg="#0D1117")
frame.pack(fill="both", expand=True, padx=20, pady=10)

# LADO ESQUERDO → SELEÇÃO DE EPIs
left = tk.LabelFrame(frame, text=" EPIs Monitorados ",
                     bg="#0D1117", fg="#E6EDF3",
                     font=("Segoe UI", 11, "bold"), padx=10, pady=10)
left.pack(side="left", fill="y", padx=(0, 15))

checkbox_vars = {}

for i, item in enumerate(CLASSES):
    var = tk.IntVar()
    cb = tk.Checkbutton(
        left, text=CLASS_LABELS.get(item, item), variable=var,
        bg="#0D1117", fg="#C9D1D9", selectcolor="#21262D",
        activebackground="#0D1117", font=("Segoe UI", 11),
        cursor="hand2"
    )
    cb.pack(anchor="w", pady=3)
    checkbox_vars[item] = var

# Botão principal
btn_detect = tk.Button(left, text="▶ INICIAR DETECÇÃO",
                       command=iniciar_detect,
                       bg="#238636", fg="white",
                       font=("Segoe UI", 13, "bold"),
                       padx=20, pady=10, cursor="hand2")
btn_detect.pack(fill="x", pady=15)


# LADO DIREITO → LOGS
right = tk.LabelFrame(frame, text=" Logs e Eventos ",
                      bg="#0D1117", fg="#E6EDF3",
                      font=("Segoe UI", 11, "bold"), padx=10, pady=10)
right.pack(side="right", fill="both", expand=True)

logs_box = scrolledtext.ScrolledText(right, bg="#0D1117", fg="#00FF9F",
                                     font=("Consolas", 10), height=20)
logs_box.pack(fill="both", expand=True)


# Footer
footer = tk.Label(root, text="Pressione Q na janela de vídeo para encerrar a detecção",
                  bg="#161B22", fg="#8B949E",
                  font=("Segoe UI", 9), pady=8)
footer.pack(fill="x")

root.mainloop()
