# -*- coding: utf-8 -*-
"""
    Instadeck app
    ~~~~~~
"""
import os
from flask import Flask, request, session, redirect, url_for, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from instadeck_classes import Deck, Slide, parse_deck_contents_into_slides
from instadeck_accessory_methods import slugify

# create our little application and a corresponding database connection
app = Flask(__name__)
db = SQLAlchemy(app)

# Load default config and override config from an environment variable
if ('DATABASE_URL' in os.environ):
    squalchemy_database_uri = os.environ['DATABASE_URL']
else:
#    raise Exception("Can't find database URI in os.environ")
    squalchemy_database_uri="postgres://uquxyjlmmjtbff:aie93RAT7ZN2aAjYgyx5C-L2A1@ec2-107-20-224-236.compute-1.amazonaws.com:5432/d3v2ot3rmp4d5u"
# NB: keeping access credentials in a public repo is never a good idea

# Leftovers from default flask app configuration. Might be useful.
app.config.update(dict(
    SQLALCHEMY_DATABASE_URI=squalchemy_database_uri, #os.environ['DATABASE_URL'],
#    DATABASE=os.path.join(app.root_path, 'instadeck.db'),
    DEBUG=True,
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))

app.config.from_envvar('INSTADECK_SETTINGS', silent=True)
# FIXME: what is this envvar? I'm not keeping anything in the environment. I should though.


@app.route('/')
def hello ():
    return render_template("welcome.html") # template, params

@app.route('/list_decks')
def list_decks():
    cur = db.engine.execute('select slug, title, slides from decks order by id desc')
    decks = cur.fetchall()
    return render_template('list_decks.html', decks=decks)


@app.route('/add', methods=['POST'])
def add_deck():
    slug = slugify(request.form['content'])
#    db.engine.execute('insert into decks (slug, title, slides) values (?, ?, ?)',
#               [slug, request.form['title'], request.form['content']])
    db.session.add(Deck(request.form['title'],request.form['content']))
    db.session.commit()
#    return redirect(url_for('list_decks'))
    return redirect('/'+slug)

@app.route ('/<slug>') # unsplash picture category
def display_deck(slug):
    ''' request a deck corresponding to a given slug, fill in deck template w/
    (slug), title, content; redirect somewhere appropriate'''
 #   cur = db.engine.execute ('select slug, title, slides from decks where slug = ?', [slug])
 #   deck = cur.fetchone() #FIXME fetch, check return type

 # slug_query = db.aliased(Deck, slug=slug)
 #    deck_query = db.session.query(Deck, Deck.slug, slug_query)
 #    deck = deck_query.get(1)

    deck = Deck.query.filter_by(slug=slug).first()
    print "#### deck returned: ", deck.slides, type(deck)

    # if deck:
    #     deck = dict(deck)
    #     deck['pic'] = 'people'
    #     deck['slides'] = parse_deck_contents_into_slides(deck['content']) # content -> slides
    #     return render_template('single_deck.html', deck=deck)
    if deck:
#        deck.pic = 'people'
        deck.slides =  parse_deck_contents_into_slides(deck.slides) # content -> slides
        return render_template('single_deck.html', deck=deck)
    else:
        return render_template('404.html')

@app.route ('/<slug>/<pic>') # unsplash picture category
def display_deck_w_pic(slug, pic):
    ''' request a deck corresponding to a given slug, fill in deck template w/
    (slug), title, content; redirect somewhere appropriate'''
    cur = db.engine.execute ('select slug, title, content from decks where slug = ?', [slug])
    deck = cur.fetchone() #FIXME fetch, check return type
    if deck:
        deck = dict(deck)
        deck.pic = pic
        deck.slides = parse_deck_contents_into_slides(deck.slides)
        return render_template('single_deck.html', deck=deck)
    else:
        return render_template('404.html')
