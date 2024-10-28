import sys

import typer


def echo_statements(stmts: list[str | None]):
    if len(stmts) < 1:
        typer.echo("")

    if len(stmts) == 1:
        typer.echo(stmts[0])

    else:
        typer.echo("\n\n".join([stmt + ";" for stmt in stmts if stmt]))


def read_file_to_buffer(file: str | None = None) -> str:
    if not file or file == "-":
        return sys.stdin.read()
    else:
        try:
            with open(file, "rb") as fp:
                return fp.read().decode()
        except FileNotFoundError:
            typer.echo(f"File {file} not found")
            raise typer.Exit(1)
