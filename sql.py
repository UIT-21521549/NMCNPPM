import pyodbc

class User():
    def __init__(self, acc, pas, *args) -> None:
        if len(args) >= 1:
            self.name = args[0]
        else:
            self.name = None
        self.acc = acc
        self.pas = pas
        if len(args) >= 2:
            self.email = args[1]
        else:
            self.email = None


    @property
    def user_login(self):
        #init connect with sql
        server = 'LAPTOP-3011TS14'
        database = 'NMCNPM'
        connection_string = f'DRIVER=ODBC Driver 17 for SQL Server;SERVER={server};DATABASE={database};Trusted_Connection=yes'
        
        # Establish connection to the database
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()

        # Execute the query
        query = f"SELECT acc,pass,acess FROM login_user WHERE acc='{self.acc}'"
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
        
        if b != self.pas:
            return None
        return result

    @property
    def user_register(self):
        #init connect with sql
        server = 'LAPTOP-3011TS14'
        database = 'NMCNPM'
        connection_string = f'DRIVER=ODBC Driver 17 for SQL Server;SERVER={server};DATABASE={database};Trusted_Connection=yes'
        # Establish connection to the database
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()

        # Execute the query
        query = f"SELECT acc,pass,acess FROM login_user WHERE acc='{self.acc}'"
        check = list(cursor.execute(query))
        conn.close()
        if len(check) > 0:
            return "True"
        
        # Fetch the result
        # query = f"insert INTO login_user(acc,pass,acess) values ('{self.acc}', '{self.pas}', 'user')"
        # cursor.execute(query)
        # conn.commit()
        return "False"