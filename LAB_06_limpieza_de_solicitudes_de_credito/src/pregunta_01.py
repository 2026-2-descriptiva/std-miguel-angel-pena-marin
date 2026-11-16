def pregunta_01():
    """
    El archivo `data/solicitudes_de_credito.csv.gz` contiene las solicitudes de
    un programa de crédito, pero llegó sucio: tiene una columna de índice que
    no pertenece a los datos, registros duplicados, registros incompletos y
    valores que representan lo mismo escritos de formas distintas en los
    campos de texto, las fechas, el estrato y el monto.

    Su tarea es limpiarlo y guardar el resultado en
    `submission/solicitudes_de_credito.csv`, usando punto y coma (`;`) como
    separador y sin el índice de Pandas.

    El archivo limpio debe cumplir lo siguiente:

    - Contiene solamente las nueve columnas `sexo`, `tipo_de_emprendimiento`,
      `idea_negocio`, `barrio`, `estrato`, `comuna_ciudadano`,
      `fecha_de_beneficio`, `monto_del_credito` y `línea_credito`, en ese
      orden.
    - Los campos de texto están en minúsculas y sus palabras separadas por
      espacios.
    - `estrato` y `monto_del_credito` son números enteros, sin símbolos ni
      separadores de miles.
    - Todas las fechas de `fecha_de_beneficio` usan un mismo formato, por
      ejemplo `AAAA-MM-DD`.
    - No hay registros incompletos. La única excepción es
      `comuna_ciudadano`: sus valores faltantes son parte de los datos
      originales y deben conservarse.
    - No hay registros duplicados.

    Ejemplo del formato del archivo:

        sexo;tipo_de_emprendimiento;idea_negocio;barrio;estrato;...
        femenino;comercio;almacen de ropa en;los cerros el vergel;2;...
        ...
    """

    import json
    import os
    import pandas as pd
    from pathlib import Path
    ruta = Path(__file__).resolve().parent.parent / "data" / "solicitudes_de_credito.csv.gz"

    dt = pd.read_csv(ruta, sep=';')

    dt.drop(columns=['Unnamed: 0'], inplace=True)

    minus = ['sexo', 'tipo_de_emprendimiento', 'idea_negocio', 'barrio', 'línea_credito']

    for i in minus:
        dt[i] = dt[i].str.lower().str.replace(r"[_\-]+", " ", regex=True).str.replace(r"\s+", " ", regex=True).str.strip() 

    enteros = ['estrato', 'monto_del_credito']

    revisar = [c for c in dt.columns if c != "comuna_ciudadano"]
    dt = dt.dropna(subset=revisar)
    
    for i in enteros:
        dt[i] = pd.to_numeric(
        dt[i].astype(str).str.replace(r"[^\d.\-]", "", regex=True),
        errors="coerce"
        )
        dt[i] = dt[i].astype(int)

    def parsear(col):
        col = col.astype(str).str.strip()
        res = pd.Series(pd.NaT, index=col.index)
        for f in ["%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y", "%Y/%m/%d"]:
            pend = res.isna()
            res[pend] = pd.to_datetime(col[pend], format=f, errors="coerce")
        return res

    dt["fecha_de_beneficio"] = parsear(dt["fecha_de_beneficio"]).dt.strftime("%Y-%m-%d")

    dt = dt.drop_duplicates()

    ruta = Path(__file__).resolve().parent.parent
    dt.to_csv(os.path.join(ruta, "submission", "solicitudes_de_credito.csv"), index= False, sep=';')




pregunta_01()
