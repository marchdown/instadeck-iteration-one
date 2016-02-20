# -*- coding: utf-8 -*-
"""
    Instadeck app
    ~~~~~~
"""

import os, re
from hashlib import sha1 as sha1
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
from flask.ext.sqlalchemy import SQLAlchemy

# FIXME: what are g, abort, flash

# FIXME: 
# complete switching to sqlalchemy
# cf http://blog.y3xz.com/blog/2012/08/16/flask-and-postgresql-on-heroku
class Deck(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True) # does postgres support autoincrement?
    slug =  db.Column(db.String(6))
    title = db.Column(db.String(400))
    unparsed_content = db.Column(db.String(8000)) #FIXME: think of appropriate size
    def __init__(self, title, content):
        self.title = title
        self.slug = slugify(contents)
        self.content = unparsed_content

    def __repr__(self):
#        return '%r <> %r' % self.slug, self.title
        return '%r' % self.slug

class Slide:
    def __init__(self, line):
        embedded = emb(line)
        if embedded:
            self.embedded = embedded
        else:
            self.embedded = None
            self.text     = line


# create our little application :)
app = Flask(__name__)

# Load default config and override config from an environment variable
if ('DATABASE_URL' in os.environ):
    squalchemy_database_uri = os.environ['DATABASE_URL']
else:
    raise Exception("Can't find database URI in os.environ")
    squalchemy_database_uri="postgres://uquxyjlmmjtbff:aie93RAT7ZN2aAjYgyx5C-L2A1@ec2-107-20-224-236.compute-1.amazonaws.com:5432/d3v2ot3rmp4d5u"
app.config.update(dict(
    SQLALCHEMY_DATABASE_URI=squalchemy_database_uri, #os.environ['DATABASE_URL'],
#    DATABASE=os.path.join(app.root_path, 'instadeck.db'),
    DEBUG=True,
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
db = SQLAlchemy(app)

app.config.from_envvar('INSTADECK_SETTINGS', silent=True)
# FIXME: what are this envvar? I'm not keeping anything in the environment.

def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def init_db():
    """Initializes the database."""
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()


# @app.cli.command('initdb')
def initdb_command():
    """Creates the database tables."""
    init_db()
    print('Initialized the database.')


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

@app.route('/')
def hello ():
    return render_template("welcome.html") # template, params

@app.route('/list_decks')
def list_decks():
    db = get_db()
    cur = db.execute('select slug, title, content from decks order by id desc')
    decks = cur.fetchall()
    return render_template('list_decks.html', decks=decks)

def slugify(content):
    return sha1(content).hexdigest()[:6]

@app.route('/add', methods=['POST'])
def add_deck():
    slug = slugify(request.form['content'])
    db = get_db()
    db.execute('insert into decks (slug, title, content) values (?, ?, ?)',
               [slug, request.form['title'], request.form['content']])
    db.commit()
    flash('New entry was successfully posted')
#    return redirect(url_for('list_decks'))
    return redirect('/'+slug)
@app.route ('/<slug>') # unsplash picture category
def display_deck(slug):
    ''' request a deck corresponding to a given slug, fill in deck template w/
    (slug), title, content; redirect somewhere appropriate'''
    db = get_db ()
    cur = db.execute ('select slug, title, content from decks where slug = ?', \
[slug])
    deck = cur.fetchone() #FIXME fetch, check return type
    if deck:
        deck = dict(deck)
        deck['pic'] = 'people'
        deck['slides'] = parse_deck_contents_into_slides(deck['content'])
        return render_template('single_deck.html', deck=deck)
    else:
        return render_template('404.html')

@app.route ('/<slug>/<pic>') # unsplash picture category
def display_deck_w_pic(slug, pic):
    ''' request a deck corresponding to a given slug, fill in deck template w/
    (slug), title, content; redirect somewhere appropriate'''
    db = get_db ()
    cur = db.execute ('select slug, title, content from decks where slug = ?', [slug])
    deck = cur.fetchone() #FIXME fetch, check return type
    if deck:
        deck = dict(deck)
        deck['pic'] = pic
        deck['slides'] = parse_deck_contents_into_slides(deck['content'])
        return render_template('single_deck.html', deck=deck)
    else:
        return render_template('404.html')

def parse_deck_contents_into_slides(deck_content):
    slides = deck_content.splitlines()
    # TODO: image and video processing code goes here
    non_empty_slides = [Slide(line) for line in slides if line] #remove empty lines (they are falsy).
    return non_empty_slides

def youtube_url_validation(url):
    youtube_regex = (
        r'(https?://)?(www\.)?'
        '(youtube|youtu|youtube-nocookie)\.(com|be)/'
        '(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')

    youtube_regex_match = re.match(youtube_regex, url)
    if youtube_regex_match:
        return youtube_regex_match.group(6)

    return youtube_regex_match

def extract_img_url(url):
    img_regex = (
        r'([a-z\-_0-9\/\:\.]*\.(jpg|jpeg|png|gif)$)')
    
    img_regex_match = re.match(img_regex, url)
    if img_regex_match:
        return img_regex_match.group(1)
    
    return img_regex_match

def vimeo_url_validation(url):
    vimeo_regex = (
        r'(?:https?\:\/\/)?(?:www\.)?(?:vimeo\.com\/)([0-9]+)')

    vimeo_regex_match = re.match(vimeo_regex, url)
    if vimeo_regex_match:
        return vimeo_regex_match.group(1) 

    return vimeo_regex_match


def emb(line):
    ''' return an html element with video or image or None '''
    youtube_url = youtube_url_validation(line) 
    vimeo_url = vimeo_url_validation(line)
    img_url = extract_img_url(line) #FIXME: return None
    if (youtube_url):
        return wrap_youtube_link(youtube_url)
    if (vimeo_url):
        return wrap_vimeo_link(vimeo_url)
    if (img_url):
        return wrap_img_link(img_url)
    return None

def wrap_img_link(img_url):
    return '<img src="' + img_url + '"/>'

def wrap_youtube_link(youtube_url):
    return '<iframe width="420" height="315" src="https://www.youtube.com/embed/'+ youtube_url  +'" frameborder="0" allowfullscreen></iframe>'
    
def wrap_vimeo_link(vimeo_id):
    return '<iframe src="https://player.vimeo.com/video/'+ vimeo_id + '" width="500" height="281" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen></iframe>'



