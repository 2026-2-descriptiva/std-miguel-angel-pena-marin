def pregunta_02():
    """
    Cuente cuántos registros hay para cada letra de la primera columna
    (`letter`). Retorne una lista de tuplas `(letra, cantidad)` ordenada
    alfabéticamente por la letra.

    Ejemplo del formato de la respuesta:

        [("A", 8), ("B", 7), ("C", 5), ...]
    """
    import pandas as pd 
    from pathlib import Path
    ruta = Path(__file__).resolve().parent.parent / "data" / "data.csv.gz"
    dt = pd.read_csv(ruta, sep="\t", header=None)
    
    dt2 = dt.groupby(0).size()
    return list(dt2.items())
