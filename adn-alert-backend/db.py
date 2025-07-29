import psycopg2
import json
import time
from psycopg2.extras import RealDictCursor

class Database:
    def __init__(self, dbname, user, password, host='localhost', port=5432):
        for intento in range(1, 11):
            try:
                print(f"⏳ Intentando conexión a PostgreSQL... intento {intento}")
                self.conn = psycopg2.connect(
                    dbname=dbname,
                    user=user,
                    password=password,
                    host=host,
                    port=port
                )
                self.cur = self.conn.cursor(cursor_factory=RealDictCursor)
                self._ensure_table()
                print("✅ Conexión a PostgreSQL establecida.")
                return
            except Exception as e:
                print(f"⚠️  Conexión fallida ({intento}/10): {e}")
                time.sleep(1)
        raise Exception("❌ No se pudo conectar a PostgreSQL después de varios intentos.")

    def _ensure_table(self):
        try:
            self.cur.execute('''
                CREATE TABLE IF NOT EXISTS alerts (
                    id SERIAL PRIMARY KEY,
                    topic VARCHAR(255) NOT NULL,
                    payload TEXT NOT NULL,
                    timestamp TIMESTAMP NOT NULL
                );
            ''')
            self.conn.commit()
        except Exception as e:
            print(f"⚠️ Error creando tabla (posible conflicto entre instancias): {e}")


    def insert_alert(self, topic, payload, timestamp):
        self.cur.execute(
            "INSERT INTO alerts (topic, payload, timestamp) VALUES (%s, %s, %s)",
            (topic, payload, timestamp)
        )
        self.conn.commit()

    def get_alerts(self):
        self.cur.execute("SELECT * FROM alerts ORDER BY timestamp DESC")
        rows = self.cur.fetchall()
        for row in rows:
            try:
                row["payload"] = json.loads(row["payload"])
            except json.JSONDecodeError:
                pass
        return rows

    def get_alerts_filtered(self, region=None, tipo=None, mensaje=None, limit=None, offset=None, order="desc"):
        query = "SELECT * FROM alerts"
        conditions = []
        params = []

        if region:
            conditions.append("payload::jsonb ->> 'region' = %s")
            params.append(region)
        if tipo:
            conditions.append("payload::jsonb ->> 'tipo' = %s")
            params.append(tipo)
        if mensaje:
            conditions.append("payload::jsonb ->> 'mensaje' ILIKE %s")
            params.append(f"%{mensaje}%")

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        # Validar orden (por seguridad contra inyecciones)
        if order.lower() not in ["asc", "desc"]:
            order = "desc"

        query += f" ORDER BY timestamp {order.upper()}"

        if limit:
            query += " LIMIT %s"
            params.append(limit)
        if offset:
            query += " OFFSET %s"
            params.append(offset)

        self.cur.execute(query, params)
        rows = self.cur.fetchall()
        for row in rows:
            try:
                row["payload"] = json.loads(row["payload"])
            except json.JSONDecodeError:
                pass
        return rows

    def close(self):
        self.cur.close()
        self.conn.close()
