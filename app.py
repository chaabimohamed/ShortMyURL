import pyshorteners
from flask import Flask,jsonify,request
from werkzeug.security import generate_password_hash,check_password_hash
import jwt
from flask_sqlalchemy import SQLAlchemy
import datetime
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = "restapi"
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:@localhost/users"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)



class user(db.Model):
    __tablename__= 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    admin = db.Column(db.Boolean, default=False)
    def __init__(self,email,password,admin=False):
        self.email = email
        self.password = generate_password_hash(password,method="sha256")
        self.admin = admin
    # def setemail(self,email):
    #     self.eamil = email




def tokenRequired(f):
    @wraps(f)
    def decorated(*args,**kwargs):
        token = None
        if 'x-api-key' in request.headers:
            token = request.headers['x-api-key']
        try:
            data= jwt.decode(token, app.config['SECRET_KEY'],algorithms="HS256")
            currentUser = user.query.filter_by(email=data['email']).first()
        except:
            return jsonify({'message:':'token not valid!'})

        return f(currentUser,*args,**kwargs)
    return decorated


#insert and get users
@app.route('/users', methods=['POST','GET'])
@tokenRequired
def users(currentUser):
    # insert user
    if request.method == 'POST':
        data = request.get_json()
        email=data['email']
        password=data['password']
        new_user = user(email,password)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message:':'new user created!'})
    # get all users
    userList = user.query.all()
    users = list()
    for i in userList:
        users.append(f'''id: {i.id}, email: {i.email}''')
    return jsonify({'users': users})




# delete user
@app.route('/users/<id>', methods=['DELETE'])
@tokenRequired
def delete_user(currentUser,id):
    singleUser = user.query.filter_by(id=id).first()
    if not singleUser:
        return jsonify({'message:':'user not found!'})
    db.session.delete(singleUser)
    db.session.commit()
    return jsonify({'message:':'user deleted!'})


#short links route
@app.route('/short/<path:longUrl>', methods=['GET'])
@tokenRequired
def shortUrl(currentUser,longUrl):
    try:
        typeTiny = pyshorteners.Shortener()
        shortUrl = typeTiny.tinyurl.short(str(longUrl))
        return jsonify({'url':shortUrl})
    except:
        return jsonify({'message':'try agein please!'})



#login route
@app.route('/login', methods=['POST'])
def login():
    auth=request.authorization
    username= auth.username
    password = auth.password
    if not username or not password:
        return jsonify({'message':'we have problem!'})
        
    singleUser = user.query.filter_by(email=username).first()
    if not singleUser:
        return jsonify({'message':'user not found!'})
   
    if check_password_hash(singleUser.password,password):
        token = jwt.encode({"email":singleUser.email,'exp':datetime.datetime.utcnow()+datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])
        return jsonify({'token': token})
    return jsonify({'message':'login error!'})
