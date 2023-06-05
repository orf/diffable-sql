from __future__ import annotations

from sqlalchemy import Column, Index, Integer, MetaData, String, Table, UniqueConstraint, create_engine

engine = create_engine("sqlite:///db.sqlite3")
metadata = MetaData()

table = Table(
    "sometable",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("foo", String),
    UniqueConstraint("foo"),
    Index("foobar", "foo"),
    sqlite_autoincrement=True,
)
metadata.create_all(engine)
