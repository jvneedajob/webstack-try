from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired,length,EqualTo,Email, ValidationError,Length
from model import User


class LoginForm(FlaskForm):
    username = StringField(u'帳 號', validators=[DataRequired(),length(min=5,max=15)])
    password = PasswordField(u'密 碼', validators=[DataRequired(),length(min=5,max=15)])
    remember_me = BooleanField(u'記住我')
    submit = SubmitField(u'登入')

class RegistrationForm(FlaskForm):
    username = StringField(u'帳 號', validators=[DataRequired(),length(min=5,max=15)])
    email = StringField(u'信 箱', validators=[DataRequired(),Email()])
    password1 = PasswordField(u'密 碼',validators=[DataRequired(),length(min=5,max=15)])
    password2 = PasswordField(u'確認密碼',validators=[DataRequired(),EqualTo('password1')])
    submit = SubmitField(u'創建')

    def validate_username(self,username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError(u'帳號已存在，請選用其他帳號!')
    def validate_email(self,email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError(u'郵件信箱已經存在，請改用其他!')

class EditProfileForm(FlaskForm):
    username = StringField(u'使用者', validators=[DataRequired()])
    about_me = TextAreaField(u'關於我', validators=[Length(min=0, max=140)])
    submit = SubmitField(u'提交')