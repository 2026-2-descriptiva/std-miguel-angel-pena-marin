def pregunta_04():
    """
    Cuente cuántos registros hay en cada mes, usando la fecha de la tercera
    columna (`date`). Represente el mes como un texto de dos dígitos y retorne
    una lista de tuplas `(mes, cantidad)` ordenada por el mes.

    Ejemplo del formato de la respuesta:

        [("01", 3), ("02", 4), ("03", 2), ...]
    """

    import pandas as pd 
    from pathlib import Path
    ruta = Path(__file__).resolve().parent.parent / "data" / "data.csv.gz"
    dt = pd.read_csv(ruta, sep="\t", header=None)
    
    dt['mes'] = dt[2].astype('str').str[5:7]
    return list(dt.groupby('mes').size().items())


