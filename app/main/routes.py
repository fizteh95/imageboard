# from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, session
from flask_login import login_user, logout_user, current_user, login_required
# from werkzeug.urls import url_parse
# from app import app, db
# from app.forms import LoginForm, RegistrationForm, EditProfileForm, PostForm



from flask import render_template, current_app
from app import db
from app.models import Board, Post, User#, Imagestore
from app.main.forms import PostForm, ThreadForm, LoginForm, PostDelForm, BoardAddForm
import os
from PIL import Image
import re
import datetime
from app.main import bp
import random
import string
import requests
import base64
from io import BytesIO

 
# @app.before_request
# def before_request():
#     if current_user.is_authenticated:
#         current_user.last_seen = datetime.utcnow()
#         db.session.commit()


# @app.route('/', methods=['GET', 'POST'])
# @app.route('/index', methods=['GET', 'POST'])
# @login_required
# def index():
#     form = PostForm()
#     if form.validate_on_submit():
#         post = Post(body=form.post.data, author=current_user)
#         db.session.add(post)
#         db.session.commit()
#         flash('Your post is now live!')
#         return redirect(url_for('index'))
#     page = request.args.get('page', 1, type=int)
#     posts = current_user.followed_posts().paginate(
#         page, app.config['POSTS_PER_PAGE'], False)
#     next_url = url_for('index', page=posts.next_num) \
#         if posts.has_next else None
#     prev_url = url_for('index', page=posts.prev_num) \
#         if posts.has_prev else None
#     return render_template('index.html', title='Home', form=form,
#                            posts=posts.items, next_url=next_url,
#                            prev_url=prev_url)


# @app.route('/explore')
# @login_required
# def explore():
#     page = request.args.get('page', 1, type=int)
#     posts = Post.query.order_by(Post.timestamp.desc()).paginate(
#         page, app.config['POSTS_PER_PAGE'], False)
#     next_url = url_for('explore', page=posts.next_num) \
#         if posts.has_next else None
#     prev_url = url_for('explore', page=posts.prev_num) \
#         if posts.has_prev else None
#     return render_template('index.html', title='Explore', posts=posts.items,
#                            next_url=next_url, prev_url=prev_url)


@bp.route('/admin', methods=['GET', 'POST'])
@bp.route('/admin/', methods=['GET', 'POST'])
def admin():
 
 
    users = User.query.all()
    if len(users) == 0:
        u = User(username='admin')
        u.set_password('secret-password')
        db.session.add(u)
        db.session.commit()
        
    boards = Board.query.all()
    if len(boards) == 0:
        b = Board(ref='b', description='Random talks')
        db.session.add(b)
        db.session.commit()
    
    try:
        file = open('test.txt')  # наличие флаги будет флагом
    except IOError as e:
        # загружаем из бд картинки в систему
        pass
    else:
        print('Not first start, okay.')
 
 
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('main.admin'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@bp.route('/logout')
@bp.route('/logout/')
def logout():
    logout_user()
    return redirect(url_for('main.index'))


# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     if current_user.is_authenticated:
#         return redirect(url_for('index'))
#     form = RegistrationForm()
#     if form.validate_on_submit():
#         user = User(username=form.username.data, email=form.email.data)
#         user.set_password(form.password.data)
#         db.session.add(user)
#         db.session.commit()
#         flash('Congratulations, you are now a registered user!')
#         return redirect(url_for('login'))
#     return render_template('register.html', title='Register', form=form)


# @app.route('/user/<username>')
# @login_required
# def user(username):
#     user = User.query.filter_by(username=username).first_or_404()
#     page = request.args.get('page', 1, type=int)
#     posts = user.posts.order_by(Post.timestamp.desc()).paginate(
#         page, app.config['POSTS_PER_PAGE'], False)
#     next_url = url_for('user', username=user.username, page=posts.next_num) \
#         if posts.has_next else None
#     prev_url = url_for('user', username=user.username, page=posts.prev_num) \
#         if posts.has_prev else None
#     return render_template('user.html', user=user, posts=posts.items,
#                            next_url=next_url, prev_url=prev_url)


# @app.route('/edit_profile', methods=['GET', 'POST'])
# @login_required
# def edit_profile():
#     form = EditProfileForm(current_user.username)
#     if form.validate_on_submit():
#         current_user.username = form.username.data
#         current_user.about_me = form.about_me.data
#         db.session.commit()
#         flash('Your changes have been saved.')
#         return redirect(url_for('edit_profile'))
#     elif request.method == 'GET':
#         form.username.data = current_user.username
#         form.about_me.data = current_user.about_me
#     return render_template('edit_profile.html', title='Edit Profile',
#                            form=form)


# @app.route('/follow/<username>')
# @login_required
# def follow(username):
#     user = User.query.filter_by(username=username).first()
#     if user is None:
#         flash('User {} not found.'.format(username))
#         return redirect(url_for('index'))
#     if user == current_user:
#         flash('You cannot follow yourself!')
#         return redirect(url_for('user', username=username))
#     current_user.follow(user)
#     db.session.commit()
#     flash('You are following {}!'.format(username))
#     return redirect(url_for('user', username=username))


# @app.route('/unfollow/<username>')
# @login_required
# def unfollow(username):
#     user = User.query.filter_by(username=username).first()
#     if user is None:
#         flash('User {} not found.'.format(username))
#         return redirect(url_for('index'))
#     if user == current_user:
#         flash('You cannot unfollow yourself!')
#         return redirect(url_for('user', username=username))
#     current_user.unfollow(user)
#     db.session.commit()
#     flash('You are not following {}.'.format(username))
#     return redirect(url_for('user', username=username))


N = 12


@bp.route('/')
def index():
    boards = Board.query.all()
    if 'user' in session:
        pass
    else:
        session['user'] = ''.join(random.choices(string.ascii_uppercase + string.digits, k=N))
        session.permanent = True
    return render_template('index.html', boards=boards)



@bp.route('/<board>/res/<thread_num>', methods=['GET', 'POST'])
@bp.route('/<board>/res/<thread_num>/', methods=['GET', 'POST'])
def thread_big(thread_num, board):

    if 'user' in session:
        pass
    else:
        session['user'] = ''.join(random.choices(string.ascii_uppercase + string.digits, k=N))
        session.permanent = True

    form_del = PostDelForm()
    form = PostForm()


    if form_del.validate_on_submit() and (len(request.form.getlist('submit_del')) > 0):
        posts_to_del = request.form.getlist('del_checkbox')
        posts_to_del = (request.form.getlist('submit_hidden'))[0].split(',')
        print(form_del.submit_del)
        print(posts_to_del)
        if posts_to_del != ['']:
            for num in posts_to_del:
                p_to_del = Post.query.filter_by(id=num).first()
                p_to_del.is_deleted = 1
            db.session.commit()
        return redirect(url_for('main.thread_big', board=board, thread_num=thread_num))
    
    
    if form.validate_on_submit() and (len(request.form.getlist('submit')) > 0):
        print('ha')
        if (not request.files['image']) and (not form.post.data):
            flash("Pic or text required!")
            thread = Post.query.filter_by(OP_num=thread_num).order_by(Post.timestamp)
            return render_template('thread_big.html', posts=thread, board=board, form=form, guest=session.get('user'))
        OP_flag = form.written_by_OP.data
        if OP_flag:
            OP_flag = 1
        else:
            OP_flag = 0
        p = Post(body=form.post.data, OP_flag=OP_flag, OP_num=thread_num, board_name=board, guest_id=session.get('user'), is_sage=0, is_deleted=0)
        db.session.add(p)
        db.session.commit()
        
        # Поднимаем тред
        if (not form.sage.data) and (len(Post.query.filter_by(OP_num=thread_num).all()) < 50):
            OP_p = Post.query.filter_by(id=thread_num).first()
            OP_p.last_bump = datetime.datetime.utcnow()
            db.session.commit()
        else: #if (form.sage.data):
            p.is_sage = 1
            db.session.commit()

        file = request.files['image']
        # if file and allowed_file(file.filename):
        #     filename = secure_filename(file.filename)
        #     file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # TODO сделать проверки на тип и название и размер
        if file:
            filename = str(str(p.id) + '.' + file.filename.split('.')[-1])
            
            file.save(os.path.abspath(os.path.join(os.path.abspath(os.curdir), "app/static/image_posts/", str(filename))))  # os.path.join
            image = Image.open(file)
            image_th = Image.open(file)
            image_th.thumbnail((120, 120), Image.ANTIALIAS)
            image_th.save(os.path.abspath(os.path.join(os.path.abspath(os.curdir), "app/static/image_posts/thumb/", str(filename))))  # , 'JPEG'

            ###
            # print(file.read())
            # with open(file.read()) as image_file:
            buffered = BytesIO()
            image.save(buffered, format="JPEG")

            encoded_string = base64.b64encode(buffered.getvalue())
            response = requests.post(
                    'https://api.imgbb.com/1/upload?key=b6acbdd3baa7d6286c87772e95dc33b8',
                    data={'image': encoded_string}, verify=False)

            #print(response.json())

            buffered2 = BytesIO()
            image_th.save(buffered2, format="JPEG")

            encoded_string_thumb = base64.b64encode(buffered2.getvalue())
            response_thumb = requests.post(
                    'https://api.imgbb.com/1/upload?key=b6acbdd3baa7d6286c87772e95dc33b8',
                    data={'image': encoded_string_thumb}, verify=False)
            ###
            #print(response.json())
            #print(response_thumb.json())
            p.image_ref = response.json()['data']['url']
            p.thumb_ref = response_thumb.json()['data']['url']
            
            db.session.commit()


        reply = re.findall(r'>>\d+', p.body)
        for i in range(len(reply)):
            num = reply[i].split('>>')[-1]
            post_to_reply = Post.query.filter_by(id=num).first()
            if post_to_reply:
                post_to_reply._answers += [p.id]
                db.session.commit()

        return redirect(url_for('main.thread_big', board=board, thread_num=thread_num, _anchor=("post_num_" + str(p.id))))
    thread = Post.query.filter_by(
        OP_num=thread_num, is_deleted=0).order_by(Post.timestamp)  # , is_deleted=0
    return render_template('thread_big.html', posts=thread, board=board, form=form, guest=session.get('user'), form_del=form_del)


def sort_of_threads(list_of_threads):
    if (list_of_threads[0].last_bump):
        return list_of_threads[0].last_bump
    else:
        return list_of_threads[-1].timestamp


@bp.route('/<board>', methods=['GET', 'POST'])
@bp.route('/<board>/', methods=['GET', 'POST'])
@bp.route('/<board>/<int:page>', methods=['GET', 'POST'])
@bp.route('/<board>/<int:page>/', methods=['GET', 'POST'])
def board_b(board, page=1):

    if 'user' in session:
        pass
    else:
        session['user'] = ''.join(random.choices(string.ascii_uppercase + string.digits, k=N))
        session.permanent = True

    form = ThreadForm()
    if form.validate_on_submit():
        
        print('thread')
        if (not request.files['image']) and (not form.post.data):
            flash("Pic required!")
            print('nooo')
            OP_posts = Post.query.filter(Post.board_name == board, Post.id == Post.OP_num).order_by(Post.timestamp)
            new_posts = []
            for OP in OP_posts:
                # изменить фильтр поиска op_flag
                new_posts.append([OP] + Post.query.filter(Post.OP_num == OP.OP_num, Post.id != OP.OP_num).order_by(Post.timestamp)[-3:])
            new_posts.sort(key=sort_of_threads, reverse=True)
            # разворачивание списка
            listmerge = (lambda x: [el for lst in x for el in lst])(new_posts)

            return render_template('board.html', posts=listmerge, form=form)

        OP_flag = 1

        p = Post(body=form.post.data, OP_flag=1, board_name=board, guest_id=session.get('user'), last_bump=datetime.datetime.utcnow(), is_sage=0, is_deleted=0)
        #p = Post(body=form.post.data, OP_flag=1, OP_num=thread_num, board_name=board, guest_id=session.get('user'), is_sage=0, is_deleted=0)
        db.session.add(p)
        db.session.commit()

        # надо записывать айди оп поста в сам оп пост
        p.OP_num = p.id
        db.session.commit()
        
        # Поднимаем тред
        # if (not form.sage.data) and (len(Post.query.filter_by(OP_num=thread_num).all()) < 50):
        #     OP_p = Post.query.filter_by(id=thread_num).first()
        #     OP_p.last_bump = datetime.datetime.utcnow()
        #     db.session.commit()
        # else: #if (form.sage.data):
        #     p.is_sage = 1
        #     db.session.commit()

        file = request.files['image']
        # if file and allowed_file(file.filename):
        #     filename = secure_filename(file.filename)
        #     file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # TODO сделать проверки на тип и название и размер
        if file:
            filename = str(str(p.id) + '.' + file.filename.split('.')[-1])
            
            file.save(os.path.abspath(os.path.join(os.path.abspath(os.curdir), "app/static/image_posts/", str(filename))))  # os.path.join
            image = Image.open(file)
            image_th = Image.open(file)
            image_th.thumbnail((120, 120), Image.ANTIALIAS)
            image_th.save(os.path.abspath(os.path.join(os.path.abspath(os.curdir), "app/static/image_posts/thumb/", str(filename))))  # , 'JPEG'

            ###
            # print(file.read())
            # with open(file.read()) as image_file:
            buffered = BytesIO()
            image.save(buffered, format="JPEG")

            encoded_string = base64.b64encode(buffered.getvalue())
            response = requests.post(
                    'https://api.imgbb.com/1/upload?key=b6acbdd3baa7d6286c87772e95dc33b8',
                    data={'image': encoded_string}, verify=False)

            #print(response.json())

            buffered2 = BytesIO()
            image_th.save(buffered2, format="JPEG")

            encoded_string_thumb = base64.b64encode(buffered2.getvalue())
            response_thumb = requests.post(
                    'https://api.imgbb.com/1/upload?key=b6acbdd3baa7d6286c87772e95dc33b8',
                    data={'image': encoded_string_thumb}, verify=False)
            ###
            #print(response.json())
            #print(response_thumb.json())
            p.image_ref = response.json()['data']['url']
            p.thumb_ref = response_thumb.json()['data']['url']
            
            db.session.commit()

        reply = re.findall(r'>>\d+', p.body)
        for i in range(len(reply)):
            num = reply[i].split('>>')[-1]
            post_to_reply = Post.query.filter_by(id=num).first()
            if post_to_reply:
                post_to_reply._answers += [p.id]
                db.session.commit()
        print(p)
        # удаляем уплывшие треды
        list_of_threads = Post.query.filter(Post.board_name == board, Post.OP_num == Post.id).all()       
        ext_threads = list_of_threads[30:]
        if (len(ext_threads) > 0):
            for item in ext_threads:
                #all_posts = Post.query.filter_by(OP_num=item.OP_num).delete()  # .all()
                db.session.query(Post).filter(Post.OP_num == item.OP_num).delete()
                #db.session.delete_all(all_posts)
                db.session.commit()


        # if (not form.post.data):  # request.files['image']
        #     flash("Pic required!")

        #     OP_posts = Post.query.filter(Post.board_name == board, Post.id == Post.OP_num).order_by(Post.timestamp)
        #     new_posts = []
        #     for OP in OP_posts:
        #         # изменить фильтр поиска op_flag
        #         new_posts.append([OP] + Post.query.filter(Post.OP_num == OP.OP_num, Post.id != OP.OP_num).order_by(Post.timestamp)[-3:])
        #     new_posts.sort(key=sort_of_threads, reverse=True)
        #     # разворачивание списка
        #     listmerge = (lambda x: [el for lst in x for el in lst])(new_posts)

        #     return render_template('board.html', posts=listmerge, form=form)
        
        # p = Post(body=form.post.data, OP_flag=1, board_name=board, guest_id=session.get('user'), last_bump=datetime.datetime.utcnow())
        # db.session.add(p)
        # db.session.commit()
        # # надо записывать айди оп поста в сам оп пост
        # p.OP_num = p.id
        # db.session.commit()
        
        # # удаляем уплывшие треды
        # list_of_threads = Post.query.filter(Post.board_name == board, Post.OP_num == Post.id).all()       
        # ext_threads = list_of_threads[20:]
        # if (len(ext_threads) > 0):
        #     for item in ext_threads:
        #         #all_posts = Post.query.filter_by(OP_num=item.OP_num).delete()  # .all()
        #         db.session.query(Post).filter(Post.OP_num == item.OP_num).delete()
        #         #db.session.delete_all(all_posts)
        #         db.session.commit()
        
        return redirect(url_for('main.thread_big', board=board, thread_num=p.id))
    
    # условие равенства айди и номера оп-поста
    # page = request.args.get('page', 1, type=int)
    '''
    .paginate(
        page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('index', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('index', page=posts.prev_num) \
        if posts.has_prev else None
    '''
    OP_posts = Post.query.filter(Post.board_name == board, Post.id == Post.OP_num, Post.is_deleted == 0).order_by(Post.last_bump.desc()).paginate(page, 6, False) # 2 - кол-во тредов на страницу
    new_posts = []
    for OP in OP_posts.items:
        # изменить фильтр поиска op_flag
        new_posts.append([OP] + Post.query.filter(Post.OP_num == OP.OP_num, Post.id != OP.OP_num, Post.is_deleted == 0).order_by(Post.timestamp)[-3:])
    new_posts.sort(key=sort_of_threads, reverse=True)
    # new_posts = new_posts
    # разворачивание списка
    #listmerge = (lambda x: [el for lst in x for el in lst])(new_posts)
    return render_template('board.html', threads=new_posts, form=form, board=board, page=page)


@bp.route('/admin_panel')
@bp.route('/admin_panel/')
@login_required
def admin_panel():
    return ''' Surprise, yeah! '''


@bp.route('/add_board', methods=['GET', 'POST'])
@bp.route('/add_board/', methods=['GET', 'POST'])
@login_required
def add_board():
    form = BoardAddForm()
    if form.validate_on_submit():
        b = Board(ref=form.ref.data, description=form.description.data)
        db.session.add(b)
        db.session.commit()
        return redirect(url_for('main.board_b', board=b.ref))
    return render_template('add_board.html', form=form)
