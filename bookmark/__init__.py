from flask import Flask

app = Flask(__name__)

from bookmark.api.routes import bookmarks
from bookmark.api.routes import api_obj
from bookmark.api.routes import Bookmark

#register blueprint with app
app.register_blueprint(api.routes.bookmarks, url_prefix='/api')

