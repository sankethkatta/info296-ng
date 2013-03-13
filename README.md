# INFO 296 - NG Project

## Environment Set-Up

There are two packages:

1. [SQLAlchemy](http://www.sqlalchemy.org/)
2. [psycopg](http://initd.org/psycopg/)

`easy_install` or `pip` would work to install these:

```
pip install -r requirements.txt
```
or
```
easy_install sqlalchemy
easy_install psycopg2
```

### Test that it all worked:
    
```
python -i models.py

>>> engine.execute("SELECT 1").scalar()
1
```
If you get the `1` back, you have connected to the db sucessfully!

