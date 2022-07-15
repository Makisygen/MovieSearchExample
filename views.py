from flask import Flask, render_template,request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_, or_, not_

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///Example.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO']=True

#@app.route('/')
#def hello():
#    return "Hello Test"

db = SQLAlchemy(app)

class Movie(db.Model):
    __tablename__ = 'Movie'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    category = db.Column(db.Text)
    price = db.Column(db.Integer)

@app.before_first_request
def init():
    db.create_all()

@app.route('/', methods=['GET'])
def index():
    datas = Movie.query.all()
    return render_template('search_result.html', lists = datas)

@app.route('/add', methods=['POST'])
def insert():
    name_txt = request.form['add_name']
    category_txt = request.form['add_category']
    price_txt = request.form['add_price']
    movie = Movie(name = name_txt, category = category_txt, price = price_txt)

    db.session.add(movie)
    db.session.commit()
    datas = Movie.query.all()
    return render_template('register.html', lists = datas)


@app.route('/register')
def register():
    datas = Movie.query.all()
    return render_template('register.html', lists = datas)

@app.route('/search', methods=['POST'])
def search():
    name_txt = request.form['search_name']
    category_list = request.form.getlist('search_category')
    price_txt = request.form['search_price']
    from_txt = request.form['from']
    query = db.session.query(Movie)

    # 絞り込み処理
    if len( category_list ) > 0 :
        query = query.filter(Movie.category.in_(category_list))
    query = query.filter(Movie.name.contains(name_txt))
    if price_txt == "0_1000":
        query = query.filter(Movie.price < 1000)
    elif price_txt == "1000_2000": 
        query = query.filter(Movie.price >= 1000)
        query = query.filter(Movie.price < 2000)
    elif price_txt == "2000_3000": 
        query = query.filter(Movie.price >= 2000)
        query = query.filter(Movie.price < 3000)
    elif price_txt == "3000_": 
        query = query.filter(Movie.price >= 3000)

    datas = query.all() 
    if from_txt == "admin":
        return render_template('register.html', lists = datas)
    return render_template('search_result.html', lists = datas)

@app.route('/delete', methods=['POST'])
def delete():
    query = db.session.query(Movie)
    target_id_list = request.form.getlist('delete_target_id')
    for target_id in target_id_list:
        delete = query.filter(Movie.id == target_id).delete()
        db.session.commit()
    datas = Movie.query.all()
    return render_template('register.html', lists = datas)

if __name__ == '__main__':
    app.run(debug=True)

