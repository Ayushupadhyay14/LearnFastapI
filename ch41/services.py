from db import engine
from tables import users, posts
from sqlalchemy import text

# Using RAW SQL (Insert)
def raw_sql_insert():
  with engine.connect() as conn:
    stmt = text("""
                INSERT INTO users (name, email)
                VALUES (:name, :email)
                """)
    conn.execute(stmt, {"name": "sonam", "email":"sonam@example.com"})
    conn.commit()

# Using RAW SQL (SELECT)
def raw_sql_example():
    with engine.connect() as conn:
        stmt = text("SELECT * FROM users WHERE email = :email")
        result = conn.execute(stmt, {"email": "sonam@example.com"}).first()
        return result