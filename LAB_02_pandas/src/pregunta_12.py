def pregunta_12():
    """
    En `data/tbl2.tsv`, cada valor de la columna `c0` aparece en varias
    filas. Construya un DataFrame con una fila por cada valor de `c0`, en
    orden ascendente, y las columnas `c0` y `c5`. En `c5`, forme un texto
    `c5a:c5b` para cada fila de ese `c0`, ordene esos textos alfabéticamente y
    únalos separados por comas.

    Ejemplo del formato de la respuesta:

            c0                             c5
        0    0  bbb:0,ddd:9,ggg:8,hhh:2,jjj:3
        1    1        aaa:3,ccc:2,ddd:0,hhh:9
        2    2        ccc:6,ddd:2,ggg:5,jjj:1
        ...
    """

    import pandas as pd
    from pathlib import Path
    ruta = Path(__file__).resolve().parent.parent / "data" / "tbl2.tsv"

    dt = pd.read_csv(ruta, sep='\t')

    dt['aux'] = dt['c5a'] + ':' + dt['c5b'].astype('str') 
    
    res = dt.groupby('c0')['aux'].apply(lambda X: ','.join(v for v in sorted(X))).reset_index()


    res.columns = ['c0', 'c5']

    return res

pregunta_12()
