import click
import sqlalchemy
from sqlalchemy import MetaData
from sqlalchemy.schema import CreateTable, CreateIndex


@click.command()
@click.argument("dsn")
def cli(dsn):
    engine = sqlalchemy.create_engine(dsn)
    metadata_obj = MetaData()
    metadata_obj.reflect(bind=engine)
    output_ddl = []

    tables = sorted(metadata_obj.tables.values(), key=lambda t: t.name)

    for table in tables:
        create_table_ddl = CreateTable(table, include_foreign_key_constraints=table.foreign_key_constraints)
        create_table_ddl.columns = sorted(create_table_ddl.columns, key=lambda c: c.element.name)
        output_ddl.append(str(create_table_ddl.compile(engine)).strip() + '\n')
        output_ddl.extend([
            str(CreateIndex(index).compile(engine))
            for index in sorted(table.indexes, key=lambda t: t.name)
        ])
        output_ddl.append('')

    print("\n".join(output_ddl))


if __name__ == '__main__':
    cli()
