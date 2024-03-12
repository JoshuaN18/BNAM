Drop the database
```sql
DROP SCHEMA public CASCADE;
CREATE SCHEMA public;
```

```sql
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO public;
```

Then
```
python manage.py migrate
```