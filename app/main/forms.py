from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, SelectField
from wtforms.validators import ValidationError, DataRequired, Length, Regexp, Email
from flask_babel import _, lazy_gettext as _l
from app.models import User, Role


class EditProfileForm(FlaskForm):
    username = StringField(_l('用户名'), validators=[DataRequired(), Length(5,20), Regexp('^[a-zA-Z][a-zA-Z0-9_]{4,15}$', 0,
         '用户名只能字母开头，包含字母、数字、点以及下划线')])

    about_me = TextAreaField(_l('我的介绍'),
                             validators=[Length(min=0, max=140)])
    submit = SubmitField(_l('提交'))

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError(_('用户名重复，请更换'))

class EditProfileAdminForm(FlaskForm):
    """管理员资料编辑表单"""
    username = StringField('用户名', validators=[
        DataRequired(), Length(5, 20), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, '用户名只能是字母开头，包含字母、数字、点以及下划线的5-20位字符')])
    phonenumber = StringField(_l('用户手机号码'), validators=[DataRequired(),
        Regexp('^(13[0-9]|14[5|7]|15[0|1|2|3|5|6|7|8|9]|18[0|1|2|3|5|6|7|8|9])\d{8}$',
            0, '接受13,14,15,18开头的手机号注册')])
    email = StringField('用户邮箱', validators=[DataRequired(), Length(1,64), Email()])
    confirmed = BooleanField('用户是否激活账户')
    role = SelectField('用户角色', coerce=int)
    about_me = TextAreaField('用户的介绍')
    submit = SubmitField('提交')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name) for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self, email):
        if email.data != self.user.email and User.query.filter_by(email=email.data).first():
            raise ValidationError('邮箱已经被占用或发生错误。')

    def validate_username(self, username):
        if username.data != self.user.username and User.query.filter_by(username=username.data).first():
            raise ValidationError('用户名已经被占用或者发生错误。')
        


class EmptyForm(FlaskForm):
    submit = SubmitField('提交')


class PostForm(FlaskForm):
    post = TextAreaField(_l('发布信息'), validators=[DataRequired()])
    submit = SubmitField(_l('发布'))


class SearchForm(FlaskForm):
    q = StringField(_l('搜索'), validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        if 'formdata' not in kwargs:
            kwargs['formdata'] = request.args
        if 'csrf_enabled' not in kwargs:
            kwargs['csrf_enabled'] = False
        super(SearchForm, self).__init__(*args, **kwargs)


class MessageForm(FlaskForm):
    message = TextAreaField(_l('Message'), validators=[
        DataRequired(), Length(min=1, max=140)])
    submit = SubmitField(_l('Submit'))
