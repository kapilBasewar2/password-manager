import sqlite3

class DbOperations:

    def connect_to_db(self):

        conn =sqlite3.connect('password_record.db')
        return conn

    def create_table(self,table_name="password_manager"):
        conn = self.connect_to_db()
        query=f'''
        CREATE TABLE If NOT EXISTS {table_name}(
            ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            gmail_id VARCHAR(200) NOT NULL,
            website VARCHAR(200) NOT NULL,
            username VARCHAR(200) NOT NULL,
            password VARCHAR(50) NOT NULL
        );
        '''

        with conn as conn:
            cursor = conn.cursor()
            cursor.execute(query)

    def create_record(self,data,table_name="password_manager"):
        gmail_id = data['gmail_id']
        website =data['website']
        username =data['username']
        password =data['password']
        conn = self.connect_to_db()
        query = f'''
        INSERT INTO {table_name} ('gmail_id','website','username','password') VALUES ( ?, ?, ?, ?);
        '''
        with conn as conn:
            cursor =conn.cursor()
            cursor.execute(query,(gmail_id,website,username,password))
            # print("save the record", (website,username,password))

    def show_records(self,table_name="password_manager"):
        conn = self.connect_to_db()
        query = f'''
        SELECT * FROM {table_name};
        '''
        with conn as conn:
            cursor = conn.cursor()
            list_records = cursor.execute(query)
            return list_records


    def update_record(self, data, table_name="password_manager"):
        ID = data['ID']
        gmail_id = data['gmail_id']
        website = data['website']
        username = data['username']
        password = data['password']
        conn = self.connect_to_db()
        query = f'''
        UPDATE {table_name} SET gmail_id = ?, website = ?, username = ?, password = ? WHERE ID = ?;
        '''
        with conn as conn:
            cursor = conn.cursor()
            cursor.execute(query, (gmail_id, website, username, password, ID))

            
    def delete_record(self, record_id, table_name="password_manager"):
        conn = self.connect_to_db()
        query = f'''
        DELETE FROM {table_name} WHERE ID = ?;
        '''
        with conn as conn:
            cursor = conn.cursor()
            cursor.execute(query, (record_id,))

    def delete_all_record(self, table_name="password_manager"):
        conn = self.connect_to_db()
        delete_query = f"""
        DELETE FROM {table_name};
    """
    
        reset_id_query = f"""
        UPDATE sqlite_sequence SET seq = 0 WHERE name = '{table_name}';
    """

        with conn as conn:
            cursor = conn.cursor()
            cursor.execute(delete_query)
            cursor.execute(reset_id_query)



    def search_records(self, website=None, username=None, table_name="password_manager"):
        conn = self.connect_to_db()

        # Create the WHERE clause based on the provided website and username
        where_clause = ""
        if website:
            where_clause += f"website LIKE '%{website}%'"
        if username:
            if where_clause:
                where_clause += " AND "
            where_clause += f"username LIKE '%{username}%'"

        # Construct the query with the WHERE clause
        query = f"""
        SELECT * FROM {table_name}
        """
        if where_clause:
            query += f"WHERE {where_clause};"
        else:
            query += ";"

        with conn as conn:
            cursor = conn.cursor()
            list_records = cursor.execute(query)
            return list_records.fetchall()

    def is_record_exists(self, record_id, table_name="password_manager"):
        conn = self.connect_to_db()
        query = f'''
            SELECT COUNT(*) FROM {table_name} WHERE ID = ?;
        '''
        with conn as conn:
            cursor = conn.cursor()
            cursor.execute(query, (record_id,))
            count = cursor.fetchone()[0]
            return count > 0
  