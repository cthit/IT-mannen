from psycopg2.extensions import cursor
from dateutil.parser import parse
from datetime import datetime

from connection_pr import pr_cursor


@pr_cursor
def create_group(cur: cursor, name: str) -> None:
    cur.execute("INSERT INTO Groups (name) VALUES (%s);", (name,))


@pr_cursor
def create_post(
    cur: cursor, description: str, file_name: str, start_time: str, end_time: str
):
    start_time_parsed: datetime = parse(start_time)
    end_time_parsed: datetime = parse(end_time)

    cur.execute(
        "INSERT INTO Posts (description, file_name, start_time, end_time, owner) VALUES (%s, %s, %s, %s, admin)",
        (description, file_name, start_time_parsed, end_time_parsed),
    )


@pr_cursor
def create_postview(cur: cursor, route: str):
    cur.execute("INSERT INTO PostViews (route, owner) VALUES (%s, admin)", (route,))


@pr_cursor
def add_post_to_postview(cur: cursor, view_route: str, post_id: int):
    cur.execute(
        "INSERT INTO PostViewContents (view_route, post_id) VALUES (%s, %s)",
        (view_route, post_id),
    )
