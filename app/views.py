import datetime
import flask
from flask.ext.login import login_user, current_user, login_required
from app import app, lm, db
from forms import LoginForm, StoryForm
from models import User, Story, Transition
from emails import story_notification

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.before_request
def before_request():
    flask.g.user = current_user

@app.route('/login', methods=['GET', 'POST'])
def login():
    #if flask.g.user is not None and flask.g.user.is_authenticated():
    #    return flask.redirect(flask.url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():
        if form.validate_login():
            flask.session['remember_me'] = form.remember_me.data
            login_user(form.get_user(), remember=form.remember_me.data)
            return flask.redirect(flask.url_for("index"))
    return flask.render_template('login.html', title='Sign In', form=form)

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    user = flask.g.user
    # find out whether there is an active story for this user
    transition = Transition.query.filter_by(target_id=user.id, active=1).first()
    if transition is None:
        story = None
    else:
        story = Story.query.filter_by(user_id=transition.source_id, storyname=transition.storyname).first()
    return flask.render_template('index.html', user=user, story=story)

def deactivate_transition(story, user):
    transition = Transition.query.filter_by(storyname=story.storyname, target_id=int(user.id)).first()
    transition.active = 0
    db.session.commit()

def activate_transition(story, user):
    transition = Transition.query.filter_by(storyname=story.storyname, source_id=int(user.id)).first()
    if transition is not None:
        transition.active = 1
        db.session.commit()
        return transition.target_id

@app.route('/thanks')
@login_required
def thanks():
    n_stories = len(flask.g.user.stories.all())
    lastone = True if n_stories == 5 else False
    more_to_go = Transition.query.filter_by(target_id=flask.g.user.id, active=1).all()
    if more_to_go:
        return flask.redirect(flask.url_for("index"))
    return flask.render_template("thanks.html", lastone=lastone)

@app.route('/retell/<storyname>', methods=['GET', 'POST'])
@login_required
def retell(storyname):
    user = flask.g.user
    story = Transition.query.filter_by(target_id=user.id, storyname=storyname, active=1).first()
    if story is None:
        flask.flash('Story (%s) already read or not found.' % storyname)
        return flask.redirect(flask.url_for("thanks"))
    form = StoryForm()
    if form.validate_on_submit() and form.validate_story():
        # add new story to database
        # make a new story containing the storyname, the text, time and current user
        story = Story(storyname=story.storyname, story=form.text.data, 
                      timestamp=datetime.datetime.utcnow(),
                      storyteller=user)
        db.session.add(story)
        db.session.commit()
        # deactivate the active transition with current user as target
        deactivate_transition(story, user)
        # next activate the next transition where current user is source
        target_id = activate_transition(story, user)
        if target_id is not None:
            new_user = User.query.get(int(target_id))
            # commit all changes
            db.session.commit()
            # send mail to next in chain
            story_notification(new_user)
        return flask.redirect(flask.url_for("thanks"))
    return flask.render_template("retell.html", form=form)

@app.errorhandler(404)
def not_found_error(error):
    return flask.render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return flask.render_template('500.html'), 500