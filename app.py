"""Flask app for Cupcakes"""
from flask import Flask, render_template, redirect, request, jsonify, flash, session
from models import User, db, connect_db, Feedback
from flask_debugtoolbar import DebugToolbarExtension
from forms import AddUserForm, UserLoginForm, AddFeedbackForm, DeleteForm
# from forms import AddPetForm, EditPetForm
# import requests
from sqlalchemy.exc import IntegrityError



app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///feedback'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config['SECRET_KEY'] = "secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()



@app.route('/')
def homepage():
    return redirect('/register')

@app.route('/register', methods=['GET', 'POST'])
def show_registration_form():
    # create new user

    form = AddUserForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        new_user = User.register(username=username, password=password, email=email, first_name=first_name, last_name=last_name)

        db.session.add(new_user)
        db.session.commit()

        session['username']=username

        flash('New user added!')
        
        return redirect(f'/users/{username}')
    else:
        return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def show_login_form():

    if 'username' in session:
            session['username']=user.username
            username =user.username
            return redirect(f'/users/{username}')

    form = UserLoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username,password)

        if user:
            session['username']=user.username
            username =user.username
            return redirect(f'/users/{username}')
        else:
            form.username.errors = ['Bad name/password']

    return render_template('login.html',form=form)

@app.route('/users/<username>')
def display_secret(username):

    if 'username' not in session or session['username'] != username:
        flash('Must be logged in to view')
        return redirect('/login')

    
    user = User.query.filter_by(username=username).first()

    posts = Feedback.query.filter_by(username=username).all()

    form = DeleteForm()

    return render_template('user.html',user=user,posts=posts, form=form)
    
        

@app.route('/logout')
def logout_user():
    session.pop('username', None)
    return redirect('/')

@app.route('/users/<username>/feedback/add', methods=['GET','POST'])
def add_feedback(username):

    if not session['username']==username or "username" not in session:
        flash('Must be logged in to view user feedback!')
        return redirect('/login')

    form = AddFeedbackForm()
    user = User.query.filter_by(username=username).first()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        new_feedback = Feedback(title=title,content=content,username=username)

        db.session.add(new_feedback)
        db.session.commit()

        return redirect(f'/users/{username}')

    
    return render_template('feedback.html',user=user,form=form)

@app.route('/feedback/<int:feedback_id>/delete', methods=['POST'])
def delete_feedback(feedback_id):
    post = Feedback.query.get_or_404(feedback_id)

    username = post.username

    # session['username'] == username?

    if 'username' not in session or username != session['username']:
        flash('Must be logged in to delete')
        return redirect('/login')

    form = DeleteForm()
    
    if form.validate_on_submit():
        db.session.delete(post)
        db.session.commit()

    return redirect(f'/users/{username}')

@app.route('/users/<username>/delete', methods = ['POST'])
def delete_user(username):

    user = User.query.filter_by(username=username).first()

    if 'username' in session and session['username']==username:
        session.pop('username')

        db.session.delete(user)
        db.session.commit()
    else:
        flash('Must be logged in to delete user!')

    return redirect('/')

@app.route('/feedback/<int:feedback_id>/update',methods=['GET','POST'])
def edit_feedback(feedback_id):

    post=Feedback.query.get_or_404(feedback_id)
    username = post.username

    if not session['username']==username or "username" not in session:
        flash('Must be logged in to edit user feedback!')
        return redirect('/login')

    form=AddFeedbackForm(obj=post)

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        post.title = title
        post.content = content

        db.session.add(post)    
        db.session.commit()

        return redirect(f'/users/{username}')

    return render_template('editFeedback.html',form=form,post=post)


