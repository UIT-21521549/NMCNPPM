import pyodbc

def user_login(acc, pas):
    server = 'LAPTOP-3011TS14'
    database = 'NMCNPM'
    connection_string = f'DRIVER=ODBC Driver 17 for SQL Server;SERVER={server};DATABASE={database};Trusted_Connection=yes'
    
    # Establish connection to the database
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()

    # Execute the query
    query = f"SELECT acc,pass,acess FROM login_user WHERE acc='{acc}'"
    check = cursor.execute(query)
    if check  == "None" and check == None:
        return None
    # Fetch the result
    result = cursor.fetchone()
    conn.close()
    if  result is not None:
        a, b, c = result
    else:
        b = None
    if b != pas:
        return None
    return result