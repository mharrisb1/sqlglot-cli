from typing import Annotated, Any, Callable

import sqlglot
import sqlglot.optimizer
import typer

from .callbacks import echo_statements, read_file_to_buffer

cli = typer.Typer(
    name="sqlglot-cli",
    help="CLI wrapper around sqlglot",
    no_args_is_help=True,
    context_settings={"help_option_names": ["-h", "--help"]},
    result_callback=echo_statements,
)


@cli.command(help="Transpile SQL (https://sqlglot.com/sqlglot.html#transpile)")
def transpile(
    file: Annotated[
        str | None,
        typer.Argument(
            help="Path to a sql file. Leave blank or use '-' for stdin",
            callback=read_file_to_buffer,
        ),
    ] = None,
    read: Annotated[
        sqlglot.Dialects | None, typer.Option("--read", "-r", help="Source dialect")
    ] = None,
    write: Annotated[
        sqlglot.Dialects | None, typer.Option("--write", "-w", help="Target dialect")
    ] = None,
    identity: Annotated[
        bool,
        typer.Option(
            "--identity",
            help="If the target dialect is not specified the source dialect will be used as both",
        ),
    ] = False,
    normalize: Annotated[
        bool, typer.Option("--normalize", help="Normalize query")
    ] = False,
    pad: Annotated[int, typer.Option(help="Query padding")] = 2,
    indent: Annotated[int, typer.Option(help="Query indent")] = 2,
    normalize_functions: Annotated[
        bool, typer.Option("--normalize-functions", help="Normalize query functions")
    ] = False,
    leading_comma: Annotated[
        bool, typer.Option("--leading-commas", help="Use leading commas")
    ] = False,
    max_text_width: Annotated[int, typer.Option(help="Query indent")] = 80,
    comments: Annotated[
        bool, typer.Option("--comments", help="Include comments")
    ] = False,
    pretty: Annotated[bool, typer.Option("--pretty", help="Pretty print")] = False,
):
    return sqlglot.transpile(  # type: ignore
        sql=file or "",
        read=read,
        write=write,
        identity=identity,
        pretty=pretty,
        normalize=normalize,
        pad=pad,
        indent=indent,
        normalize_functions=normalize_functions,
        leading_comma=leading_comma,
        max_text_width=max_text_width,
        comments=comments,
    )


@cli.command(help="Optimize SQL (https://sqlglot.com/sqlglot/optimizer/optimizer.html)")
def optimize(
    file: Annotated[
        str | None,
        typer.Argument(
            help="Path to a sql file. Leave blank or use '-' for stdin",
            callback=read_file_to_buffer,
        ),
    ] = None,
    dialect: Annotated[
        sqlglot.Dialects | None, typer.Option("--dialect", "-d", help="SQL dialect")
    ] = None,
    all: Annotated[bool, typer.Option("--all", help="Enable all rules")] = False,
    qualify: Annotated[
        bool, typer.Option("--qualify", help="Qualify tables and columns")
    ] = False,
    pushdown_projections: Annotated[
        bool,
        typer.Option("--pushdown-predicates", help="Remove unused columns projections"),
    ] = False,
    normalize: Annotated[
        bool, typer.Option("--normalize", help="Normal form or disjunctive normal form")
    ] = False,
    unnest_subqueries: Annotated[
        bool,
        typer.Option(
            "--unnest-subqueries",
            help="Convert some predicates with subqueries into joins",
        ),
    ] = False,
    pushdown_predicates: Annotated[
        bool,
        typer.Option(
            "--pushdown-predicated", help="Pushdown predicates in FROMS and JOINS"
        ),
    ] = False,
    optimize_joins: Annotated[
        bool,
        typer.Option(
            "--optimize-joins",
            help="Removes cross joins if possible and reorder joins based on predicate dependencies",
        ),
    ] = False,
    eliminate_subqueries: Annotated[
        bool,
        typer.Option(
            "--eliminate-subqueries",
            help="Rewrite derived tables as CTES, deduplicating if possible",
        ),
    ] = False,
    merge_subqueries: Annotated[
        bool,
        typer.Option(
            "--merge-subqueries", help="Merge derived tables into the outer query"
        ),
    ] = False,
    eliminate_joins: Annotated[
        bool,
        typer.Option(
            "--eliminate-joins", help="Remove unused joins from an expression"
        ),
    ] = False,
    eliminate_ctes: Annotated[
        bool,
        typer.Option("--eliminate-ctes", help="Remove unused CTEs from an expression"),
    ] = False,
    quote_identifiers: Annotated[
        bool,
        typer.Option(
            "--quote-identifiers",
            help="Makes sure all identifiers that need to be quoted are quoted",
        ),
    ] = False,
    annotate_types: Annotated[
        bool,
        typer.Option(
            "--annotate-types",
            help="Infers the types of an expression, annotating its AST accordingly",
        ),
    ] = False,
    canonicalize: Annotated[
        bool, typer.Option("--canonicalize", help="Converts to standard form")
    ] = False,
    simplify: Annotated[
        bool, typer.Option("--simplify", help="Simplify expressions")
    ] = False,
    pretty: Annotated[bool, typer.Option("--pretty", help="Pretty print")] = False,
):
    exprs = sqlglot.parse(sql=file or "", dialect=dialect)  # type: ignore
    rule_flags = dict(
        qualify=all or qualify,
        pushdown_projections=all or pushdown_projections,
        normalize=all or normalize,
        unnest_subqueries=all or unnest_subqueries,
        pushdown_predicates=all or pushdown_predicates,
        optimize_joins=all or optimize_joins,
        eliminate_subqueries=all or eliminate_subqueries,
        merge_subqueries=all or merge_subqueries,
        eliminate_joins=all or eliminate_joins,
        eliminate_ctes=all or eliminate_ctes,
        quote_identifiers=all or quote_identifiers,
        annotate_types=all or annotate_types,
        canonicalize=all or canonicalize,
        simplify=all or simplify,
    )
    rule_map = {rule.__name__: rule for rule in sqlglot.optimizer.RULES}  # type: ignore
    rules: list[Callable[..., Any]] = [rule_map[k] for k, v in rule_flags.items() if v]
    optimized = [
        sqlglot.optimizer.optimize(expr, dialect=dialect, rules=rules)  # type: ignore
        for expr in exprs
        if expr
    ]
    return [o.sql(dialect=dialect, pretty=pretty) for o in optimized]  # type: ignore
