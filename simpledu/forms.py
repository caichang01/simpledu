from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, IntegerField
from wtforms.validators import Length, Email, EqualTo, DataRequired, URL, NumberRange
from simpledu.models import db, User, Course, Live
from wtforms import ValidationError

class RegisterForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(), Length(3, 24, message='用户名的长度为3-24个字符之间')])
    email = StringField('Email', validators=[DataRequired(), Email(message='请输入合法的email地址')])
    password = PasswordField('密码', validators=[DataRequired(), Length(6, 24, message='密码的长度为6-24个字符之间')])
    repeat_password = PasswordField('重复密码', validators=[DataRequired(), EqualTo('password', message='请输入同样的密码')])
    submit = SubmitField('提交')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已被注册')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已被注册')

    def create_user(self):
        user = User()
        user.username = self.username.data
        user.email = self.email.data
        user.password = self.password.data
        db.session.add(user)
        db.session.commit()
        return user

    def update_user(self, user):
        self.populate_obj(user)
        db.session.add(user)
        db.session.commit()
        return user


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('密码', validators=[DataRequired(), Length(6, 24)])
    remember_me = BooleanField('记住我')

    def validate_email(self, field):
        if field.data and not User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱未注册')

    def validate_password(self, field):
        user = User.query.filter_by(email=self.email.data).first()
        if user and not user.check_password(field.data):
            raise ValidationError('密码错误')
    submit = SubmitField('提交')


class CourseForm(FlaskForm):
    name = StringField('课程名称', validators=[DataRequired(), Length(5, 32, message='课程名称的长度为5-32个字符之间')])
    description = TextAreaField('课程描述', validators=[DataRequired(), Length(20, 256, message='课程描述的长度为20-256个字符之间')])
    image_url = StringField('封面图链接', validators=[DataRequired(), URL(message='请输入合法的url地址')])
    author_id = IntegerField('作者ID', validators=[DataRequired(), NumberRange(min=1, message='无效的用户ID')])
    submit = SubmitField('提交')

    def validate_author_id(self, field):
        if not User.query.get(self.author_id.data):
            raise ValidationError('指定作者不存在')

    def create_course(self):
        course = Course()
        self.populate_obj(course)
        db.session.add(course)
        db.session.commit()
        return course

    def update_course(self, course):
        self.populate_obj(course)
        db.session.add(course)
        db.session.commit()
        return course


class LiveForm(FlaskForm):
    name = StringField('直播名称', validators=[DataRequired(), Length(2, 32, message='直播名称的长度为2-32个字符之间')])
    description = TextAreaField('直播描述', validators=[DataRequired(), Length(5, 256, message='直播描述的长度为5-256个字符之间')])
    image_url = StringField('封面图链接', validators=[DataRequired(), URL('请输入合法的url地址')])
    live_url = StringField('直播拉流链接', validators=[DataRequired(), URL('请输入合法的url地址')])
    broadcaster_id = IntegerField('主播ID', validators=[DataRequired(), NumberRange(min=1, message='无效的用户ID')])
    submit = SubmitField('提交')

    def validate_broadcaster_id(self, field):
        if not User.query.get(self.broadcaster_id.data):
            raise ValidationError('指定主播不存在')

    def create_live(self):
        live = Live()
        self.populate_obj(live)
        db.session.add(live)
        db.session.commit()
        return live

    def update_live(self, live):
        self.populate_obj(live)
        db.session.add(live)
        db.session.commit()
        return live


class MessageForm(FlaskForm):
    text = StringField('消息内容', validators=[DataRequired(), Length(1, 256, message='消息内容的长度为1-256个字符之间')])
    submit = SubmitField('提交')
