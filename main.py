
#import statement

import sqlite3
from sqlite3 import Cursor

import streamlit as st
#database connection
def connect_to_db():
    engine = create_engine ('sqlite:///C:/Users/hp1/Desktop/SAMPLE.sqlite.db')
    connection = engine.connect ()
    return connection
#connect_to_db(): This function is intended to create a connection to the SQLite database using SQLAlchemy's create_engine, but there is an issue as create_engine is not imported.

def list_tables(connection):
    try:
        result = connection.execute (text ("SELECT name FROM sqlite_master WHERE type='table';"))
        tables = [row[0] for row in result]
        return tables
    except Exception as e:
        st.error (f"An error occurred while listing tables: {e}")
        return []

#list_tables(connection): Retrieves the names of all tables in the SQLite database. It uses SQL query to get table names and handles any errors that occur.
def fetch_data(user_input, connection, table_names, column_names):
    try:
        data = []
        query_template = 'SELECT * FROM "{}" WHERE "{}" LIKE :user_input'

        for table_name in table_names:

            for column_name in column_names:
                query = query_template.format (table_name, column_name)
                result = connection.execute (text (query), {'user_input': f'%{user_input}%'})
                for row in result:
                    data.append (row)
        return data
    except Exception as e:
        st.error (f"An error occurred: {e}")
        return []



#fetch_data(user_input, connection, table_names, column_names): Queries the database for records where the user_input is found in specified columns of specified tables. Handles exceptions by showing an error message.
#format_numbers(numbers): Formats a space-separated string of numbers into a SQL IN clause. It wraps each number in single quotes and joins them into a list for SQL query.
def format_numbers(numbers):
    formatted_nums = []
    for num in numbers.split ():
        formatted_nums.append (f"'{num}'")

    return f'"PCA Barcode" IN ({", ".join (formatted_nums)})'


def main():
    st.title ("BarcodeOps")
    numbers = st.text_area ("Enter serial numbers (space-separated):")

    st.button ("Format")
    formatted = format_numbers (numbers)
    st.write ("Output query")
    st.code (formatted)


if __name__ == "__main__":
    main ()

import os

print ("C:/Users/hp1/PycharmProjects/barcode_app.py/sample.db", os.getcwd ())

# Construct absolute path to the database file
# Correct usage of f-string with a literal path
print (f"Database file 'C:/Users/hp1/Desktop/SAMPLE.sqlite' found.")

import os

print (f"Database file 'C:/Users/hp1/Desktop/SAMPLE.sqlite' found.")

if os.path.isfile (f"Database file 'C:/Users/hp1/Desktop/SAMPLE.sqlite"):

    print (f"Database file 'C:/Users/hp1/Desktop/SAMPLE.sqlite' found.")

else:

    print (f"Database file 'C:/Users/hp1/Desktop/SAMPLE.sqlite' found.")
import streamlit as st
import pandas as pd
import sqlite3


def get_table_names(conn):
    query = "SELECT name FROM sqlite_master WHERE type='table';"
    tables = pd.read_sql (query, conn)['name'].tolist ()
    return tables


def fetch_data(conn, table_name, offset, limit):
    query = f'SELECT * FROM "{table_name}" LIMIT {limit} OFFSET {offset}'
    data = pd.read_sql (query, conn)
    return data


def get_total_rows(conn, table_name):
    query = f'SELECT COUNT(*) FROM "{table_name}"'
    total_rows = pd.read_sql (query, conn).iloc[0, 0]
    return total_rows


def get_columns(conn, table_name):
    query = f'PRAGMA table_info("{table_name}");'
    columns = pd.read_sql (query, conn)
    return columns


conn = sqlite3.connect ('C:/Users/hp1/Desktop/SAMPLE.sqlite')

table_names = get_table_names (conn)

selected_table = st.selectbox ("Select a table", table_names)

columns = get_columns (conn, selected_table)
st.write ("Columns:", columns)

page_size = 1000
page_number = st.number_input ("Page number", min_value=1, value=1, step=1, key='page_number_input')

offset = (page_number - 1) * page_size

data = fetch_data (conn, selected_table, offset, page_size)
st.dataframe (data)

primaryColor = '#1f77b4'
backgroundColor = '#f0f2f6'
secondaryBackgroundColor = '#ffffff'
textColor = '#262730'
font = 'sans serif'
import sqlite3

conn = sqlite3.connect ('C:/Users/hp1/Desktop/SAMPLE.sqlite')
c = conn.cursor ()

table_name = '"1_P_FULL_ASSEMBLY_FT_NEUTRAL_CURRENT"'
c.execute (f"PRAGMA table_info({table_name})")
columns = c.fetchall ()

for column in columns:
    print (column[1])

conn.close ()

import streamlit as st
import sqlite3
import pandas as pd


st.title ('Barcode Data Lookup for Selected Table')
st.write (
    'Select a table to see its structure and optionally enter multiple barcodes separated by commas to retrieve related data.')

table_columns = {
    '1_P_FULL_ASSEMBLY_FT_NEUTRAL_CURRENT': 'PCA Barcode mismatch',
    '1_P_FULL_ASSEMBLY_FT': 'PCA Barcode mismatch',
    '1P_EESL_NEO4G_FA': 'PCA Barcode',
    '1P_EESL_NEO4G_PCA': 'PCA Barcode',
    '3P EESL NEO4G FA': 'PCA Barcode',
    'ALPHA_R': 'Barcode',
    'CHRONUS': 'PCA Barcode',
    'CYGNUS': 'Barcode',
    'JIO_NBIOT': 'PCA Barcode',
    'MERCURY': 'Barcode',
    'NORTEM': 'PCA Barcode',
    'SFF': 'Barcode',
    'SM_19_E': 'Barcode'

}

selected_table = st.selectbox ('Select a table:', list (table_columns.keys ()), key='unique_table_select')


conn = sqlite3.connect ('C:/Users/hp1/Desktop/SAMPLE.sqlite')
c = conn.cursor ()

def table_exists(conn, table_name):
    c = conn.cursor ()
    c.execute (f'SELECT name FROM sqlite_master WHERE type="table" AND name="{table_name}"')
    return c.fetchone () is not None


def list_columns(conn, table_name):
    c = conn.cursor ()
    c.execute (f'PRAGMA table_info("{table_name}")')
    return [column[1] for column in c.fetchall ()]


if selected_table:
    if table_exists (conn, selected_table):
        columns = list_columns (conn, selected_table)
        st.write (f"Columns in {selected_table}: {columns}")
    else:
        st.write (f'Table {selected_table} does not exist in the database.')


barcodes_input = st.text_area ('Enter barcodes separated by commas:', key='unique_barcodes_input_textarea')


def query_database(conn, table, barcode_column, barcodes):
    c = conn.cursor ()
    placeholders = ','.join (['?' for _ in barcodes])
    query = f'SELECT * FROM "{table}" WHERE "{barcode_column}" IN ({placeholders})'
    c.execute (query, barcodes)
    return c.fetchall (), [description[0] for description in c.description]



if barcodes_input and selected_table:
    barcodes = [barcode.strip () for barcode in barcodes_input.split (',') if barcode.strip ()]

    if barcodes:
        if table_exists (conn, selected_table):
            barcode_column = table_columns[selected_table]
            try:
                results, columns = query_database (conn, selected_table, barcode_column, barcodes)

                if results:
                    st.write (f'Related data from {selected_table}:')
                    # Display results in a table
                    df = pd.DataFrame (results, columns=columns)
                    st.dataframe (df)
                else:
                    st.write (f'No data found for the entered barcodes in {selected_table}.')

            except sqlite3.Error as e:
                st.error (f"An error occurred while querying {selected_table}: {e}")
        else:
            st.write (f'Table {selected_table} does not exist in the database.')


conn.close ()
