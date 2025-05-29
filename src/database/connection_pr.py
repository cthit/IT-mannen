import psycopg2
import dotenv
import os
from psycopg2.extensions import cursor, connection
from typing import Callable, Concatenate, ParamSpec, TypeVar
from functools import wraps

dotenv.load_dotenv()

PR_DB_USER = os.getenv("PR_DB_USER")
PR_DB_NAME = os.getenv("PR_DB_NAME")
PR_DB_PASSWORD = os.getenv("PR_DB_PASSWORD")
PR_DB_HOST = os.getenv("PR_DB_HOST")
PR_DB_PORT = os.getenv("PR_DB_PORT")


def create_connection_pr() -> connection:
    conn = psycopg2.connect(
        database=PR_DB_NAME,
        user=PR_DB_USER,
        password=PR_DB_PASSWORD,
        host=PR_DB_HOST,
        port=PR_DB_PORT,
    )
    return conn


T = TypeVar("T")
P = ParamSpec("P")


def pr_cursor(f: Callable[Concatenate[cursor, P], T]) -> Callable[P, T]:
    """
    Decorator to inject a cursor as the first argument.
    """

    @wraps(f)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        with create_connection_pr() as conn:
            with conn.cursor() as cur:
                return f(cur, *args, **kwargs)

    return wrapper
