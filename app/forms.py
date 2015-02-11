from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Required, ValidationError
from models import User

class LoginForm(Form):
    username = StringField('username', validators=[Required()])
    password = PasswordField('password', validators=[Required()])
    remember_me = BooleanField('remember_me', default=False)

    def validate_login(self):
        user = self.get_user()
        if user is None:
            self.username.errors.append('Jij bestaat niet.')
            return False
        if user.password != self.password.data:
            self.password.errors.append('Verkeerd wachtwoord.')
            return False
        return True

    def get_user(self):
        return User.query.filter_by(username=self.username.data).first()


class StoryForm(Form):
    text = TextAreaField("story", validators=[DataRequired()])

    def validate_story(self):
        if not self.text.data.strip():
            raise ValidationError("Je hebt geen tekst ingevoerd!")
        return True
