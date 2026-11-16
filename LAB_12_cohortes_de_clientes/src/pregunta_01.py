import pandas as pd


def build_cohort_analysis() -> pd.DataFrame:
    """
    Una tienda quiere saber si sus clientes vuelven a comprar después de su
    primera compra. Para responder, agrupe a los clientes en cohortes según
    el mes de su primera compra y mida, mes a mes, qué proporción de cada
    cohorte vuelve a comprar. Use `data/sales.csv.gz`, que tiene una fila por
    orden con su cliente (`CustomerID`) y su fecha (`OrderDate`).

    Use estas definiciones:

    - `cohort_month`: el mes de la primera compra del cliente, escrito como
      `AAAA-MM`.
    - `period_index`: los meses transcurridos desde `cohort_month`; es 0 en el
      mes de la primera compra, 1 en el mes siguiente, y así sucesivamente.
    - `active_customers`: la cantidad de clientes distintos de la cohorte que
      compraron en ese período.
    - `cohort_size`: la cantidad de clientes de la cohorte, es decir, sus
      clientes activos en el período 0.
    - `retention_rate`: `active_customers` sobre `cohort_size`.

    Genere dos archivos en `submission/`:

    1. `cohort_retention.csv`, sin el índice de Pandas, con las columnas
       `cohort_month`, `period_index`, `active_customers`, `cohort_size` y
       `retention_rate`, y una fila por cada combinación cohorte–período
       observada, ordenadas por cohorte y período.

    2. `cohort_retention_heatmap.png`, un mapa de calor de `retention_rate`
       con una fila por cohorte (eje vertical) y una columna por período
       (eje horizontal). Muestre los valores como porcentajes. Los períodos
       que todavía no se pueden observar para una cohorte no significan
       retención cero: déjelos vacíos en el mapa.

    La función también debe retornar la tabla de retención.

    Ejemplo del formato de `cohort_retention.csv`:

        cohort_month,period_index,active_customers,cohort_size,retention_rate
        2022-01,0,100,100,1.0
        2022-01,1,26,100,0.26
        ...
    """

    import pandas as pd
    import numpy as np
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from pathlib import Path
    
    base = Path(__file__).resolve().parent.parent
    ruta = base / 'data' / 'sales.csv.gz'
    dt = pd.read_csv(ruta, sep=',')

    dt['OrderDate'] = pd.to_datetime(dt['OrderDate'])
    dt['order_month'] = dt['OrderDate'].dt.to_period('M')
    dt['cohort_month'] = dt.groupby('CustomerID')['order_month'].transform('min')

    dt['period_index'] = (
        (dt['order_month'].dt.year - dt['cohort_month'].dt.year) * 12
        + (dt['order_month'].dt.month - dt['cohort_month'].dt.month)
    )
    dt['cohort_month'] = dt['cohort_month'].dt.strftime('%Y-%m')

    cohort_re = (
        dt.groupby(['cohort_month', 'period_index'])
          .agg(active_customers=('CustomerID', 'nunique'))
          .reset_index()
    )

    size = (
        cohort_re[cohort_re['period_index'] == 0]
        .set_index('cohort_month')['active_customers']
        .rename('cohort_size')
    )
    cohort_re = cohort_re.merge(size, on='cohort_month', how='left')
    cohort_re['retention_rate'] = (cohort_re['active_customers']
                                   / cohort_re['cohort_size'])
    cohort_re = (
        cohort_re.sort_values(['cohort_month', 'period_index'])
                 .reset_index(drop=True)
    )

    # Mapa de calor
    pivot = cohort_re.pivot(index='cohort_month', columns='period_index',
                            values='retention_rate')
    datos = np.ma.masked_invalid(pivot.values)

    cmap = plt.get_cmap('Blues').copy()
    cmap.set_bad('white')   # períodos no observables quedan vacíos

    fig, ax = plt.subplots(figsize=(max(8, pivot.shape[1] * 0.7),
                                    max(6, pivot.shape[0] * 0.4)))
    im = ax.imshow(datos, cmap=cmap, aspect='auto', vmin=0, vmax=1)

    ax.set_xticks(range(pivot.shape[1]))
    ax.set_xticklabels(pivot.columns)
    ax.set_yticks(range(pivot.shape[0]))
    ax.set_yticklabels(pivot.index)
    ax.set_xlabel('Período (meses desde la primera compra)')
    ax.set_ylabel('Cohorte')
    ax.set_title('Retención por cohorte')

    for i in range(pivot.shape[0]):
        for j in range(pivot.shape[1]):
            valor = pivot.values[i, j]
            if not np.isnan(valor):
                ax.text(j, i, f'{valor:.0%}', ha='center', va='center',
                        fontsize=7,
                        color='white' if valor > 0.6 else 'black')

    fig.colorbar(im, ax=ax, format=lambda x, _: f'{x:.0%}')
    fig.tight_layout()

    out = base / 'submission'
    out.mkdir(exist_ok=True)
    fig.savefig(out / 'cohort_retention_heatmap.png', dpi=150)
    plt.close(fig)

    cohort_re.to_csv(out / 'cohort_retention.csv', index=False)

    return cohort_re

build_cohort_analysis()

