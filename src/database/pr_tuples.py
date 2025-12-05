from typing import NamedTuple
from datetime import datetime


class Post(NamedTuple):
    id: int
    name: str
    description: str
    is_timed: bool


class TimedPost(NamedTuple):
    id: int
    start_time: datetime
    end_time: datetime


class FeaturedPost(NamedTuple):
    id: int
    name: str
    description: str
    is_timed: bool
    start_time: datetime
    end_time: datetime


class Slideshow(NamedTuple):
    id: int
    name: str
