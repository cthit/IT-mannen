from psycopg2.extensions import cursor
from dateutil.parser import parse
from datetime import datetime

from database.connection_pr import pr_cursor
from database.pr_tuples import *


@pr_cursor
def create_group(cur: cursor, group_name: str):
    cur.execute("INSERT INTO Groups (name) VALUES (%s);", (group_name,))


@pr_cursor
def create_post(cur: cursor, description: str, file_name: str):

    cur.execute(
        "INSERT INTO Posts (description, file_name, owner) VALUES (%s, %s, %s);",
        (description, file_name, "admin"),
    )

## this creates aboth a post and a timed post entry, with the same id
@pr_cursor
def create_timed_post(cur: cursor, description: str, file_name: str, start_time: str, end_time: str) -> int:
    start_time_parsed: datetime = start_time
    end_time_parsed: datetime = end_time

    cur.execute(
        "INSERT INTO Posts (description, file_name, owner) VALUES (%s, %s, %s) RETURNING id;",
        (description, file_name, "admin"),
    )
    post_id: int = cur.fetchone()[0]

    cur.execute(
        "INSERT INTO TimedPosts VALUES (%s, %s, %s);",
        (post_id, start_time_parsed, end_time_parsed),
    )

    return post_id

@pr_cursor
def delete_post(cur: cursor, post_id: int):
    cur.execute("DELETE FROM Posts WHERE id=%s;", (post_id,))


@pr_cursor
def change_post(cur: cursor, post_id: int, new_description: str):

    cur.execute(
        "UPDATE Posts SET description=%s WHERE id=%s;", (new_description, post_id)
    )

## this only creates a timed post entry, the post must already exist
@pr_cursor
def set_timed_post(cur: cursor, post_id: int, start_time: str, end_time: str):
    start_time_parsed: datetime = parse(start_time)
    end_time_parsed: datetime = parse(end_time)

    cur.execute(
        "INSERT INTO TimedPosts VALUES (%s, %s, %s);",
        (post_id, start_time_parsed, end_time_parsed),
    )


@pr_cursor
def remove_timed_post(cur: cursor, post_id: int):
    cur.execute("DELETE FROM TimedPosts WHERE id=%s;", (post_id,))


@pr_cursor
def get_timed_post(cur: cursor, post_id: int) -> TimedPost:
    cur.execute(
        "SELECT id, start_time, end_time FROM TimedPosts WHERE id=%s;", (post_id,)
    )
    row: tuple[int, datetime, datetime] | None = cur.fetchone()

    if row is None:
        raise ValueError(f"Post {post_id} is not a timed post")

    post: TimedPost = TimedPost(row[0], row[1], row[2])
    return post


@pr_cursor
def change_timed_post(
    cur: cursor,
    post_id: int,
    new_start_time: str | None = None,
    new_end_time: str | None = None,
):
    fields: list[str] = []
    values: list[datetime | int] = []

    if new_start_time is not None:
        fields.append("start_time=%s")
        new_start_time_parsed: datetime = parse(new_start_time)
        values.append(new_start_time_parsed)

    if new_end_time is not None:
        fields.append("end_time=%s")
        new_end_time_parsed: datetime = parse(new_end_time)
        values.append(new_end_time_parsed)

    if not fields:
        return

    values.append(post_id)
    cur.execute(f"UPDATE TimedPosts SET {', '.join(fields)} WHERE id=%s;", values)


@pr_cursor
def get_groups_posts(cur: cursor, owner_group: str) -> tuple[Post, ...]:
    cur.execute(
        """SELECT p.id, p.description, p.file_name, tp.id IS NOT NULL AS is_timed 
        FROM Posts p 
        LEFT JOIN TimedPosts tp ON p.id=tp.id 
        WHERE owner=%s;""",
        (owner_group,),
    )

    rows: list[tuple[int, str, str, bool]] = cur.fetchall()
    posts: tuple[Post, ...] = tuple(
        Post(row[0], row[1], row[2], row[3]) for row in rows
    )
    return posts


@pr_cursor
def create_postview(cur: cursor, name: str):
    cur.execute(
        "INSERT INTO PostViews (name, owner) VALUES (%s, %s, %s);",
        (name, "admin"),
    )


@pr_cursor
def delete_postview(cur: cursor, postview_id: int):
    cur.execute("DELETE FROM PostViews WHERE id=%s;", (postview_id,))


@pr_cursor
def change_postview(
    cur: cursor, postview_id: int, name: str | None = None
):
    fields: list[str] = []
    values: list[int | str] = []

    if name is not None:
        fields.append("name=%s")
        values.append(name)

    if not fields:
        return

    values.append(postview_id)
    cur.execute(f"UPDATE PostViews SET {', '.join(fields)} WHERE id=%s;", values)


@pr_cursor
def get_postviews(cur:cursor) -> tuple[PostView, ...]:
    cur.execute("SELECT id, name FROM PostViews")
    rows: list[tuple[int, str]] = cur.fetchall()

    postviews: tuple[PostView, ...] = tuple(
        PostView(row[0], row[1]) for row in rows
    )
    return postviews


@pr_cursor
def get_groups_postviews(cur: cursor, owner_group: str) -> tuple[PostView, ...]:
    cur.execute("SELECT id name FROM PostViews WHERE owner=%s;", (owner_group,))
    rows: list[tuple[int, str]] = cur.fetchall()

    postviews: tuple[PostView, ...] = tuple(
        PostView(row[0], row[1]) for row in rows
    )
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
def get_content_from_postview(cur: cursor, view_id: int) -> tuple[Post, ...]:
    cur.execute(
        """SELECT p.id, p.description, p.file_name, tp.id IS NOT NULL AS is_timed 
        FROM Posts p JOIN PostViewContents pvc ON p.id=pvc.post_id
        LEFT JOIN TimedPosts tp ON p.id=tp.id 
        WHERE pvc.view_id=%s;""",
        (view_id,),
    )
    rows: list[tuple[int, str, str, bool]] = cur.fetchall()

    posts: tuple[Post, ...] = tuple(
        Post(row[0], row[1], row[2], row[3]) for row in rows
    )
    return posts
