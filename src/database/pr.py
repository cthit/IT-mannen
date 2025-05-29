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
        "INSERT INTO Posts (description, file_name, start_time, end_time, owner) VALUES (%s, %s, %s, %s, %s);",
        (description, file_name, start_time_parsed, end_time_parsed, "admin"),
    )


@pr_cursor
def delete_post(cur: cursor, id: int):
    cur.execute("DELETE FROM Posts WHERE id=%s;", (id,))


@pr_cursor
def change_post_description(cur: cursor, id: int, new_description: str):
    cur.execute("UPDATE Posts SET description=%s WHERE id=%s;", (new_description, id))


@pr_cursor
def change_post_times(cur: cursor, id: int, new_start_time: str, new_end_time: str):
    new_start_time_parsed: datetime = parse(new_start_time)
    new_end_time_parsed: datetime = parse(new_end_time)

    cur.execute(
        "UPDATE Posts SET start_time=%s, end_time=%s WHERE id=%s;",
        (new_start_time_parsed, new_end_time_parsed, id),
    )


@pr_cursor
def get_post(cur: cursor, id: int) -> tuple[str, str, datetime, datetime, str]:
    cur.execute(
        "SELECT description, file_name, start_time, end_time, owner FROM Posts WHERE id=%s;",
        (id,),
    )
    row = cur.fetchone()
    if row is None:
        raise ValueError(f"No post found with id {id}")

    post: tuple[str, str, datetime, datetime, str] = row
    return post


@pr_cursor
def create_postview(cur: cursor, route: str, name: str):
    cur.execute(
        "INSERT INTO PostViews (route, name, owner) VALUES (%s, %s, %s);",
        (route, name, "admin"),
    )


@pr_cursor
def delete_postview(cur: cursor, id: int):
    cur.execute("DELETE FROM PostViews WHERE id=%s;", (id,))


@pr_cursor
def change_postview_name(cur: cursor, id: int, new_name: str):
    cur.execute("UPDATE PostViews SET name=%s WHERE id=%s;", (new_name, id))


@pr_cursor
def change_postview_route(cur: cursor, id: int, new_route: str):
    cur.execute("UPDATE PostViews SET route=%s WHERE id=%s;", (new_route, id))


@pr_cursor
def get_groups_postviews(cur: cursor, group: str) -> list[tuple[int, str, str]]:
    cur.execute("SELECT id, route, name FROM PostViews WHERE owner=%s;", (group,))

    postviews: list[tuple[int, str, str]] = cur.fetchall()
    return postviews


@pr_cursor
def add_post_to_postview(cur: cursor, view_id: int, post_id: int):
    cur.execute(
        "INSERT INTO PostViewContents (view_id, post_id) VALUES (%s, %s);",
        (view_id, post_id),
    )


@pr_cursor
def remove_post_from_postview(cur: cursor, view_id: int, post_id: int):
    cur.execute(
        "DELETE FROM PostViewContents WHERE view_id=%s AND post_id=%s;",
        (view_id, post_id),
    )


@pr_cursor
def get_content_from_postview(cur: cursor, view_id: int) -> list[int]:
    cur.execute("SELECT post_id FROM PostViewContents WHERE view_id=%s;", (view_id,))
    rows: list[tuple[int]] = cur.fetchall()
    posts: list[int] = [row[0] for row in rows]

    return posts
