from flask_wtf import FlaskForm  # type: ignore
from flask_wtf.file import FileField, FileRequired, FileAllowed  # type: ignore
from wtforms import StringField, BooleanField, SubmitField
from wtforms.fields import DateTimeLocalField
from wtforms.validators import InputRequired


class delete_button_form(FlaskForm):
    submit = SubmitField("Delete")


class modify_button_form(FlaskForm):
    submit = SubmitField("Modify")


class create_post_form(FlaskForm):
    description = StringField("description", validators=[InputRequired()])
    file = FileField(
        "file", validators=[FileRequired(), FileAllowed(["png", "jpg"], "Images only!")]
    )
    is_timed = BooleanField("Timed post?")
    start_time = DateTimeLocalField("Start time", format='%Y-%m-%dT%H:%M')
    end_time = DateTimeLocalField("End time", format='%Y-%m-%dT%H:%M')
    submit = SubmitField("Create post")


class modify_post_form(FlaskForm):
    description = StringField("description", validators=[InputRequired()])
    is_timed = BooleanField("Timed post?")
    start_time = DateTimeLocalField("Start time", format='%Y-%m-%dT%H:%M')
    end_time = DateTimeLocalField("End time", format='%Y-%m-%dT%H:%M')
    submit = SubmitField("Save changes")


class create_slideshow_form(FlaskForm):
    #route = StringField("Route", validators=[InputRequired()])
    name = StringField("Name", validators=[InputRequired()])
    submit = SubmitField("Create view")


class edit_slideshow_form(FlaskForm):
    name = StringField("Name", validators=[InputRequired()])
    post_ids = list[int]("Post IDs")
    submit = SubmitField("Modify view")
