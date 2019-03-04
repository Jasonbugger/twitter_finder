from flask import render_template, url_for, redirect, Response, Flask, request, jsonify
from wtforms import StringField, SubmitField, RadioField, SelectField, Form
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap
import sys
from datetime import timedelta
from flask_mongoengine import MongoEngine
from LoadInDB import TUser
from LoadInDB import TweetInfo

sys.path.append(r'E:\twitter_finder')
app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['MONGODB_SETTINGS'] = {
    'db': 'tweet',
    'host': '127.0.0.1',
    'port': 27017
}
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1)

db = MongoEngine(app)
app.secret_key = 's12saf123f'
WTF_CSRF_ENABLED = False
WTF_CSRF_CHECK_DEFAULT = False


class SearchForm(Form):
    query = StringField(label='查询', validators=[DataRequired('请输入用户id')])
    type = SelectField('查询类型', 
                        [DataRequired()], 
                        default='id', 
                        choices=[('name', '按姓名'), 
                        ('id', '按id')], 
                        render_kw={})
    submit1 = SubmitField('查找')


class HashtagChoser(Form):
    Hashtag = SelectField('hashtag&attr', [DataRequired()])
    choices = [('emotion0', '积极'),
    ('emotion1', '消极'),
    ('emotion2', '愤怒'),
    ('emotion3', '期盼'),
    ('emotion4', '厌恶'),
    ('emotion5', '恐惧'),
    ('emotion6', '喜悦'),
    ('emotion7', '惊讶'),
    ('emotion8', '信任'),
    ('character0', '宜人性'), 
    ('character1', '认真性'), 
    ('character2', '外倾性'), 
    ('character3', '神经质'), 
    ('character4', '经验开放性'),
    ('gender0', '性别'),
    ("age0",'年龄：13-18'),
    ("age1",'年龄：19-22'),
    ("age2",'年龄：23-29'),
    ("age3",'年龄：30+')]
    attr = SelectField('属性', [DataRequired()],choices=choices,default='age1')
    submit2 = SubmitField('提交')


@app.route('/', methods=['GET', 'POST'])
def Main_Search(status=""):
    search_form = SearchForm(request.form)
    if search_form.validate():
        query = search_form.query.data
        return redirect(url_for('ShowUser', 
                                usertype=search_form.type.data, 
                                userinfo=query))
    return render_template('index.html', 
                            form=search_form, 
                            status=status)


@app.route('/tweet/<usertype>/<userinfo>', methods=['GET', 'POST'])
def ShowUser(usertype, userinfo):
    search_form = SearchForm()
    user = TUser.find(usertype, userinfo)
    # 转化为dict再转化为json格式，以便传参给js
    if search_form.validate():
        query = search_form.query.data
        return redirect(url_for('ShowUser', 
                        usertype=search_form.type.data, 
                        userinfo=query))
    if user:
        return render_template('user.html', 
                                user=user, 
                                form=search_form)
    else:
        return redirect(url_for('Main_Search', status="No such User"))

#        return "no user"


# 显示人地理位置分布
@app.route('/user/location/<hashtag>/<attr>',methods=['GET','POST'])
def show_user_location(hashtag='#all', attr='age1'):
    users = TUser()
    locations = users.find_loc_by_hashtag(hashtag, attr)
    search_form = SearchForm(request.form)
    hashtag_form = HashtagChoser(request.form)
    hashtag_form.Hashtag.choices = get_hashtags()
    if search_form.validate():
        query = search_form.query.data
        return redirect(url_for('ShowUser', usertype=search_form.type.data, userinfo=query))
    if hashtag_form.submit2.data and hashtag_form.validate():
        return redirect(url_for('show_user_location', 
                                hashtag=hashtag_form.Hashtag.data, 
                                attr=hashtag_form.attr.data))
    return render_template('user_hashtag_loc.html', 
                            form=search_form, 
                            hashtag=hashtag, 
                            hashtag_form=hashtag_form, 
                            data=locations)


# 获得所有hashtag
def get_hashtags():
    return [('#isis', '#isis'), ('#terrorism', '#terrorism'), ('#saudi', '#saudi'), ('all', 'all')]


@app.route('/tweet/<hashtag>', methods=["GET", "POST"])
def show_hashtag_location(hashtag='all'):
    locations = TweetInfo.find_loc_by_hashtag(hashtag)
    search_form = SearchForm(request.form)
    hashtag_form = HashtagChoser(request.form)
    hashtag_form.Hashtag.choices = get_hashtags()
    # print(search_form.submit1.data)
    # print(search_form.query.data)
    if search_form.validate():
        query = search_form.query.data
        return redirect(url_for('ShowUser', 
                                usertype=search_form.type.data, 
                                userinfo=query))
    if hashtag_form.submit2.data and hashtag_form.validate():
        return redirect(url_for('show_hashtag_location', 
                                hashtag=hashtag_form.Hashtag.data))
    return render_template('location.html', 
                            form=search_form, 
                            hashtag=hashtag, 
                            hashtag_form=hashtag_form, 
                            data=locations)


if __name__ == '__main__':
    app.debug = True
    app.run()
