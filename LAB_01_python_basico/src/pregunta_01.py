def pregunta_01():
    """
    Calcule la suma de los valores de la segunda columna (`value`) del
    archivo `data/data.csv.gz` y retorne el resultado como un número entero.

    Ejemplo del formato de la respuesta:

        214
    """
    
    import pandas as pd 
    from pathlib import Path
    ruta = Path(__file__).resolve().parent.parent / "data" / "data.csv.gz"
    dt = pd.read_csv(ruta, sep="\t", header=None)
    valor = sum(dt[1])


    return valor


pregunta_01()