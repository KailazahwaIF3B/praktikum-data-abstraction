import sqlite3
import pandas as pd

# 1. BIKIN DATABASE SQLITE (network_nodes.db)
def create_sqlite_db():
    conn = sqlite3.connect("data/network_nodes.db")
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS network_nodes (
        node_id TEXT PRIMARY KEY,
        cluster_group TEXT,
        ip_address TEXT,
        latitude REAL,
        longitude REAL
    )
    """)
    
    nodes_data = [
        ("NODE-01", "Datacenter", "192.168.1.1", -0.9471, 100.3543),
        ("NODE-02", "Core-Gateway", "192.168.1.2", -0.9512, 100.3601),
        ("NODE-03", "Edge-A", "192.168.1.3", -0.9210, 100.3412),
        ("NODE-04", "Edge-B", "192.168.1.4", -0.9823, 100.3890),
    ]
    
    cursor.executemany("INSERT OR REPLACE INTO network_nodes VALUES (?,?,?,?,?)", nodes_data)
    conn.commit()
    conn.close()
    print("[SUCCESS] File SQLite 'data/network_nodes.db' berhasil dibuat!")

# 2. BIKIN DATABASE ACCESS / CSV MOCK (system_logs)
def create_access_mock_csv():
    # Karena MS Access butuh driver spesifik, kita bisa buatkan CSV 
    # atau buat file Access jika MS Access Engine terpasang.
    logs_data = {
        "log_id": [1, 2, 3, 4],
        "timestamp": ["2026-10-10 08:00:00", "2026-10-10 08:15:00", "2026-10-10 08:30:00", "2026-10-10 08:45:00"],
        "node_id": ["NODE-01", "NODE-02", "NODE-01", "NODE-03"],
        "severity_level": ["Low", "Medium", "High", "Critical"],
        "metric_value": [12.5, 45.0, 89.2, 120.4]
    }
    df = pd.DataFrame(logs_data)
    df.to_csv("data/system_logs.csv", index=False)
    print("[SUCCESS] File sampel 'data/system_logs.csv' berhasil dibuat!")

if __name__ == "__main__":
    create_sqlite_db()
    create_access_mock_csv()