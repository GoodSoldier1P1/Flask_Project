from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.validators import DataRequired, EqualTo

class PostForm(FlaskForm):
    title = StringField('Title: ')
    caption = StringField('Caption')
    img_url = StringField('Image URL:  ', validators=[DataRequired()])
    submit_btn = SubmitField('Create Post')