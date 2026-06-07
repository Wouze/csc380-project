import mysql.connector

def get_connection(with_db=True):
    kwargs = {
        "host": "127.0.0.1",
        "user": "root",
        "password": ""
    }
    if with_db:
        kwargs["database"] = "car_rental"
    return mysql.connector.connect(**kwargs)

