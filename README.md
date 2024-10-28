# sqlglot-cli

CLI wrapper around [sqlglot](https://github.com/tobymao/sqlglot).

## Installation

```sh
pipx install sqlglot-cli

# or with sqlglotrs
pipx install 'sqlglot-cli[rs]'

# or with rich terminal
pipx install 'sqlglot-cli[rich]'

# or with both
pipx install 'sqlglot-cli[rs,rich]'
```

## Usage

> [!IMPORTANT]
> All output is written to stdout

```sh
# read from file
sqlglot-cli transpile foo.sql --read postgres --write clickhouse --pretty

# or use stdin
cat foo.sql | sqlglot-cli transpile - --read postgres --write clickhouse --pretty

# pipe to your heart's desire to incorporate into workflows
cat examples/postgres__ctes.in.sql |
sqlglot-cli optimize - -d postgres --all |
sqlglot-cli transpile - -r postgres -w snowflake |
sqlglot-cli optimize - -d snowflake --all |
sqlfluff fix - --dialect snowflake
```
