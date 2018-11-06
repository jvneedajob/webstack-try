#encoding: utf-8
'''
logo圖片引用:最酷的背包菜鳥log
主要架構引用:bootstrap.com

'''
from datetime import datetime as dt
from flask import Flask,render_template, request, url_for , redirect, session, g , flash
from model import User,Question,Answer
import config
from exts import db
#from decorators import login_required
from sqlalchemy import or_
from auth.auth import bp
from auth import auth
from form import LoginForm,RegistrationForm,EditProfileForm
from flask_login import  current_user , login_user ,logout_user , LoginManager,login_required
from werkzeug.urls import url_parse


app = Flask(__name__)
app.config.from_object(config)
app.register_blueprint(bp,url_prefix='/auth')
#app.register_blueprint(auth.bp)
login_manage = LoginManager(app)
@login_manage.user_loader
def load_user(id):
    return User.query.get(int(id))  #若放在model會產生循環衝突?
login_manage.login_view = 'login'
db.init_app(app)



@app.route('/')
def index():
    context = {
        'questions': Question.query.order_by('-create_time').all()
    }
    return render_template('index.html',**context)
@app.route('/login/',methods = ["GET","POST"])
def login():
    # if request.method == 'GET':
    #     return render_template('login.html')
    # else:     
    #     username = request.form.get('username')
    #     password = request.form.get('password')
    #     user = User.query.filter(User.username == username).first()

    #     if user and user.check_password(password):
    #         session['user_id'] = user.id
    #         #31天(默認)內cookie存留
    #         session.permanent = True
    #         return redirect(url_for('index'))
    #     else:
    #         flash(u'帳號或密碼輸入錯誤，請重新輸入!')
    #         return render_template('login.html')
    # if form.validate_on_submit():
    #     flash('Login requested for user {}, remember_me={}'.format(
    #     form.username.data, form.remember_me.data))
    #     return redirect('/index')
    #  return render_template('login.html', title='Sign In', form=form)
    #------------------------
    # print('以下是wtf表單創建的')
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():  #!!!!!加入wtf專用密鑰才能通過
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash(u'帳號、密碼有誤！')
            return render_template('login.html',form=form)
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
            return redirect(next_page)
    return render_template('login.html', form=form)
    
@app.route('/regist/',methods = ["GET","POST"])
def regist():
    # if request.method == 'GET':
    #     return render_template('regist.html')
    # else:
    #     username = request.form.get('username')
    #     email = request.form.get('email')
    #     password1 = request.form.get('password1')
    #     password2 = request.form.get('password2')
    #     if username and password1 and email:
    #     #確認帳號是否被使用
    #         user = User.query.filter(User.username == username).first()
    #         email_check = User.query.filter(User.email == email).first()
    #         if user:
    #             flash(u'該帳號已被註冊，請嘗試其他帳號')
    #             return render_template('regist.html')
    #         if email_check:
    #             flash(u'該信箱已被註冊，請嘗試其他信箱')
    #             return render_template('regist.html')
    #         else:
    #             #password確認
    #             if  password1 != password2:
    #                 flash(u'密碼不一致，請重新輸入密碼!')
    #                 return render_template('regist.html')
    #             else:
    #                 user = User(username=username,password=password1,email=email)
    #                 db.session.add(user)
    #                 db.session.commit()
    #                 return redirect(url_for('login')) 
    #     else:
    #         flash(u'帳號、密碼或信箱不得為空!')
    #         return render_template('regist.html')
    # print('以下是wtf表單創建的')
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit(): #沒()這個符號, form不會開機過濾
        print('1.1')##不通過的原因為{{ form.csrf_token }}
        username=form.username.data
        password=form.password1.data
        email=form.email.data
        if username and password and email:
            user = User(username=username,password=password,email=email)
            db.session.add(user)
            db.session.commit()
            flash(u'註冊成功')
            return redirect(url_for('login'))
    return render_template('regist.html',form=form)

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': '測試#1'},
        {'author': user, 'body': '測試#2'}
    ]
    return render_template('user.html', user=user, posts=posts)

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        if form.username.data and form.about_me.data:
            current_user.username = form.username.data
            current_user.about_me = form.about_me.data
            db.session.commit()
            flash(u'更改完成')
            return redirect(url_for('edit_profile'))
        elif request.method == 'GET':
            form.username.data = current_user.username
            form.about_me.data = current_user.about_me
    return render_template('edit_profile.html',form=form)

@app.route('/question/',methods = ["GET","POST"])
@login_required
def question():
    if request.method =='GET':
        return render_template('question.html')
    else:
        title = request.form.get('title')
        content = request.form.get('content')
        question = Question(title=title,content=content)
        question.author = g.user
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('index'))

@app.route('/detail/<question_id>',methods = ["GET","POST"])
def detail(question_id):
    quesiton_model = Question.query.filter(Question.id == question_id).first()
    return render_template('detail.html',question=quesiton_model)

@app.route('/add_answer/',methods = ["POST"])
@login_required
def add_answer():
    content = request.form.get('answer_content')
    question_id = request.form.get('question_id')
    create_time = Answer.query.order_by('-create_time').first()
    answer = Answer(content=content)
    answer.author = g.user
    question = Question.query.filter(Question.id == question_id).first()
    answer.question = question
    db.session.add(answer)
    db.session.commit()
    

    return redirect(url_for('detail',question_id=question_id))
@app.route('/logout/',methods = ["GET","POST"])
def logout():
    # session.clear()
    # return redirect(url_for('login'))
#----------------
   logout_user()
   return redirect(url_for('index'))


@app.context_processor
def my_context_processor():
    if hasattr(g,'user'):
            return {'user':g.user}
    else:
        return {}

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = dt.utcnow()
        db.session.commit()
@app.before_request  ##一個def對一個@before-request
def my_before_request():
#     #user_id = session['user_id']
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            g.user = user

@app.route('/search/',methods = ["GET","POST"])
def search():
    q =request.args.get('q')
    questions = Question.query.filter(or_(Question.title.contains(q),Question.content.contains(q))).order_by('-create_time')
    
    return render_template('index.html',questions=questions)


if __name__ == '__main__':
    app.run(host = '0.0.0.0',
        port = 71  )
    # app.run(host = '127.0.0.1 auth.freshfly.dev.com',
    #     port = 71  )
    