from flask import Flask, jsonify, render_template, request
import pymysql
import argparse

app = Flask(__name__)

def connect_to_db(host, user, password, db, charset="utf8mb4", cursorclass=pymysql.cursors.DictCursor):
    """Connects to a MySQL database."""
    try:
        connection = pymysql.connect(
            host=host,
            user=user,
            password=password,
            db=db,
            charset=charset,
            cursorclass=cursorclass
        )
        print("Connected to the database!")
        return connection
    except pymysql.MySQLError as e:
        print(f"Error connecting to the database: {e}")
        return None

def get_db_connection():
    """Gets a database connection using command-line arguments."""
    parser = argparse.ArgumentParser(description="Connect to a MySQL database.")
    parser.add_argument("host", help="MySQL host")
    parser.add_argument("user", help="MySQL user")
    parser.add_argument("password", help="MySQL password")
    parser.add_argument("db", help="MySQL database")
    parser.add_argument("--charset", type=str, default="utf8mb4")

    args = parser.parse_args()

    return connect_to_db(
        args.host, args.user, args.password, args.db, args.charset, pymysql.cursors.DictCursor
    )

@app.route('/health')
def health():
    return "Up & Running"

@app.route('/create_table')
def create_table():
    connection = get_db_connection()
    cursor = connection.cursor()
    create_table_query = """
        CREATE TABLE IF NOT EXISTS example_table (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL
        )
    """
    cursor.execute(create_table_query)
    connection.commit()
    connection.close()
    return "Table created successfully"

@app.route('/insert_record', methods=['POST'])
def insert_record():
    name = request.json['name']
    connection = get_db_connection()
    cursor = connection.cursor()
    insert_query = "INSERT INTO example_table (name) VALUES (%s)"
    cursor.execute(insert_query, (name,))
    connection.commit()
    connection.close()
    return "Record inserted successfully"

@app.route('/data')
def data():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM example_table')
    result = cursor.fetchall()
    connection.close()
    return jsonify(result)

# UI route
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':

    app.run(debug=False, host='0.0.0.0')
