import os
from pathlib import Path

# Mapeamento de nomes para nomes padronizados
CLASS_MAP = {
    "earplug": "earplug",
    "goggles": "goggles",
    "hairnet": "hairnet",
    "hair-net": "hairnet",
    "helmet": "helmet",

    "no_earplug": "no_earplug",
    "no_goggles": "no_goggles",
    "no_hairnet": "no_hairnet",
    "no-hairnet": "no_hairnet",
    "no_helmet": "no_helmet",

    "person": "person",
    "head": "person",

    "vest": "vest",
    "apron": "vest",
    "aporn": "vest",

    "no_vest": "no_vest",
    "no-apron": "no_vest",
    "no-aporn": "no_vest",

    "gloves": "gloves",
    "no-gloves": "no_gloves",

    "shoe-cover": "shoe_cover",
    "shoe_cover": "shoe_cover",
    "no-shoe-cover": "no_shoe_cover",
    "no-shoe_cover": "no_shoe_cover",
}

# Lista final das classes
FINAL_CLASSES = [
  'earplug', 'goggles', 'hairnet', 'helmet',
  'no_earplug', 'no_goggles', 'no_hairnet', 'no_helmet',
  'person', 'vest', 'no_vest',
  'gloves', 'no_gloves',
  'shoe_cover', 'no_shoe_cover'
]

# Pastas esperadas
DATA_DIRS = [
    "data/train/labels",
    "data/valid/labels",
    "data/test/labels"
]

def process_label_file(file_path: Path):
    new_lines = []
    with open(file_path, "r") as f:
        for line in f.readlines():
            parts = line.split()
            if len(parts) < 5:
                continue

            class_id = parts[0]
            rest = parts[1:]

            # Ignorar arquivos com ID não numérico
            if not class_id.isdigit():
                continue

            old_class_name = current_classes[int(class_id)]

            # Se classe não está no mapa, descarta
            if old_class_name not in CLASS_MAP:
                print(f"Descartando classe ignorada: {old_class_name}")
                continue

            new_name = CLASS_MAP[old_class_name]

            # Novo índice
            new_id = FINAL_CLASSES.index(new_name)

            new_lines.append(str(new_id) + " " + " ".join(rest) + "\n")

    # Salva corrigido
    with open(file_path, "w") as f:
        f.writelines(new_lines)

if __name__ == "__main__":
    # Detectar classes do dataset base
    base_yaml = Path("deteccao_epi/data.yaml")
    import yaml
    data = yaml.safe_load(open(base_yaml))
    global current_classes
    current_classes = data["names"]

    for d in DATA_DIRS:
        path = Path(d)
        if not path.exists():
            continue

        for txt in path.glob("*.txt"):
            process_label_file(txt)

    print("\n✔ Correção concluída!")
    print("Agora você pode treinar com as classes unificadas.\n")
