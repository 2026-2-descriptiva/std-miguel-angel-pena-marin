from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "submission"

SPLITS = ("train", "test")
COLUMNS = ["phrase", "target"]


def load_split(split_dir: Path) -> pd.DataFrame:
    """Lee todas las frases de un split y las etiqueta con el nombre de su carpeta."""
    records = [
        {
            "phrase": file.read_text(encoding="utf-8").strip(),
            "target": label_dir.name,
        }
        for label_dir in sorted(split_dir.iterdir())
        if label_dir.is_dir()
        for file in sorted(label_dir.glob("*.txt"))
    ]
    return pd.DataFrame(records, columns=COLUMNS)


def pregunta_01():
    """
    Las frases de este laboratorio no están en una tabla, sino en miles de
    archivos de texto organizados en carpetas. Dentro de `data/` hay dos
    carpetas, `train/` y `test/`, y cada una contiene las carpetas
    `negative/`, `neutral/` y `positive/`. Cada archivo `.txt` contiene una
    frase, y la carpeta donde se encuentra indica su sentimiento.

    Su tarea es construir un dataset para cada división y guardarlo en:

    - `submission/train_dataset.csv`
    - `submission/test_dataset.csv`

    Cada archivo debe tener dos columnas: `phrase`, con el texto de la frase,
    y `target`, con el nombre de la carpeta de sentimiento (`negative`,
    `neutral` o `positive`). Recorra las carpetas y los archivos en orden
    alfabético, de modo que el resultado sea siempre el mismo. No guarde el
    índice de Pandas en el CSV.

    Ejemplo del formato de cada archivo:

        phrase,target
        "The real estate company posted a net loss ...",negative
        ...
        "Cardona slowed her vehicle , turned around ...",neutral
        ...
    """

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for split in SPLITS:
        dataset = load_split(DATA_DIR / split)
        dataset.to_csv(OUTPUT_DIR / f"{split}_dataset.csv", index=False)