from flask import Flask
from . import main
from flask_login import login_required,current_user
from flask import render_template, redirect, url_for,flash,request
import datetime
from ..models import Pitch, Comment,Subscriber,Post,User
from .forms import PitchForm , CommentForm,SubscribeForm
from .. import db

app = Flask(__name__)


@main.route("/")
def index():
   '''
   title = "Bensam blog"
   '''
  
   title = 'Bensam blog'
#    pitch=Pitch.query.order_by(Pitch.id.desc()).all()

   return render_template('index.html', title= title)

@main.route('/pitch/new', methods=['GET','POST'])
@login_required
def new_pitch():
    form = PitchForm()

    if form.validate_on_submit():

        title=form.title.data
        content=form.content.data
        category=form.category.data
        pitch = Pitch(title=title, content=content,category=category)
        db.session.add(pitch)
        db.session.commit()

        flash('Your was a success!', 'success')
        return redirect(url_for('main.index', id=pitch.id))

    return render_template('pitches.html', title='New Post', pitch_form=form, post ='New Post') 


@main.route("/create-comment/<post_id>", methods=['POST'])
@login_required
def create_comment(post_id):
    text = request.form.get('text')
    if not text:
        flash('Comment cannot be empty.', category='error')
    else:
        post = Post.query.filter_by(id=post_id)
        if post:
            comment = Comment(
                text=text, author=current_user.id, post_id=post_id)
            db.session.add(comment)
            db.session.commit()
        else:
            flash('Post does not exist.', category='error')
    return redirect(url_for('main.home'))

@main.route('/subscription',methods=['GET','POST'])
def subscription():
    subscription_form = SubscribeForm()

    if subscription_form.validate_on_submit():
        new_subscriber = Subscriber(subscriber_name=subscription_form.subscriber_name.data,subscriber_email=subscription_form.subscriber_email.data)

        db.session.add(new_subscriber)
        db.session.commit()

        return redirect(url_for('main.index'))    

    return render_template('subscription.html',subscription_form = subscription_form)     


@main.route('/comment/new/<int:id>', methods=['GET','POST'])
@login_required
def new_comment(id):
    form = CommentForm()

    if form.validate_on_submit():
        
        comment_content = form.comment.data
        

        comment = Comment(comment_content= comment_content,pitch_id=id)

        db.session.add(comment)
        db.session.commit()
        
    comment = Comment.query.filter_by(pitch_id=id).all()
  


    return render_template('coments.html', title='New Post', comment=comment,comment_form=form, post ='New Post')