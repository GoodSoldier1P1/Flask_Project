from flask import Blueprint

posts = Blueprint('posts', __name__, template_folder='posts_templates')

from . import routes