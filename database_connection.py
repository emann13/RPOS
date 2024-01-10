from django.shortcuts import render


import pyodbc

def get_sql_anywhere_connection():
    server = 'ECS_RPOS_T001'
    port = '10.5.0.8'
    database = 'ECS_RPOS_T001'
    username = 'dba'
    password = 'BM@12345246810_mb'

    connection_string = (
        f"DRIVER={{SQL AnyWhere 17}};"
        f"Server={server};Port={port};Database={database};"
        f"UID={username};PWD={password};"
        f"Links=tcpip"
    )

    connection = pyodbc.connect(connection_string)
    cursor = connection.cursor()
    
    return connection, cursor

