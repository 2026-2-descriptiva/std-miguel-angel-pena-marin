import pandas as pd


def pregunta_01() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Una entidad pública recibe peticiones, quejas, reclamos y sugerencias
    (PQRS) por dos canales, la página web y las cartas, y la ley le da 15 días
    hábiles para responder cada una. Su tarea es medir si la entidad cumple
    ese plazo.

    Los archivos `data/historical_requests_web.csv.gz` y
    `data/historical_requests_letter.csv.gz` tienen una fila por solicitud
    recibida entre 2016 y 2021 por cada canal, con su identificador
    (`record_id`), la fecha de entrada (`in_date`), el día de la semana de
    entrada (`day_name`) y la fecha de respuesta (`out_date`). Si `out_date`
    está vacía, la solicitud todavía no ha sido respondida.

    Tenga en cuenta lo siguiente:

    - Algunas solicitudes aparecen repetidas: elimine las filas idénticas
      dentro de cada canal, para contar cada solicitud una sola vez. Las
      filas sin `record_id` son solicitudes válidas.
    - Llame `letter` al canal de las cartas y `web` al de la página web.
    - Los días hábiles de respuesta son los días de lunes a viernes
      posteriores a la fecha de entrada, hasta la fecha de respuesta
      incluida. Por ejemplo, una solicitud que entra un viernes y se responde
      el lunes siguiente tardó 1 día hábil. No considere los festivos.
    - Los días calendario de respuesta son la diferencia entre la fecha de
      respuesta y la de entrada.
    - Una solicitud cumple el plazo si fue respondida en 15 días hábiles o
      menos. Una solicitud pendiente no ha cumplido el plazo.
    - `on_time_rate` es la proporción de solicitudes que cumplen el plazo,
      sobre el total de solicitudes, incluidas las pendientes.
    - Las medianas de días se calculan solamente con las solicitudes
      respondidas.

    Genere tres archivos en `submission/`, sin el índice de Pandas y con las
    columnas en el orden indicado:

    1. `channel_summary.csv`, con una fila por canal, en orden alfabético:
       `channel`, `requests`, `answered`, `pending`,
       `median_business_days` y `on_time_rate`.

    2. `yearly_summary.csv`, con una fila por año de entrada y canal,
       ordenada por año y luego por canal: `year`, `channel`, `requests`,
       `pending` y `on_time_rate`.

    3. `entry_day_summary.csv`, con una fila por día de entrada, de lunes a
       domingo, con los dos canales juntos: `day_name`, `requests`,
       `median_calendar_days` y `median_business_days`.

    Observe en el tercer archivo cómo cambia la lectura del tiempo de
    respuesta según se cuenten días calendario o días hábiles.

    La función también debe retornar las tres tablas, en el mismo orden.

    Ejemplo del formato de `channel_summary.csv`:

        channel,requests,answered,pending,median_business_days,on_time_rate
        letter,28138,...
        ...
    """

    import pandas as pd
    import numpy as np
    from pathlib import Path

    base = Path(__file__).resolve().parent.parent
    web = pd.read_csv(base / 'data' / 'historical_requests_web.csv.gz', sep=',')
    letter = pd.read_csv(base / 'data' / 'historical_requests_letter.csv.gz', sep=',')

    # Filas idénticas se eliminan dentro de cada canal
    web = web.drop_duplicates()
    letter = letter.drop_duplicates()
    web['channel'] = 'web'
    letter['channel'] = 'letter'
    dt = pd.concat([web, letter], ignore_index=True)

    dt['in_date'] = pd.to_datetime(dt['in_date']).dt.normalize()
    dt['out_date'] = pd.to_datetime(dt['out_date']).dt.normalize()
    dt['year'] = dt['in_date'].dt.year
    dt['dow'] = dt['in_date'].dt.dayofweek

    dt['answered'] = dt['out_date'].notna()

    # Días calendario
    dt['calendar_days'] = (dt['out_date'] - dt['in_date']).dt.days

    # Días hábiles: lunes a viernes después de la entrada, hasta la respuesta incluida
    # busday_count cuenta [inicio, fin), por eso se suma 1 a ambas fechas
    dt['business_days'] = np.nan
    ini = dt.loc[dt['answered'], 'in_date'].values.astype('datetime64[D]')
    fin = dt.loc[dt['answered'], 'out_date'].values.astype('datetime64[D]')
    dt.loc[dt['answered'], 'business_days'] = np.busday_count(ini + 1, fin + 1)

    # Las pendientes dan NaN, y NaN <= 15 es False
    dt['on_time'] = dt['business_days'] <= 15

    # 1. Resumen por canal
    channel_sum = (
        dt.groupby('channel')
          .agg(
              requests=('channel', 'size'),
              answered=('answered', 'sum'),
              median_business_days=('business_days', 'median'),
              on_time_rate=('on_time', 'mean'),
          )
          .reset_index()
    )
    channel_sum['pending'] = channel_sum['requests'] - channel_sum['answered']
    channel_sum = channel_sum[['channel', 'requests', 'answered', 'pending',
                               'median_business_days', 'on_time_rate']]

    # 2. Resumen por año y canal
    yearly_sum = (
        dt.groupby(['year', 'channel'])
          .agg(
              requests=('channel', 'size'),
              answered=('answered', 'sum'),
              on_time_rate=('on_time', 'mean'),
          )
          .reset_index()
    )
    yearly_sum['pending'] = yearly_sum['requests'] - yearly_sum['answered']
    yearly_sum = (
        yearly_sum[['year', 'channel', 'requests', 'pending', 'on_time_rate']]
        .sort_values(['year', 'channel'])
        .reset_index(drop=True)
    )

    # 3. Resumen por día de entrada (lunes a domingo, ambos canales)
    day_sum = (
        dt.groupby(['dow', 'day_name'])
          .agg(
              requests=('channel', 'size'),
              median_calendar_days=('calendar_days', 'median'),
              median_business_days=('business_days', 'median'),
          )
          .reset_index()
          .sort_values('dow')
          .drop(columns='dow')
          .reset_index(drop=True)
    )

    out = base / 'submission'
    out.mkdir(exist_ok=True)
    channel_sum.to_csv(out / 'channel_summary.csv', index=False)
    yearly_sum.to_csv(out / 'yearly_summary.csv', index=False)
    day_sum.to_csv(out / 'entry_day_summary.csv', index=False)

    return channel_sum, yearly_sum, day_sum
