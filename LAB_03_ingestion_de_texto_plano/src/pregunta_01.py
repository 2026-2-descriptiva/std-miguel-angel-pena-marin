def pregunta_01():
    """
    El archivo `data/clusters_report.txt` es un reporte de clústeres de
    palabras clave pensado para ser leído por una persona, no por un programa:
    los encabezados ocupan varias líneas, las columnas están alineadas con
    espacios y la lista de palabras clave de un clúster continúa en las líneas
    siguientes.

    Su tarea es convertir ese reporte en un DataFrame de Pandas con una fila
    por clúster y las columnas:

    - `cluster`: número del clúster, como entero.
    - `cantidad_de_palabras_clave`: como entero.
    - `porcentaje_de_palabras_clave`: como número decimal; por ejemplo, el
      texto `15,9 %` debe quedar como `15.9`.
    - `principales_palabras_clave`: todas las palabras clave del clúster en un
      solo texto, separadas por una coma y un único espacio.

    Retorne el DataFrame.

    Ejemplo del formato de la respuesta (se omite la última columna):

           cluster  cantidad_de_palabras_clave  porcentaje_de_palabras_clave
        0        1                         105                          15.9
        1        2                         102                          15.4
        ...
    """
    import pandas as pd
    from pathlib import Path
    import re
    ruta = Path(__file__).resolve().parent.parent / "data" / "clusters_report.txt"
    registros = []
    patron = re.compile(r"^\s*(\d+)\s+(\d+)\s+([\d,]+)\s*%\s*(.*)$")
    with open(ruta, encoding="utf-8") as f:
      for linea in f:
          linea = linea.rstrip("\n")
          m = patron.match(linea)
          if m:
              registros.append([m.group(1), m.group(2), m.group(3), m.group(4).strip()])
          elif registros and linea.strip():
              registros[-1][3] += " " + linea.strip()
              
              
    dt = pd.DataFrame(registros, columns= ['cluster', 'cantidad_de_palabras_clave', 'porcentaje_de_palabras_clave', 'principales_palabras_clave'])
    dt['cluster'] = dt['cluster'].astype('int')
    dt['cantidad_de_palabras_clave'] = dt['cantidad_de_palabras_clave'].astype('int')

    dt['porcentaje_de_palabras_clave'] = dt['porcentaje_de_palabras_clave'].str.replace(',', '.').astype('float')
    dt['principales_palabras_clave'] = dt['principales_palabras_clave'].str.replace(".","")
    dt['principales_palabras_clave'] = dt['principales_palabras_clave'].str.replace(r"\s+"," ", regex=True)
    dt['principales_palabras_clave'] = dt['principales_palabras_clave'].str.strip()
    
    return dt
    



pregunta_01()
