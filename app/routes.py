# from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, session
from flask_login import login_user, logout_user, current_user, login_required
# from werkzeug.urls import url_parse
# from app import app, db
# from app.forms import LoginForm, RegistrationForm, EditProfileForm, PostForm
# from app.models import User, Post



from flask import render_template
from app import app, db
from app.models import Board, Post, User
from app.forms import PostForm, ThreadForm, LoginForm, PostDelForm
import os
from PIL import Image
import re
import datetime



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


@app.route('/admin', methods=['GET', 'POST'])
@app.route('/admin/', methods=['GET', 'POST'])
def admin():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('admin'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
@app.route('/logout/')
def logout():
    logout_user()
    return redirect(url_for('index'))


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





@app.route('/')
def index():
    boards = Board.query.all()
    if 'user' in session:
        pass
    else:
        session['user'] = os.urandom(24)
        session.permanent = True
    return render_template('index.html', boards=boards)


@app.route('/<board>/res/<thread_num>', methods=['GET', 'POST'])
@app.route('/<board>/res/<thread_num>/', methods=['GET', 'POST'])
def thread_big(thread_num, board):

    if 'user' in session:
        pass
    else:
        session['user'] = os.urandom(24)
        session.permanent = True

    form_del = PostDelForm()
    form = PostForm()


    if form_del.validate_on_submit() and (len(request.form.getlist('submit_del')) > 0):
        posts_to_del = request.form.getlist('del_checkbox')
        posts_to_del = (request.form.getlist('submit_hidden'))[0].split(',')
        print(form_del.submit_del)
        for num in posts_to_del:
            p_to_del = Post.query.filter_by(id=num).first()
            p_to_del.is_deleted = 1
        db.session.commit()
        return redirect(url_for('thread_big', board=board, thread_num=thread_num))
    
    
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
            file.save(os.path.join("C:\\2ch\\imageboard\\app\\static\\image_posts", filename))
            image = Image.open(file)
            image.thumbnail((120, 120), Image.ANTIALIAS)
            image.save(os.path.join("C:\\2ch\\imageboard\\app\\static\\image_posts\\thumb", filename))  # , 'JPEG'

            p.image_ref = filename
            db.session.commit()

        reply = re.findall(r'>>\d+', p.body)
        for i in range(len(reply)):
            num = reply[i].split('>>')[-1]
            post_to_reply = Post.query.filter_by(id=num).first()
            if post_to_reply:
                post_to_reply._answers += [p.id]
                db.session.commit()

        return redirect(url_for('thread_big', board=board, thread_num=thread_num, _anchor=("post_num_" + str(p.id))))
    thread = Post.query.filter_by(
        OP_num=thread_num, is_deleted=0).order_by(Post.timestamp)  # , is_deleted=0
    return render_template('thread_big.html', posts=thread, board=board, form=form, guest=session.get('user'), form_del=form_del)


def sort_of_threads(list_of_threads):
    if (list_of_threads[0].last_bump):
        return list_of_threads[0].last_bump
    else:
        return list_of_threads[-1].timestamp

@app.route('/<board>', methods=['GET', 'POST'])
@app.route('/<board>/', methods=['GET', 'POST'])
@app.route('/<board>/<int:page>', methods = ['GET', 'POST'])
@app.route('/<board>/<int:page>/', methods = ['GET', 'POST'])
def board_b(board, page=1):

    if 'user' in session:
        pass
    else:
        session['user'] = os.urandom(24)
        session.permanent = True

    form = ThreadForm()
    if form.validate_on_submit():
        
        if (not form.post.data):  # request.files['image']
            flash("Pic required!")

            OP_posts = Post.query.filter(Post.board_name == board, Post.id == Post.OP_num).order_by(Post.timestamp)
            new_posts = []
            for OP in OP_posts:
                # изменить фильтр поиска op_flag
                new_posts.append([OP] + Post.query.filter(Post.OP_num == OP.OP_num, Post.id != OP.OP_num).order_by(Post.timestamp)[-3:])
            new_posts.sort(key=sort_of_threads, reverse=True)
            # разворачивание списка
            listmerge = (lambda x: [el for lst in x for el in lst])(new_posts)

            return render_template('board.html', posts=listmerge, form=form)
        
        p = Post(body=form.post.data, OP_flag=1, board_name=board, guest_id=session.get('user'), last_bump=datetime.datetime.utcnow())
        db.session.add(p)
        db.session.commit()
        # надо записывать айди оп поста в сам оп пост
        p.OP_num = p.id
        db.session.commit()
        
        # удаляем уплывшие треды
        list_of_threads = Post.query.filter(Post.board_name == board, Post.OP_num == Post.id).all()       
        ext_threads = list_of_threads[20:]
        if (len(ext_threads) > 0):
            for item in ext_threads:
                #all_posts = Post.query.filter_by(OP_num=item.OP_num).delete()  # .all()
                db.session.query(Post).filter(Post.OP_num == item.OP_num).delete()
                #db.session.delete_all(all_posts)
                db.session.commit()
        
        return redirect(url_for('thread_big', board=board, thread_num=p.id))
    
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
    OP_posts = Post.query.filter(Post.board_name == board, Post.id == Post.OP_num, Post.is_deleted == 0).order_by(Post.last_bump.desc()).paginate(page, 2, False) # 2 - кол-во тредов на страницу
    new_posts = []
    for OP in OP_posts.items:
        # изменить фильтр поиска op_flag
        new_posts.append([OP] + Post.query.filter(Post.OP_num == OP.OP_num, Post.id != OP.OP_num, Post.is_deleted == 0).order_by(Post.timestamp)[-3:])
    new_posts.sort(key=sort_of_threads, reverse=True)
    # new_posts = new_posts
    # разворачивание списка
    #listmerge = (lambda x: [el for lst in x for el in lst])(new_posts)

    return render_template('board.html', threads=new_posts, form=form, board=board, page=page)


@app.route('/admin_panel')
@app.route('/admin_panel/')
@login_required
def admin_panel():
    return ''' Surprise, yopta! '''

