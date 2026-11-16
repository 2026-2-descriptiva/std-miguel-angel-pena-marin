import pandas as pd


def clean_campaign_data() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Los datos de una campaña de mercadeo bancario llegaron repartidos en diez
    archivos comprimidos, `data/bank-marketing-campaing-*.csv.gz`, con
    información mezclada del cliente, de la campaña y del contexto económico.
    Su tarea es leerlos directamente desde los archivos comprimidos, sin
    descomprimirlos a mano, y separarlos en tres tablas limpias.

    Guarde cada tabla como un CSV sin comprimir en `submission/`, sin el índice
    de Pandas y con las columnas en el orden indicado:

    1. `client.csv`: `client_id`, `age`, `job`, `marital`, `education`,
       `credit_default` y `mortgage`.
       - En `job`, elimine los puntos y cambie los guiones por guiones bajos.
       - En `education`, cambie los puntos por guiones bajos y deje el valor
         `unknown` como faltante.
       - En `credit_default` y `mortgage`, escriba 1 si el valor es `yes` y 0
         en cualquier otro caso.

    2. `campaign.csv`: `client_id`, `number_contacts`, `contact_duration`,
       `previous_campaign_contacts`, `previous_outcome`, `campaign_outcome` y
       `last_contact_date`.
       - En `previous_outcome`, escriba 1 si el valor es `success` y 0 en
         cualquier otro caso.
       - En `campaign_outcome`, escriba 1 si el valor es `yes` y 0 en
         cualquier otro caso.
       - Construya `last_contact_date` a partir de las columnas `month` y
         `day`, usando el año 2022 y el formato `AAAA-MM-DD`.

    3. `economics.csv`: `client_id`, `cons_price_idx` y
       `euribor_three_months`.

    La función también debe retornar las tres tablas, en el orden `client`,
    `campaign` y `economics`.

    Ejemplo del formato de `campaign.csv`:

        client_id,number_contacts,contact_duration,...,last_contact_date
        0,1,261,...,2022-05-13
        ...
    """

    import pandas as pd
    import os 
    from pathlib import Path
    from functools import reduce

    base = Path(__file__).resolve().parent.parent
    carpeta = base / "data"
    archivos = sorted(carpeta.glob("*.csv.gz"))
    dfs = [pd.read_csv(f, sep=",") for f in archivos]

    
    dt = pd.concat((pd.read_csv(f) for f in archivos), ignore_index=True)

    dt_client = dt[['client_id', 'age', 'job', 'marital', 'education', 'credit_default', 'mortgage']].copy()
    
    dt_client['job'] = dt_client['job'].str.replace('.', '')
    dt_client['job'] = dt_client['job'].str.replace('-', '_')
    dt_client['education'] = dt_client['education'].str.replace('.', '_')
    dt_client['education'] = dt_client['education'].replace('unknown', pd.NA)
    dt_client['credit_default'] = dt_client['credit_default'].map({'yes': 1}).fillna(0).astype(int)
    dt_client['mortgage'] = dt_client['mortgage'].map({'yes': 1}).fillna(0).astype(int)
    
    dt_campaing = dt[['client_id', 'number_contacts', 'contact_duration', 'previous_campaign_contacts', 'previous_outcome', 'campaign_outcome']].copy()
    dt_campaing['previous_outcome'] = dt_campaing['previous_outcome'].map({'success': 1}).fillna(0).astype(int)
    dt_campaing['campaign_outcome'] = dt_campaing['campaign_outcome'].map({'yes': 1}).fillna(0).astype(int)

    dt_campaing["last_contact_date"] = pd.to_datetime(
    "2022-" + dt["month"].str.strip().str.lower() + "-" + dt["day"].astype(str),
    format="%Y-%b-%d",
    errors="coerce",
    ).dt.strftime("%Y-%m-%d")

    dt_economics = dt[['client_id', 'cons_price_idx', 'euribor_three_months']]

    ruta = Path(__file__).resolve().parent.parent
    dt_client.to_csv(os.path.join(ruta, "submission", "client.csv"), index= False, sep=',')
    dt_campaing.to_csv(os.path.join(ruta, "submission", "campaign.csv"), index= False, sep=',')
    dt_economics.to_csv(os.path.join(ruta, "submission", "economics.csv"), index= False, sep=',')



    return dt_client, dt_campaing, dt_economics
    
clean_campaign_data()