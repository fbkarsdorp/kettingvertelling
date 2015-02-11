from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), index=True, unique=True)
    firstname = db.Column(db.String(64), index=True, unique=False)
    surname = db.Column(db.String(64), index=True, unique=False)
    password = db.Column(db.String(64), index=True, unique=False)
    email = db.Column(db.String(120), index=True, unique=True)
    stories = db.relationship('Story', backref='storyteller', lazy='dynamic')

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<User(%r)>' % self.username

class Story(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    storyname = db.Column(db.String(64), index=True, unique=False)
    story = db.Column(db.String())
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Story(%r)>' % self.story

class Transition(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    storyname = db.Column(db.String(64), index=True, unique=False)
    source_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    target_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    active = db.Column(db.Integer)

    def __repr__(self):
        return '<Transition(%r: %r, %r, %r)>' % (
            self.storyname, self.source_id, self.target_id, self.active)

