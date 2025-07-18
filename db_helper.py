import sqlite3
import pandas as pd

DB_PATH = 'app.db'

def get_conn():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def save_sheet_to_db(sheet_name, df):
    conn = get_conn()
    # Remove all unnamed columns
    df = df.loc[:, [col for col in df.columns if not str(col).lower().startswith("unnamed")]]
    # Skip saving if DataFrame is empty or has no columns
    if df.empty or len(df.columns) == 0:
        conn.close()
        return
    # Overwrite table safely
    df.to_sql(sheet_name, conn, if_exists='replace', index=False)
    conn.close()

def load_sheet_from_db(sheet_name):
    conn = get_conn()
    try:
        df = pd.read_sql(f'SELECT * FROM "{sheet_name}"', conn)
        df = df.astype(str)
    except Exception:
        df = pd.DataFrame()
    conn.close()
    return df
