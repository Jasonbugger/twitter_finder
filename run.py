from flask import render_template, url_for, redirect, Response, Flask, request, jsonify
from wtforms import StringField, SubmitField, RadioField, SelectField, Form
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap
import json
import sys
from datetime import timedelta
from flask_mongoengine import MongoEngine
import mongoengine
import math
from LoadInDB import TUser
from LoadInDB import Tweet_Info

sys.path.append(r'E:\tweet')
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
    query = StringField(label='查询', validators = [DataRequired('请输入用户id')])
    type = SelectField('查询类型', [DataRequired()], default='id', choices=[('name', '按姓名'), ('id', '按id')], render_kw={})
    submit1 = SubmitField('查找')

class HashtagChoser(Form):
    Hashtag = SelectField('hashtag',[DataRequired()])
    submit2 = SubmitField('change')

@app.route('/', methods=['GET', 'POST'])
def Main_Search(status=""):
    search_form = SearchForm(request.form)
    query = ''
    if search_form.validate():
        query = search_form.query.data
        return redirect(url_for('ShowUser', usertype=search_form.type.data, userinfo=query))
    return render_template('index.html', form=search_form, status=status)


@app.route('/tweet/<usertype>/<userinfo>', methods=['GET', 'POST'])
def ShowUser(usertype, userinfo):
    search_form = SearchForm()
    user, user_list = TUser.find(usertype, userinfo)
    # 转化为dict再转化为json格式，以便传参给js
    if search_form.validate():
        query = search_form.query.data
        return redirect(url_for('ShowUser', usertype=search_form.type.data, userinfo=query))
    print(user)
    if user:
        return render_template('user.html', user=user, user_list=user_list, form=search_form)
    else:
        return redirect(url_for('Main_Search', status="No such User"))

#        return "no user"

# 统计某类hashtag中的人的相关属性的分布
@app.route('/tweet/hashtag/<hashtag>')
def show_hashTag(hashtag):
    
    return

# 获取所有的用户地理位置列表
def get_locations():
    locations = []
    for user in TUser.itter():
        locations.append(user.location)
    return locations

# 显示人地理位置分布
@app.route('/tweet/location')
def show_location():
    # 将地理位置取出传给模板
    locations = get_locations()
    return render_template('location.html', location_list = locations)


#获得所有hashtag
def get_hashtags():
    return [('isis','isis'),('#terrorism','#terrorism'),('#saudi','#saudi')]

@app.route('/tweet/<hashtag>', methods=["GET","POST"])
def show_hashtag_lcation(hashtag = 'all'):
    tweet_db = Tweet_Info()
    locations = tweet_db.find_loc_by_hashtag(hashtag)
    hashtag_form = HashtagChoser()
    search_form = SearchForm()
    
    hashtag_form.Hashtag.choices = get_hashtags()
    if search_form.validate():
        query = search_form.query.data
        return redirect(url_for('ShowUser', usertype=search_form.type.data, userinfo=query))
    if hashtag_form.validate():
        hashtag = hashtag_form.Hashtag.data
        return render_template('location.html',form=search_form,hashtag=hashtag, hashtag_form= hashtag_form,data=locations)
    return render_template('location.html',form=search_form,hashtag=hashtag, hashtag_form= hashtag_form,data=locations)

if __name__ == '__main__':
    app.debug = True
    app.run()
