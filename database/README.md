# Database-related things

## Connecting to the DB through Docker (externally)

```bash
docker compose exec -it db psql -U morpheus
```

PostgreSQL prompt will open and you can now run any SQL (or Postgre-specific) commands you want. To quit, press Ctrl+D.

## Enable debug prints

Add `echo=True` to `database/__init__.py`:

```python
8   self.engine = create_async_engine(config.db_string, echo=False)
                                                        ^
```

## Database backup/restore

> [!Note]
> For most of these operations you need the database container running.
> ```bash
> docker compose up -d db
> ```

To backup the database, run the following command:

```bash
docker compose exec db pg_dump -U morpheus -d morpheus > backup.sql
```

Restore the database from the backup file automatically by running the following commands:

> [!Note]
> Backup.sql with data must be in `database/backup/backup.sql`

```bash
docker compose down
docker volume rm morpheus_postgres_data
docker compose up --build -d
```

To manually restore the database, run the following commands:

```bash
# drop and recreate the database must be separate commands
docker compose exec db psql -U morpheus -d postgres -c "DROP DATABASE morpheus;"
docker compose exec db psql -U morpheus -d postgres -c "CREATE DATABASE morpheus WITH OWNER morpheus;"

# restore the database from the backup file
docker compose exec -T db psql -U morpheus < backup.sql
```

You can drop specific table using this command:

```bash
docker compose exec db psql -U morpheus -c "DROP TABLE [table_name] CASCADE;"
```

To get only specific table and it's data use this command:

```bash
docker compose exec db pg_dump -U morpheus -d morpheus -t [table_name] > [table_name].sql
```
