from psycopg2 import connect
from psycopg2.extensions import connection
import dotenv
import os

dotenv.load_dotenv()

SQL_FILE = "setup/pr.sql"
PR_DB_USER = os.getenv("PR_DB_USER")
PR_DB_NAME = os.getenv("PR_DB_NAME")
PR_DB_PASSWORD = os.getenv("PR_DB_PASSWORD")
PR_DB_HOST = os.getenv("PR_DB_HOST")
PR_DB_PORT = os.getenv("PR_DB_PORT")


def read_sql_file(file_path: str):
    """
    Read the SQL file and return its content.
    """
    with open(file_path, "r") as file:
        sql_content = file.read()
    return sql_content


def execute_sql(conn: connection, sql: str):
    """
    Execute the SQL command.
    """
    with conn.cursor() as cursor:
        cursor.execute(sql)
        conn.commit()


def create_pr_tables():
    """
    Create the pr tables in the database.
    """
    with connect(
        dbname=PR_DB_NAME,
        user=PR_DB_USER,
        password=PR_DB_PASSWORD,
        host=PR_DB_HOST,
        port=PR_DB_PORT,
    ) as conn:
        sql = read_sql_file(SQL_FILE)
        execute_sql(conn, sql)


if __name__ == "__main__":
    print("Connecting with the following settings:")
    print(f"Host: {PR_DB_HOST}")
    print(f"Port: {PR_DB_PORT}")
    print(f"User: {PR_DB_USER}")
    print(f"DB Name: {PR_DB_NAME}")
    print(f"Password: {PR_DB_PASSWORD}")
    create_pr_tables()
    print("Pr tables created successfully.")
