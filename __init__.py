from flask import Flask

app = Flask(__name__, static_folder='static')
app.url_map.strict_slashes = False

app.jinja_options = app.jinja_options.copy()
app.jinja_options.update({
    'trim_blocks': True,
    'lstrip_blocks': True
})

app.config['DEBUG'] = True
app.config['SECRET_KEY'] = \
    'c05304a94025aa5936ad850d9e38961f901c63440e5a4659'

app.config['JSON_AS_ASCII'] = False

from app import views  # noqa
