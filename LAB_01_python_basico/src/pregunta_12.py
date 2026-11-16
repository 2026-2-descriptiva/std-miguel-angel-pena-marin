def pregunta_12():
    """
    Para cada letra de la primera columna (`letter`), sume todos los valores
    numéricos de los pares `clave:valor` de la quinta columna (`metrics`).
    Retorne un diccionario `{letra: suma}` con las letras en orden alfabético.

    Ejemplo del formato de la respuesta:

        {"A": 177, "B": 187, "C": 114, ...}
    """

    import pandas as pd 
    from pathlib import Path
    ruta = Path(__file__).resolve().parent.parent / "data" / "data.csv.gz"
    dt = pd.read_csv(ruta, sep="\t", header=None)
    dt[4] = dt[4].astype('str').str.split(',')
    dt2 = dt[[4]].explode(4)
    dt2[4] = dt2[4].apply(lambda x: x[4:])
    dt2['letra'] = dt[0]
    dt2[4] = dt2[4].astype('int')

    dic = dict(dt2.groupby('letra')[4].sum())


    return dic 
    
    


pregunta_12()