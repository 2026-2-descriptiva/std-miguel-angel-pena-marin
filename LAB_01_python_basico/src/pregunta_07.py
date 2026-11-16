def pregunta_07():
    """
    Para cada valor distinto de la segunda columna (`value`), construya la
    lista de letras de la primera columna (`letter`) que aparecen con ese
    valor. Conserve las letras repetidas y el orden en que aparecen en el
    archivo. Retorne una lista de tuplas `(valor, letras)` ordenada por el
    valor.

    Ejemplo del formato de la respuesta:

        [(0, ["C"]), (1, ["E", "B", "E"]), (2, ["A", "E"]), ...]
    """
    import pandas as pd 
    from pathlib import Path
    ruta = Path(__file__).resolve().parent.parent / "data" / "data.csv.gz"
    dt = pd.read_csv(ruta, sep="\t", header=None)

    dt2 = dt.groupby(1)[0].agg(list)
    
    
    return [(valor, letras) for valor, letras in dt2.items()]


print(pregunta_07())