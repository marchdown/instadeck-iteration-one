import os, re
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from instadeck_accessory_methods import slugify

#app = Flask(__name__)
app = Flask('instadeck')
db = SQLAlchemy(app)
#db = SQLAlchemy()

class Deck(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True) # does postgres support autoincrement?
    slug =  db.Column(db.String(6))
    title = db.Column(db.String(400))
    slides = db.Column(db.String(8000)) #FIXME: think of appropriate size
    def __init__(self, title, slides):
        self.title = title
        self.slides = slides
        self.slug = slugify(slides)
        
    def __repr__(self):
#        return '%r <> %r' % self.slug, self.title
        return '%r' % self.slug


# Load default config and override config from an environment variable
if ('DATABASE_URL' in os.environ):
     squalchemy_database_uri = os.environ['DATABASE_URL']
else:
    squalchemy_database_uri="postgres://drjhgnilfoimyr:Xfd9ThpoGIsrBfHL_ZpCDRz0h8@ec2-107-20-224-236.compute-1.amazonaws.com:5432/dbq42pinio51ba"

app.config.update(dict(
    SQLALCHEMY_DATABASE_URI=squalchemy_database_uri, #os.environ['DATABASE_URL'],
))

single_slide_deck = Deck("Here's a database for you", 'no slides, though')

copybook = Deck('The Gods of the Copybook Headings ',
                '''
AS I PASS through my incarnations in every age and race,
I make my proper prostrations to the Gods of the Market Place.
Peering through reverent fingers I watch them flourish and fall,
And the Gods of the Copybook Headings, I notice, outlast them all.

We were living in trees when they met us. They showed us each in turn
That Water would certainly wet us, as Fire would certainly burn:
But we found them lacking in Uplift, Vision and Breadth of Mind,
So we left them to teach the Gorillas while we followed the March of Mankind.

We moved as the Spirit listed. They never altered their pace,
Being neither cloud nor wind-borne like the Gods of the Market Place,
But they always caught up with our progress, and presently word would come
That a tribe had been wiped off its icefield, or the lights had gone out in Rome.

With the Hopes that our World is built on they were utterly out of touch,
They denied that the Moon was Stilton; they denied she was even Dutch;
They denied that Wishes were Horses; they denied that a Pig had Wings;
So we worshipped the Gods of the Market Who promised these beautiful things.

When the Cambrian measures were forming, They promised perpetual peace.
They swore, if we gave them our weapons, that the wars of the tribes would cease.
But when we disarmed They sold us and delivered us bound to our foe,
And the Gods of the Copybook Headings said: "Stick to the Devil you know." 

On the first Feminian Sandstones we were promised the Fuller Life
(Which started by loving our neighbour and ended by loving his wife)
Till our women had no more children and the men lost reason and faith,
And the Gods of the Copybook Headings said: "The Wages of Sin is Death." 

In the Carboniferous Epoch we were promised abundance for all, 
By robbing selected Peter to pay for collective Paul; 
But, though we had plenty of money, there was nothing our money could buy, 
And the Gods of the Copybook Headings said: "If you don't work you die." 

Then the Gods of the Market tumbled, and their smooth-tongued wizards withdrew
And the hearts of the meanest were humbled and began to believe it was true
That All is not Gold that Glitters, and Two and Two make Four
And the Gods of the Copybook Headings limped up to explain it once more.

As it will be in the future, it was at the birth of Man
There are only four things certain since Social Progress began. 
That the Dog returns to his Vomit and the Sow returns to her Mire, 
And the burnt Fool's bandaged finger goes wabbling back to the Fire;

And that after this is accomplished, and the brave new world begins
When all men are paid for existing and no man must pay for his sins, 
As surely as Water will wet us, as surely as Fire will burn, 
The Gods of the Copybook Headings with terror and slaughter return! 
''')


if __name__ == '__main__':
    db.create_all() # <-- generate relations
    print "create_all called"
    db.session.add(copybook)
    db.session.add(single_slide_deck)
    db.session.commit()

# def init_db():
#     """Initializes the database."""
#     db = get_db()
#     with app.open_resource('schema.sql', mode='r') as f:
#         db.cursor().executescript(f.read())
#     db.commit()


# # @app.cli.command('initdb')
# def initdb_command():
#     """Creates the database tables."""
#     init_db()
#     print('Initialized the database.')

