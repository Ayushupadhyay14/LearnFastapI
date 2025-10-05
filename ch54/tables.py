from sqlalchemy import MetaData, Table, Column, Integer, String

metadata = MetaData()

users = Table(
  "users",
  metadata,
  Column("id", Integer, primary_key=True),
  Column("name", String(length=50), nullable=False),
  Column("email", String, nullable=False, unique=True)
  )
