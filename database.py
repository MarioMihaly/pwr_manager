# TODO
# add protection against SQL injection

import mysql.connector
from mysql.connector.errors import DataError
from constants import COLUMN_SELECTION, SITE_COL

DATABASES = 'DATABASES'
TABLES = 'TABLES'

class Database:
    def __init__(self, host, user, database, password):
        '''
            Costume class for MySQL database.

            Arguments:
                host:       name of the machine running the MySQL database.
                user:       user connecting to the database.
                database:   name of the database.
                password:   password of the user.
        '''

        self.host = host
        self.user = user

        self.connect_database(database, password)

    def connect_database(self, database, password):
        '''
            Method to connect to a database.

            Arguments:
                database: name of the database.
                password: password of the user connecting to the database.
        '''
        
        try:
            self.connection =  mysql.connector.connect(host=self.host, user=self.user, password=password, database=database)
        except:
            self.connection = mysql.connector.connect(host=self.host, user=self.user, password=password)
            self.new_database(database)
            self.connection =  mysql.connector.connect(host=self.host, user=self.user, password=password, database=database)

    def new_database(self, database):
        '''
            Method to create a new database if it does not exists already.

            Arguments:
                database: name of the new database.
        '''

        if self.exists(database, DATABASES):
            print(f'Database {database} already exists.')
            return
        
        cursor = self.connection.cursor()
        cursor.execute(f'CREATE DATABASE {database}')
        cursor.close()

    def new_table(self, name, cols):
        '''
            Method to create new table in the current database.

            Arguments:
                name: name of the new table.
                cols: list of (column_name, column_type).
        '''

        if self.exists(name, TABLES):
            print(f'Table {name} already exists.')
            return

        columns = ', '.join([f'{c[0]} {c[1]}' for c in cols])
        cursor = self.connection.cursor()
        cursor.execute(f'CREATE TABLE {name} ({columns})')
        cursor.close()

    def exists(self, name, type):
        '''
            Method to check for existing database or table.

            Arguments:
                name:   name of the database or table.
                type:   DATABASES | TABLES
        '''

        if type.upper() not in {DATABASES, TABLES}:
            print('Invalid type for checking existance of database or table!', type)

        cursor = self.connection.cursor()
        cursor.execute(f'SHOW {type.upper()}')
        selection = cursor.fetchall()
        cursor.close()

        return (name,) in selection

    def delete(self, name, type):
        '''
            Method to delete an existing database or table.

            Arguments:
                name:   name of the database or table.
                type:   DATABASES | TABLES
        '''

        if type.upper() not in {DATABASES, TABLES}:
            print('Invalid type for deleting existing database or table!', type)

        cursor = self.connection.cursor()
        cursor.execute(f'DROP {type.upper()} IF EXISTS {name}')
        cursor.close()  

    def in_table(self, table, column, value):
        '''
            Method to check value in a given column of a table.

            Arguments:
                table:  name of the table.
                column: column to search.
                value:  value of entry in column.
        '''

        if not self.exists(table, TABLES):
            print(f'Table {table} does not exists.')
            return
        
        if not self.valid_column(table, column):
            print(f'Column {column} not in table {table}.')
            return
        
        cursor = self.connection.cursor()
        cursor.execute(f'SELECT {column} FROM {table}')
        entries = cursor.fetchall()
        cursor.close()
        
        return (value,) in entries

    def valid_column(self, table, column):
        '''
            Method to check column is in a table.

            Arguments:
                table:  name of the table.
                column: name of the column.
        '''
        
        if not self.exists(table, 'TABLES'):
            print(f'Table {table} does not exists.')
            return

        cursor = self.connection.cursor()
        cursor.execute(f'SHOW COLUMNS FROM {table} like "{column}"')
        columns = cursor.fetchall()
        cursor.close()

        return len(columns) != 0

    def get_entry(self, table, column, value, return_column=None):
        '''
            Method to return value of column specifed by return_column in the first
            entry with given value in a column in a table. If return_column is not
            specified, the whole entry is returned.

            Arguments:
                table: name of the table.
                column: name of the column to search for value.
                value: value of entry in column.
                return_column (optional): name of column for which entry is returned.
        '''

        if not self.exists(table, TABLES):
            print(f'Table {table} does not exists.')
            return

        if not self.valid_column(table, column):
            print(f'Table {table} does not have {column} column.')
            return

        cursor = self.connection.cursor()
        cursor.execute(f"SELECT * FROM {table} WHERE {column} = '{value}'")
        entries = cursor.fetchall()
        cursor.close()
        
        if return_column == None:
            return entries[0]

        if return_column not in COLUMN_SELECTION:
            print(f'Invalid return column {return_column}.')
            return None
        
        if len(entries) == 0:
            print('No entries found.')
            return None

        return entries[0][COLUMN_SELECTION[return_column]]

    def get_entries(self, table, columns=None):
        '''
            Method to return specific columns of all entries in table.
            If no columns are specified, everything is returned.

            Arguments:
                table: name of the table.
                column (optional): list of column names -> columns to return.
        '''
        
        if not self.exists(table, TABLES):
            print(f'Table {table} does not exists.')
            return None
        if columns:
            for column in columns:
                if not self.valid_column(table, column):
                    print('Invalid column selection.')
                    return None 

        if columns == None:
            cols = '*'
        else:
            cols = ', '.join(columns)

        cursor = self.connection.cursor()
        sql = f'SELECT {cols} FROM {table}'
        cursor.execute(sql)
        entries = cursor.fetchall()
        cursor.close()

        return entries

    def insert(self, table, values):
        '''
            Method to insert a complete row into a table.

            Arguments:
                table:  name of the table.
                values: list of values in the order of the columns.
        '''

        if not self.exists(table, TABLES):
            print(f'Table {table} does not exists.')
            return
        
        try:
            values_str = ', '.join(['%s'] * len(values))
            cursor = self.connection.cursor()
            sql = f'INSERT INTO {table} VALUES ({values_str})'
            cursor.execute(sql, values)
            self.connection.commit()
            cursor.close()
        
        except DataError as e:
            print(f'Incorrect number of values when inserting entries into table {table}.')

    def update(self, table, site, column, new_value):
        '''
            Method to update the value of a cell in a table.

            Arguments:
                table: name of the table.
                site: name of site to update.
                column: name of the column containing the cell to update.
                new_value: new value for the cell.
        '''
        
        if not self.exists(table, TABLES):
            print(f'Table {table} does not exists.')
            return

        if not self.valid_column(table, column):
            print(f'Table {table} does not have {column} column.')
            return

        if not self.in_table(table, 'site', site):
            print(f'No entry for {site}.')
            return

        cursor = self.connection.cursor()
        sql = f'UPDATE {table} SET {column} = %s WHERE {SITE_COL} = %s'
        val = (new_value, site)
        cursor.execute(sql, val)
        self.connection.commit()
        cursor.close()

    def delete(self, table, site):
        '''
            Method to delete entry from a table specified by the site name.

            Arguments:
                table: name of the table.
                site: name of the site.
        '''

        if not self.exists(table, TABLES):
            print(f'Table {table} does not exists.')
            return

        if not self.in_table(table, SITE_COL, site):
            print(f'No entry for site {site} in {table}')
            return

        cursor = self.connection.cursor()
        sql = f'DELETE FROM {table} WHERE {SITE_COL} = %s'
        val = (site,)
        cursor.execute(sql, val)
        self.connection.commit()
        cursor.close()

    def reset_table(self, table):
        '''
            Method to reset the content of a table.

            Arguments:
                table: name of the table.
        '''

        if not self.exists(table, TABLES):
            print(f'Table {table} does not exists.')
            return

        cursor = self.connection.cursor()
        cursor.execute(f'TRUNCATE TABLE {table}')
        cursor.close()

    def change_password(self, new_password):
        '''
            Method to change user password for the database.

            Arguments:
                new_password: new password for the database.
        '''
        cursor = self.connection.cursor()
        sql = f'ALTER USER {self.user}@{self.host} IDENTIFIED BY "{new_password}"'
        cursor.execute(sql)
        cursor.close()

    def exit(self):
        self.connection.close()
