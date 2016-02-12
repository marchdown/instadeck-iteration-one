# -*- coding: utf-8 -*-
"""
    Instadeck app
    ~~~~~~
"""

import os
from hashlib import sha1 as sha1
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash

# FIXME: what are g, abort, flash

# create our little application :)
app = Flask(__name__)

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'instadeck.db'),
    DEBUG=True,
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
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


@app.command('initdb')
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

@app.route('/add', methods=['POST'])
def add_deck():
    slug = sha1(request.form['content']).hexdigest()[:6] #FIXME concat title
    db = get_db()
    db.execute('insert into decks (slug, title, content) values (?, ?, ?)',
               [slug, request.form['title'], request.form['content']])
    db.commit()
    flash('New entry was successfully posted')
#    return redirect(url_for('list_decks'))
    return redirect('/'+slug)

@app.route ('/<slug>')
def display_deck(slug):
    ''' request a deck corresponding to a given slug, fill in deck template w/
    (slug), title, content; redirect somewhere appropriate'''
    db = get_db ()
    cur = db.execute ('select slug, title, content from decks where slug = ?', [slug])
    deck = cur.fetchone() #FIXME fetch, check return type
    if deck:
        deck = dict(deck)
        deck['slides'] = parse_deck_contents_into_slides(deck['content'])
        return render_template('single_deck.html', deck=deck)
    else:
        return render_template('404.html')

def parse_deck_contents_into_slides(deck_content):
    slides = deck_content.splitlines()
    # TODO: image and video processing code goes here
    non_empty_slides = [slide for slide in slides if slide] #remove empty lines (they are falsy).
    return non_empty_slides
