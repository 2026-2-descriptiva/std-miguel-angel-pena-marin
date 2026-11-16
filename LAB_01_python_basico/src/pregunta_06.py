def pregunta_06():
    """
    La quinta columna (`metrics`) contiene pares `clave:valor` separados por
    comas. Para cada clave, encuentre el valor mínimo y el valor máximo que
    aparecen en todo el archivo. Retorne una lista de tuplas
    `(clave, mínimo, máximo)` ordenada alfabéticamente por la clave.

    Observe que el orden es mínimo y luego máximo, al contrario de la
    pregunta 5.

    Ejemplo del formato de la respuesta:

        [("aaa", 1, 9), ("bbb", 1, 9), ...]
    """
    import pandas as pd 
    from pathlib import Path
    ruta = Path(__file__).resolve().parent.parent / "data" / "data.csv.gz"
    dt = pd.read_csv(ruta, sep="\t", header=None)
    dt2 = dt[4].astype('str').str.split(",").explode()
    dt2 = dt2.str.split(':', expand=True)
    dt2[1] = dt2[1].astype('int')
    dt2 = dt2.groupby(0)[1].agg(['min', 'max'])
   
    return [(letra, fila['min'], fila['max']) for letra, fila in dt2.iterrows()]

print(pregunta_06())