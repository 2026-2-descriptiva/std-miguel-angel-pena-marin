import pandas as pd


def pregunta_01() -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Una autoridad aeronáutica publica cada año un ranking de aerolíneas según
    su tasa de demora, y algunas aerolíneas se quejan de que es injusto: las
    demoras se acumulan a lo largo del día, de modo que una aerolínea con
    muchos vuelos en la tarde y la noche parece peor aunque opere igual de
    bien que las demás. Su tarea es construir un ranking que tenga en cuenta
    la mezcla de horarios de cada aerolínea.

    El archivo `data/flights_by_carrier_day_hour.csv.gz` tiene los vuelos
    nacionales entre 2006 y 2008, agregados por año, mes, día de la semana,
    hora programada de salida (`scheduled_departure_hour`) y aerolínea
    (`reporting_airline`). Use las columnas `operated_flights` (vuelos
    operados) y `delayed_departure_15_flights` (vuelos que salieron con 15
    minutos o más de demora).

    Siga estos pasos:

    1. Calcule la tasa nacional de demora de cada hora programada de salida:
       vuelos demorados sobre vuelos operados, con todas las aerolíneas
       juntas.
    2. Para cada aerolínea, calcule las demoras esperadas: en cada hora,
       multiplique sus vuelos operados por la tasa nacional de esa hora, y
       sume sobre todas las horas. Son las demoras que tendría si en cada hora
       se comportara como el promedio nacional.
    3. Divida las demoras observadas entre las esperadas. Un valor mayor que 1
       significa que la aerolínea se demora más de lo que explican sus
       horarios.

    Genere dos archivos en `submission/`, sin el índice de Pandas y con las
    columnas en el orden indicado:

    1. `hourly_delay_rates.csv`, con una fila por hora, de 0 a 23:
       `scheduled_departure_hour`, `operated_flights`,
       `delayed_departure_15_flights` y `delay_rate`.

    2. `carrier_adjusted_delays.csv`, con una fila por aerolínea:
       `reporting_airline`, `operated_flights`,
       `delayed_departure_15_flights`, `delay_rate` (la tasa sin ajustar),
       `expected_delayed_flights`, `observed_to_expected_ratio`, `crude_rank`
       y `adjusted_rank`. Incluya solamente aerolíneas con al menos 100 000
       vuelos operados. `crude_rank` es la posición según `delay_rate` y
       `adjusted_rank` la posición según `observed_to_expected_ratio`; en
       ambos, 1 es la peor aerolínea. Ordene la tabla por `adjusted_rank`.

    Compare los dos rankings: las aerolíneas que cambian de posición son las
    que el ranking sin ajustar juzga mal por sus horarios.

    La función también debe retornar las dos tablas, en el mismo orden.

    Ejemplo del formato de `carrier_adjusted_delays.csv`:

        reporting_airline,operated_flights,...,crude_rank,adjusted_rank
        EV,819223,...,1,1
        ...
    """

    import pandas as pd
    import numpy as np
    import json
    from pathlib import Path
 
    base = Path(__file__).resolve().parent.parent
    ruta = base / 'data' / 'flights_by_carrier_day_hour.csv.gz'
    dt = pd.read_csv(ruta, sep=',')

    hour_cs = (
    dt.groupby('scheduled_departure_hour')
      .agg(
          operated_flights=('operated_flights', 'sum'),
          delayed_departure_15_flights=('delayed_departure_15_flights', 'sum'),
      )
      .reindex(range(24), fill_value=0)
      .rename_axis('scheduled_departure_hour')
      .reset_index()
)
    hour_cs['delay_rate'] = (hour_cs['delayed_departure_15_flights']
                             / hour_cs['operated_flights'])
    
    # 2. Demoras esperadas por aerolínea
    car_hour = (
        dt.groupby(['reporting_airline', 'scheduled_departure_hour'],
                   as_index=False)['operated_flights'].sum()
          .merge(hour_cs[['scheduled_departure_hour', 'delay_rate']],
                 on='scheduled_departure_hour', how='left')
    )
    car_hour['expected'] = car_hour['operated_flights'] * car_hour['delay_rate']
    expected = (car_hour.groupby('reporting_airline')['expected'].sum()
                        .rename('expected_delayed_flights'))

    carrier = (
        dt.groupby('reporting_airline')
          .agg(
              operated_flights=('operated_flights', 'sum'),
              delayed_departure_15_flights=('delayed_departure_15_flights', 'sum'),
          )
          .join(expected)
          .reset_index()
    )

    carrier = carrier[carrier['operated_flights'] >= 100_000].copy()

    carrier['delay_rate'] = (carrier['delayed_departure_15_flights']
                             / carrier['operated_flights'])
    carrier['observed_to_expected_ratio'] = (
        carrier['delayed_departure_15_flights']
        / carrier['expected_delayed_flights']
    )

    carrier['crude_rank'] = carrier['delay_rate'].rank(
        ascending=False, method='min').astype(int)
    carrier['adjusted_rank'] = carrier['observed_to_expected_ratio'].rank(
        ascending=False, method='min').astype(int)

    carrier = carrier[[
        'reporting_airline', 'operated_flights',
        'delayed_departure_15_flights', 'delay_rate',
        'expected_delayed_flights', 'observed_to_expected_ratio',
        'crude_rank', 'adjusted_rank',
    ]].sort_values('adjusted_rank').reset_index(drop=True)

    out = base / 'submission'
    out.mkdir(exist_ok=True)
    hour_cs.to_csv(out / 'hourly_delay_rates.csv', index=False)
    carrier.to_csv(out / 'carrier_adjusted_delays.csv', index=False)

    return hour_cs, carrier


pregunta_01()
