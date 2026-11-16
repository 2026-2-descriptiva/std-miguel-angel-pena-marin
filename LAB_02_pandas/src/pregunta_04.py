def pregunta_04():
    """
    Usando `data/tbl0.tsv`, calcule el promedio de la columna `c2` para cada
    categoría de la columna `c1`. Retorne una Serie de Pandas cuyo índice son
    las categorías, en orden alfabético, y cuyos valores son los promedios.

    Ejemplo del formato de la respuesta:

        c1
        A    4.6250
        B    5.1429
        C    5.4000
        ...
    """

    import pandas as pd
    from pathlib import Path
    ruta = Path(__file__).resolve().parent.parent / "data" / "tbl0.tsv"

    dt = pd.read_csv(ruta, sep='\t')

    res = dt.groupby('c1')['c2'].mean()

    return res.sort_index()


pregunta_04()
    