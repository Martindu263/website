from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, RadioField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length, Regexp
from flask_babel import _, lazy_gettext as _l
from app.models import User


class LoginForm(FlaskForm):
    phonenumber = StringField(_l('请输入手机号'), validators=[DataRequired()])
    password = PasswordField(_l('请输入密码'), validators=[DataRequired()])
    remember_me = BooleanField(_l('记住本次登录(请勿在公共设备勾选)'))
    submit = SubmitField(_l('登录'))


class RegistrationForm(FlaskForm):
    username = StringField(_l('用户名'), validators=[
        DataRequired(), Length(3,20), Regexp('^[a-zA-Z][a-zA-Z0-9_]{4,15}$', 0,
         '用户名只能字母开头，包含字母、数字、点以及下划线')])
    #用户名是4-16位
    phonenumber = StringField(_l('本人手机号码'), validators=[DataRequired(),
        Regexp('^(13[0-9]|14[5|7]|15[0|1|2|3|5|6|7|8|9]|18[0|1|2|3|5|6|7|8|9])\d{8}$',
            0, '接受13,14,15,18开头的手机号注册')])
    email = StringField(_l('Email'), validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField(_l('密码'), validators=[DataRequired(),
        Regexp('^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,20}$', 0, '密码必须是包含大小写字母和数字的组合，不能使用特殊字符，长度小于20个字符')])
    password2 = PasswordField(_l('再次输入密码'), validators=[DataRequired(), EqualTo('password', message='两次密码必须一致')])
    isteacher = RadioField(_l('是否是老师'), choices=[('t', '教师'), ('s','学生或家长')], validators=[DataRequired()])
    submit = SubmitField(_l('提交注册'))

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError(_('用户名重复了，请更换一个用户名。'))

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError(_('邮箱重复了，请更换邮箱'))

    def validate_phonenumber(self, phonenumber):
        user = User.query.filter_by(phonenumber=phonenumber.data).first()
        if user is not None:
            raise ValidationError(_('该手机号码已注册，请更换手机号码'))


class ResetPasswordRequestForm(FlaskForm):
    email = StringField(_l('Email'), validators=[DataRequired(), Email()])
    submit = SubmitField(_l('Request Password Reset'))


class ResetPasswordForm(FlaskForm):
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    password2 = PasswordField(
        _l('Repeat Password'), validators=[DataRequired(),
                                           EqualTo('password')])
    submit = SubmitField(_l('Request Password Reset'))
