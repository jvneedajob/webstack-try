#encoding: utf-8
'''
logo圖片引用:最酷的背包菜鳥log
主要架構引用:bootstrap.com

'''
from flask import Flask,render_template, request, url_for , redirect, session, g
import config
from model import User, Question,Answer
from exts import db
from decorators import login_required
from sqlalchemy import or_

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)

@app.route('/')
def index():
    context = {
        'questions': Question.query.order_by('-create_time').all()
    }
    return render_template('index.html',**context)
@app.route('/login/',methods = ["GET","POST"])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:     
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter(User.username == username).first()

        if user and user.check_password(password):
            session['user_id'] = user.id
            #31天(默認)內cookie存留
            session.permanent = True
            return redirect(url_for('index'))
        else:
            return u'帳號或密碼輸入錯誤，請重新輸入!'

@app.route('/regist/',methods = ["GET","POST"])
def regist():
    if request.method == 'GET':
        return render_template('regist.html')
    else:
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        if username and password1:
        #確認帳號是否被使用
            user = User.query.filter(User.username == username).first()
            if user:
                return u'該帳號已被註冊，請嘗試其他帳號'
            else:
                #password確認
                if  password1 != password2:
                    return u'密碼不一致，請重新輸入密碼'
                else:
                    user = User(username=username,password=password1)
                    db.session.add(user)
                    db.session.commit()
                    return redirect(url_for('login')) 
        else:
            return u'帳號或密碼不得為空!'   

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
    
    return render_template('detail.html',question=quesiton_model )

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
    session.clear()
    return redirect(url_for('login'))

@app.context_processor
def my_context_processor():
    if hasattr(g,'user'):
            return {'user':g.user}
    else:
        return {}

@app.before_request
def my_before_request():
    #user_id = session['user_id']
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
    app.run(host='0.0.0.0',port=71)