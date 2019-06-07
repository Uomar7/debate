from flask import render_template,request,redirect,url_for,abort
from . import main
from app import socketio
from flask_login import login_required, current_user
from .forms import ContactForm,UpdateProfile
from ..models import User,Debate,Category,Chat
from .. import db


@main.route('/')
def index():
   chats = Chat.query.all()
   print(chats)
   return render_template('./create_discussion.html', chats = chats)

# @main.route('/live')
# def live():
#     messages = Chat.query.all()
#     print(messages)
#     return render_template('create_discussion.html', messages = messages)



@socketio.on('my event')
def handle_my_custom_event(json):
   chat = Chat(chat= str(json.get('msg')))
   print(chat,json)
   db.session.add(chat)
   db.session.commit()


   socketio.emit('my response', json)
   
@main.route('/contact us',methods=['POST','GET'])
def contact():
   form = ContactForm()
   if form.validate_on_submit():
       name =form.name.data
       email = form.email.data
       message = form.message.data
   return render_template('contact.html',contact_form=form)


@main.route('/user/<uname>',methods=['GET','POST'])
def profile(uname):
   user = User.query.filter_by(username = uname).first()
   debates = Debate.query.filter_by(user_id=current_user.id).all()
   return render_template("profile/profile.html", user = user,debates=debates)


@main.route('/user/<uname>/update/',methods = ['GET','POST'])
@login_required
def update_profile(uname):
   user = User.query.filter_by(username = uname).first()
   if user is None:
       abort(404)
   form = UpdateProfile()
   if form.validate_on_submit():
       user.bio = form.bio.data
       db.session.add(user)
       db.session.commit()
       return redirect(url_for('main.profile',uname=user.username))
   return render_template('profile/update.html',form =form,user=user)


@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
   user = User.query.filter_by(username = uname).first()
   if 'photo' in request.files:
       filename = photos.save(request.files['photo'])
       path = f'photos/{filename}'
       user.profile_pic_path = path
       db.session.commit()
   return redirect(url_for('main.profile',uname=uname))

