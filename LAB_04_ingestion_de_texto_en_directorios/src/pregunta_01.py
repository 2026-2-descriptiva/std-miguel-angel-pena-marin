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

    import glob
    import pandas as pd
    from pathlib import Path
    import os

    train = []
    test = []
    ruta = Path(__file__).resolve().parent.parent
    archivos1 = glob.glob(f"{ruta}/data/test/*/*.txt", recursive = True)
    archivos2 = glob.glob(f"{ruta}/data/train/*/*.txt", recursive = True)
    for ruta in archivos1:
        with open(ruta) as f:
            frase = f.read().strip()
        emocion = os.path.basename(os.path.dirname(ruta))
        test.append({'phrase': frase, 'target': emocion})
    for ruta in archivos2:
        with open(ruta) as f:
            frase = f.read().strip()
        emocion = os.path.basename(os.path.dirname(ruta))
        train.append({'phrase': frase, 'target': emocion})

    

    test_dt = pd.DataFrame(test)
    train_dt = pd.DataFrame(train)
    raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    test_dt.to_csv(os.path.join(raiz, "submission", "test_dataset.csv"), index= False)
    train_dt.to_csv(os.path.join(raiz, "submission", "train_dataset.csv"), index= False)
    
    

pregunta_01()
