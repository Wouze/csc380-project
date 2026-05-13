import mysql.connector

def get_connection(with_db=True):
    kwargs = {
        "host": "127.0.0.1",
        "user": "root",
        "password": ""
    }
    if with_db:
        kwargs["database"] = "hotel_management"
    return mysql.connector.connect(**kwargs)

