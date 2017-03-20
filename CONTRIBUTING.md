(TODO: General guidelines for contributing. Getting started, e.g some pointers as to what is where.)

# Updating the database schema (destructive)
These instructions will delete the current schema with all its tables and redefine the schema with the definitions in `database.sql` (from `master`).

1. Make desired changes in `database.sql` and get it merged into `master`.
2. `heroku pg:psql`
  * `drop schema public cascade`
  * `create schema public`
  * `\i database.sql`
  * `\i database.sql`

We currently have to do `\i database.sql` twice because of circular references. You will first see errors about tables that don't exist, and then tables that already exist. This is ok.
