#!flask/bin/python
import codecs
import glob
import random
from app import db, models

# first add the administrator
admin = models.User(username='admin', firstname='admin', surname='admin',
                    password='admin', email='ketting.vertelling@gmail.com')
db.session.add(admin)

# next add all participants
for user in open("users.txt"):
    username, name, email, password = user.strip().split(',')
    firstname, surname = name.split(' ', 1)
    user = models.User(username=username, firstname=firstname, surname=surname,
                       password=password, email=email)
    db.session.add(user)
db.session.commit()

# add all stories to the database (admin is author)
admin = models.User.query.filter_by(username='admin').first()
for fname in glob.glob("stories/*.txt"):
    storyid = fname.split('/')[-1]
    with codecs.open(fname, encoding='utf-8') as f:
        story = f.read()
        story = models.Story(storyname=storyid, story=story, storyteller=admin)

# finally add all chains to the transition table
users = [user for user in models.User.query.all() if user.username != 'admin']
admin = models.User.query.filter_by(username='admin').first()
# get all story IDs
stories = admin.stories.all()
# make random chains and populate the database
for story in stories:
    random.shuffle(users)
    transition = models.Transition(
        storyname=story.storyname, source_id=admin.id, target_id=users[0].id, active=1)
    db.session.add(transition)
    for i in range(len(users)-1):
        source, target = users[i], users[i+1]
        transition = models.Transition(
            storyname=story.storyname, source_id=source.id, target_id=target.id, active=0)
        db.session.add(transition)
db.session.commit()

