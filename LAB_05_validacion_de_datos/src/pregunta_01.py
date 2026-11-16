def main():
    """
    Antes de limpiar o analizar un conjunto de datos, un analista debe
    documentar qué problemas tiene. En este laboratorio usted no va a limpiar
    `data/ventas.csv.gz`: va a construir un reporte de calidad que deje evidencia
    de sus problemas, tal como están en el archivo.

    Lea `data/ventas.csv.gz` sin modificar sus valores. Para trabajar con los
    encabezados, normalícelos: páselos a minúsculas, elimine los espacios al
    inicio y al final (y cualquier marca BOM) y reemplace los espacios
    internos por `_`. Las columnas requeridas son `supplier_id`, `supplier`,
    `country`, `city`, `purchase_date`, `amount`, `discount`, `weight`,
    `units`, `unit_price` y `contact_email`.

    Escriba el reporte en `submission/data_quality_report.json` con estas
    claves:

    - `row_count`: cantidad de filas de datos.
    - `column_count`: cantidad de columnas.
    - `missing_required_columns`: lista ordenada de columnas requeridas que no
      están en el archivo.
    - `unexpected_columns`: lista ordenada de columnas del archivo que no son
      requeridas.
    - `duplicate_row_count`: cantidad de filas idénticas a una fila anterior.
    - `duplicate_supplier_id_row_count`: cantidad de filas cuyo `supplier_id`
      aparece más de una vez (cuente todas esas filas, no solo las
      repetidas).
    - `missing_value_count_by_column`: diccionario con la cantidad de valores
      faltantes de cada columna. Considere faltantes las celdas vacías y las
      que contienen `N/A`.
    - `invalid_email_count`: cantidad de valores de `contact_email` que no
      tienen la forma `usuario@dominio.extension`.
    - `invalid_unit_count`: cantidad de valores numéricos de `units` que no son
      enteros positivos. Los valores faltantes no se cuentan aquí.
    - `country_values`: lista ordenada de los valores distintos de `country`,
      escritos exactamente como aparecen en el archivo.

    La función también debe retornar el reporte como un diccionario.

    Ejemplo del formato del reporte:

        {
          "row_count": 103,
          "column_count": 11,
          "missing_required_columns": [],
          ...
          "country_values": [" Colombia ", "CO", ...]
        }
    """
    import json
    import pandas as pd
    from pathlib import Path
    ruta = Path(__file__).resolve().parent.parent / "data" / "ventas.csv.gz"

    dt = pd.read_csv(ruta, sep=',')
    dt.columns = ['supplier_id','supplier','country','city','purchase_date','amount','discount','weight','units','unit_price','contact_email']

    columnas_req = [
    "supplier_id", "supplier",
    "country", "city", "purchase_date", "amount", "discount", "weight",
    "units", "unit_price", "contact_email"
    ]

    duplicados = dt.duplicated().sum()
    duplicados_id_supp = dt['supplier_id'].duplicated(keep=False).sum()


    dic =  {}

    for col in dt.columns:
        dic[col] = int(dt[col].isna().sum())

    patron = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    dominios_malos = int((~dt["contact_email"].str.match(patron, na=False)).sum())

    enteros = int((dt['units'] % 1 != 0).sum()) - dt['units'].isna().sum()
    paises = sorted(list(dt['country'].unique()))

    datos = {
      "row_count": len(dt),
      "column_count": len(dt.columns),
      "missing_required_columns": sorted(set(columnas_req) - set(dt.columns)),
      "unexpected_columns": sorted(set(dt.columns) - set(columnas_req)),
      "duplicate_row_count": int(duplicados),
      "duplicate_supplier_id_row_count": int(duplicados_id_supp),
      "missing_value_count_by_column": dic,
      "invalid_email_count": dominios_malos,
      "invalid_unit_count": int(enteros),
      "country_values": paises
    }

    ruta2 = Path(__file__).resolve().parent.parent / "submission" / "data_quality_report.json"
    with open(ruta2, "w") as f:
        json.dump(datos, f, ensure_ascii=False, indent=4)
    

    

main()
