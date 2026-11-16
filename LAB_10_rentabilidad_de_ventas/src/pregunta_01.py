import pandas as pd


def pregunta_01() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Una cadena de suministros de oficina vende mucho, pero la gerencia
    sospecha que parte de esas ventas no deja utilidad. El archivo
    `data/superstore_orders.csv.gz` tiene una fila por línea de pedido, con
    el número de pedido (`Order ID`), las ventas (`Sales`), la utilidad
    (`Profit`), el descuento aplicado (`Discount`, como proporción), el
    segmento del cliente (`Customer Segment`) y la categoría del producto
    (`Product Category`). Una utilidad negativa significa que la línea se
    vendió con pérdida.

    Use estas definiciones:

    - Margen (`profit_margin`): utilidad sobre ventas.
    - Línea con pérdida: una línea cuya utilidad es negativa.
    - `loss_line_rate`: la proporción de líneas con pérdida.
    - `lost_profit`: la suma de las pérdidas de las líneas con pérdida,
      escrita como número positivo.
    - Rango de descuento (`discount_band`): `0%` si no hubo descuento,
      `1%-5%` si fue mayor que 0 y hasta 5 %, `6%-10%` si fue mayor que 5 % y
      hasta 10 %, y `más de 10%` en otro caso.

    Genere tres archivos en `submission/`, sin el índice de Pandas y con las
    columnas en el orden indicado:

    1. `profitability_summary.csv`, con una sola fila: `lines` (cantidad de
       líneas), `orders` (pedidos distintos), `sales`, `profit`,
       `profit_margin`, `loss_lines` (cantidad de líneas con pérdida),
       `loss_line_rate` y `lost_profit`.

    2. `discount_summary.csv`, con una fila por rango de descuento, en el
       orden en que se definieron arriba: `discount_band`, `lines`, `sales`,
       `profit`, `profit_margin`, `loss_line_rate` y `lost_profit`.

    3. `priority_segments.csv`, con los cinco segmentos segmento–categoría
       que más utilidad pierden: `Customer Segment`, `Product Category`,
       `lines`, `sales`, `profit`, `profit_margin` y `lost_profit`. Considere
       solamente segmentos con al menos 100 líneas y ordénelos por
       `lost_profit` de mayor a menor.

    La función también debe retornar las tres tablas, en el mismo orden.

    Ejemplo del formato de `discount_summary.csv`:

        discount_band,lines,sales,profit,profit_margin,loss_line_rate,...
        0%,166,170539.05,29472.3789,0.1728,0.488,...
        ...
    """

    import pandas as pd
    import numpy as np
    import json
    from pathlib import Path
 
    base = Path(__file__).resolve().parent.parent
    ruta = base / 'data' / 'superstore_orders.csv.gz'
    dt = pd.read_csv(ruta, sep=';')

    dt['Sales'] = dt['Sales'].str.replace(",", ".").astype(float)
    dt['Profit'] = dt['Profit'].str.replace(",", ".").astype(float)
    dt['loss'] = (-dt['Profit']).clip(lower=0)
    dt['is_loss'] = dt['Profit'] < 0
    prof_sum = pd.DataFrame(
        {'lines': len(dt),
         'orders': len(dt['Order ID'].unique()),
         'sales': dt['Sales'].sum(),
         'profit': dt['Profit'].sum(),
         'profit_margin': dt['Profit'].sum() / dt['Sales'].sum(),
         'loss_lines': (dt['Profit'] < 0 ).sum(),
         'loss_line_rate': (dt['Profit'] < 0 ).sum() / len(dt),
         'lost_profit': abs(dt['Profit'][dt['Profit'] < 0].sum())}, 
         index=[0]
    )   

    dt['Discount'] = dt['Discount'].str.replace(',', '.').astype(float)
    
    bins = [-1, 0, 0.05, 0.1, np.inf]
    etiquetas = ['0%', '1%-5%', '6%-10%', 'más de 10%']
    dt['discount_band'] = pd.cut(dt['Discount'], bins=bins, labels=etiquetas)

    disc_sum = (
    dt.groupby('discount_band', observed=False)
      .agg(
          lines=('Order ID', 'count'),
          sales=('Sales', 'sum'),
          profit=('Profit', 'sum'),
          loss_lines=('is_loss', 'sum'),
          lost_profit=('loss', 'sum'),
      )
      .reset_index()
    )
    disc_sum['profit_margin'] = disc_sum['profit'] / disc_sum['sales']
    disc_sum['loss_line_rate'] = disc_sum['loss_lines'] / disc_sum['lines']
    disc_sum = disc_sum[['discount_band', 'lines', 'sales', 'profit',
                         'profit_margin', 'loss_line_rate', 'lost_profit']]

    priority = (
        dt.groupby(['Customer Segment', 'Product Category'])
          .agg(
              lines=('Order ID', 'count'),
              sales=('Sales', 'sum'),
              profit=('Profit', 'sum'),
              lost_profit=('loss', 'sum'),
          )
          .reset_index()
    )
    priority['profit_margin'] = priority['profit'] / priority['sales']
    priority = (
        priority[priority['lines'] >= 100]
          .sort_values('lost_profit', ascending=False)
          .head(5)
    )
    priority = priority[['Customer Segment', 'Product Category', 'lines',
                         'sales', 'profit', 'profit_margin', 'lost_profit']]

    out = base / 'submission'
    prof_sum.to_csv(out / 'profitability_summary.csv', index=False)
    disc_sum.to_csv(out / 'discount_summary.csv', index=False)
    priority.to_csv(out / 'priority_segments.csv', index=False)

    return prof_sum, disc_sum, priority

pregunta_01()
