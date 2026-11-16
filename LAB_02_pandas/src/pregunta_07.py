def pregunta_07():
    """
    Usando `data/tbl0.tsv`, sume los valores de la columna `c2` para cada
    categoría de la columna `c1`. Retorne una Serie de Pandas cuyo índice son
    las categorías, en orden alfabético, y cuyos valores son las sumas.

    Ejemplo del formato de la respuesta:

        c1
        A    37
        B    36
        C    27
        ...
    """

    import pandas as pd
    from pathlib import Path
    ruta = Path(__file__).resolve().parent.parent / "data" / "tbl0.tsv"

    dt = pd.read_csv(ruta, sep='\t')

    res = dt.groupby('c1')['c2'].sum()

    return res.sort_index()
   


pregunta_07()
