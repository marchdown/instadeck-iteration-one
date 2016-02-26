from urllib import urlopen
# used in instadeck-initialize-db.py and instadeck.py
from flask.ext.sqlalchemy import SQLAlchemy
from instadeck_accessory_methods import slugify, emb, request_a_new_picture_url_from_unsplash
db = SQLAlchemy()

class Deck(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True) # does postgres support autoincrement?
    slug =  db.Column(db.String(6))
    title = db.Column(db.String(400))
    slides = db.Column(db.String(8000)) #FIXME: think of an appropriate size
    
    def __init__(self, title, slides):
        self.title = title
        self.slides = slides
        self.slug = slugify(slides)
        self.pic = request_a_new_picture_url_from_unsplash(filter="")
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

def parse_deck_contents_into_slides(deck_content):
    slides = deck_content.splitlines()
    # TODO: image and video processing code goes here
    non_empty_slides = [Slide(line) for line in slides if line] #remove empty lines (they are falsy).
    return non_empty_slides
