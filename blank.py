from flask import Flask
import session


app = Flask(__name__)
app.config['SECRET_KEY'] = 'any random string' #must be set


@app.route('/')
def hello():
    return render_template('template_file.html', var1=value1)


@app.route('/hello/<string:name>')
def hello(name):
    if 'key_name' in session: #session exists and has key
        session_var = session['key_value'] 
    else: #session does not exist
        session['key_name'] = 'key_value' #stores a secure cookie in browser
    return 'Hello ' + name + '!' 
    



# models.py

class Thread(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    OP_num = db.Column(db.Integer, index=True, unique=True)
    name = db.Column(db.String(120))
    OP_user = db.Column(db.String(128))
    posts = db.relationship('Post', backref='thread', lazy='dynamic')
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    board = db.Column(db.String(10), unique=True)

    def __repr__(self):
        return '<Thread {}>'.format(self.name)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    OP_flag = db.Column(db.Integer)
    image_ref = db.Column(db.String(120))
    thread_id = db.Column(db.Integer, db.ForeignKey('thread.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)




# routes.py

@app.route('/thread/<thread_num>')
def thread_big(thread_num):
    thread = Thread.query.filter_by(id=thread_num).first_or_404()
    posts = thread.posts.order_by(Post.timestamp.desc())  # .paginate(page, app.config['POSTS_PER_PAGE'], False)
    if str(thread_num) in session: #session exists and has key
        op = session[str(thread_num)]
    return render_template('thread_big.html', posts=posts, op=op)


@app.route('/b')
def board_b():
# тут нужно к каждому треду передавать 4 последних поста. хотя они и так передаются, их нужно грамотно вытащить в темплейте
    threads = Thread.query.filter_by(board='b').
   # короче тут надо отсортировать по времени последнего поста
    order_by(Thread.posts.order_by(Post.timestamp.desc())[-1].timestamp.desc()).paginate(
        page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('board', board='b', page=threads.next_num) \
        if threads.has_next else None
    prev_url = url_for('board', board='b', page=threads.prev_num) \
        if threads.has_prev else None
    return render_template('board.html', threads=threads.items, next_url=next_url, prev_url=prev_url)

# в темплейте должно быть следующее: 
{% for thread in threads %}
    {% include '_thread.html' %}
     # а нижнее в _thread.html
    {% for post in thread.posts.order_by(Post.timestamp.desc())[-4:] %}
        {% include '_post.html' %}
    {% endfor %}
{% endfor %}



<html>
    <head>
    </head>

    <body>
        <div>
            {{posts[0].body}}
        </div>
        <br>
        {% for post in posts.order_by(Post.timestamp.desc()) %}
        <div> 
            {{post.body}}
        </div>
        {% end for %}
    </body>
</html>



<html>
    <head>
    </head>

    <body>
    {% for thread in threads %}
        <div>
            {{thread.posts[0].body}}
        </div>
        <br>
        {% for post in thread.posts.order_by(Post.timestamp.desc()) %}
        <div> 
            {{post.body}}
        </div>
        <br>
        {% end for %}
        <br>
    {% endfor %}
    </body>
</html>




    
if __name__ == '__main__':
    app.run(debug=True)
