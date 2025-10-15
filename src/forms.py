from collections.abc import Sequence
from typing import Any, Mapping
from flask_wtf import FlaskForm  # type: ignore
from flask_wtf.file import FileField, FileRequired, FileAllowed  # type: ignore
from wtforms import StringField, BooleanField, SubmitField, SelectMultipleField
from wtforms.fields import DateTimeLocalField
from wtforms.validators import InputRequired


class delete_button_form(FlaskForm):
    submit = SubmitField("Delete")


class modify_button_form(FlaskForm):
    submit = SubmitField("Modify")


class create_post_form(FlaskForm):
    description = StringField("description", validators=[InputRequired()])
    file = FileField(
        "file", validators=[FileRequired(), FileAllowed(["png"], "png images only!")]
    )
    is_timed = BooleanField("Timed post?")
    start_time = DateTimeLocalField("Start time", format="%Y-%m-%dT%H:%M")
    end_time = DateTimeLocalField("End time", format="%Y-%m-%dT%H:%M")
    submit = SubmitField("Create post")

    def validate(
        self, extra_validators: Mapping[str, Sequence[Any]] | None = None
    ) -> bool:

        default_validators = super().validate(extra_validators)
        start_time, end_time = self.start_time.data, self.end_time.data

        if not default_validators:
            return default_validators

        if not self.is_timed.data:
            return True

        if not start_time:
            self.start_time.errors.append("Start time is required for timed posts")
            return False

        if not end_time:
            self.end_time.errors.append("End time is required for timed posts")
            return False

        if end_time <= start_time:
            self.end_time.errors.append("End time must be strictly after start time")
            return False

        return True


class modify_post_form(FlaskForm):
    description = StringField("description", validators=[InputRequired()])
    is_timed = BooleanField("Timed post?")
    start_time = DateTimeLocalField("Start time", format="%Y-%m-%dT%H:%M")
    end_time = DateTimeLocalField("End time", format="%Y-%m-%dT%H:%M")
    submit = SubmitField("Save changes")


class create_slideshow_form(FlaskForm):
    name = StringField("Name", validators=[InputRequired()])
    submit = SubmitField("Create view")


class edit_slideshow_form(FlaskForm):
    post_ids = SelectMultipleField("Post IDs", coerce=int)
    submit = SubmitField("Modify view")
