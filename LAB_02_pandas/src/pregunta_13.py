def pregunta_13():
    """
    Combine las tablas `data/tbl0.tsv` y `data/tbl2.tsv` usando la columna
    `c0`, que ambas comparten. Luego, sume los valores de la columna `c5b`
    para cada categoría de la columna `c1`. Retorne una Serie de Pandas cuyo
    índice son las categorías, en orden alfabético, y cuyos valores son las
    sumas.

    Ejemplo del formato de la respuesta:

        c1
        A    146
        B    134
        C     81
        ...
    """

    import pandas as pd
    from pathlib import Path
    ruta = Path(__file__).resolve().parent.parent / "data" / "tbl0.tsv"
    ruta2 = Path(__file__).resolve().parent.parent / "data" / "tbl2.tsv"

    dt = pd.read_csv(ruta, sep='\t')
    dt2 = pd.read_csv(ruta2, sep='\t')


    dt = dt.merge(dt2, on="c0")
    res = dt.groupby('c1')['c5b'].sum()

    return res

pregunta_13()