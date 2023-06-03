import click
import sqlalchemy
from sqlalchemy import MetaData
from sqlalchemy.schema import CreateTable, CreateIndex


@click.command()
@click.argument("dsn_list", metavar="[dsn]...", nargs=-1)
def cli(dsn_list):
    output_ddl = []
    tables = []
    for dsn in dsn_list:
        engine = sqlalchemy.create_engine(dsn)
        metadata_obj = MetaData()
        metadata_obj.reflect(bind=engine)
        tables.extend((engine, table) for table in metadata_obj.tables.values())

    sorted_tables = sorted(tables, key=lambda t: t[1].name)

    for (engine, table) in sorted_tables:
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
