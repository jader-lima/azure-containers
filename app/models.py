from sqlalchemy import Column, Integer, String, Table, MetaData

metadata = MetaData()

departamento = Table(
    "departamento", metadata,
    Column("id", Integer, primary_key=True),
    Column("nome", String(100))
)

cargos = Table(
    "cargos", metadata,
    Column("id", Integer, primary_key=True),
    Column("departamento_id", Integer),
    Column("nome", String(100))
)

empregados = Table(
    "empregados", metadata,
    Column("id", Integer, primary_key=True),
    Column("cargo_id", Integer),
    Column("nome", String(100))
)
