import sqlite3
import pandas as pd
import pyodbc
from sqlalchemy import create_engine

# ====================================================
# 1. INGESTION DATA DARI 3 ENGINE DBMS
# ====================================================

# Ingestion MS Access (.accdb)
def ingest_access_data(db_path: str) -> pd.DataFrame:
    conn_str = (
        r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};"
        rf"DBQ={db_path};"
    )
    with pyodbc.connect(conn_str) as conn:
        query = "SELECT log_id, timestamp, node_id, severity_level, metric_value FROM system_logs"
        return pd.read_sql(query, conn)

# Ingestion SQLite
def ingest_sqlite_data(db_path: str) -> pd.DataFrame:
    with sqlite3.connect(db_path) as conn:
        query = "SELECT node_id, cluster_group, ip_address, latitude, longitude FROM network_nodes"
        return pd.read_sql_query(query, conn)

# Ingestion PostgreSQL
def ingest_postgres_data(user: str, pwd: str, host: str, port: int, db: str) -> pd.DataFrame:
    uri = f"postgresql+psycopg2://{user}:{pwd}@{host}:{port}/{db}"
    engine = create_engine(uri)
    query = "SELECT source_node, target_node, latency_ms, packet_loss FROM topology_edges"
    with engine.connect() as conn:
        return pd.read_sql(query, conn)


# ====================================================
# 2. PIPELINE VALIDASI ABSTRAKSI DATA
# ====================================================

def validate_abstraction_pipeline(df_logs: pd.DataFrame, df_nodes: pd.DataFrame, df_edges: pd.DataFrame):
    # 2.1 Abstraksi Temporal & Ordinal (Access)
    df_logs["timestamp"] = pd.to_datetime(df_logs["timestamp"])
    df_logs["severity_level"] = pd.Categorical(
        df_logs["severity_level"],
        categories=["Low", "Medium", "High", "Critical"],
        ordered=True
    )
    df_logs["metric_value"] = pd.to_numeric(df_logs["metric_value"], downcast="float")

    # 2.2 Abstraksi Spatial & Tabular (SQLite)
    df_nodes["cluster_group"] = df_nodes["cluster_group"].astype("category")
    df_nodes["latitude"] = pd.to_numeric(df_nodes["latitude"])
    df_nodes["longitude"] = pd.to_numeric(df_nodes["longitude"])

    # 2.3 Abstraksi Network (PostgreSQL)
    edge_list = df_edges[["source_node", "target_node", "latency_ms"]].copy()

    # Cetak laporan verifikasi skema
    print("=== DOKUMENTASI VALIDASI DATA ABSTRACTION ===")
    print("\n[TEMPORAL & ORDINAL - Access System Logs]")
    print(df_logs.dtypes)
    
    print("\n[SPATIAL & CATEGORICAL - SQLite Network Nodes]")
    print(df_nodes.dtypes)
    
    print("\n[NETWORK TOPOLOGY - PostgreSQL Edges]")
    print(edge_list.head())


if __name__ == "__main__":
    print("Modul pipeline siap dijalankan sesuai konfigurasi DBMS aktif.")