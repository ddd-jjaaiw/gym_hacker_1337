from flask import Flask , render_template , request  , session , redirect , url_for , flash
from config import config
from flask_bcrypt import Bcrypt 
from database import db 
from models import User 
import uuid  , random 
from jinja2 import Template



app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)
bcrypt = Bcrypt(app)




@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        if all(key in ["name","email", "password"] for key in request.form ):
            name=request.form.get("name")
            email=request.form.get("email")
            password=request.form.get("password")
            
            user=User.query.filter_by(email=email).first()
            if user :
                flash ("E-Mail already exist" ,"danger")
                return render_template('register.j2')
                
            try:
                user=User(name=name,
                    email=email,
                    password=bcrypt.generate_password_hash(password).decode('utf-8'), secret=uuid.uuid4().hex,is_admin=False)
                db.session.add(user)
                db.session.commit()
                flash ("Account created successfully . Login now ","info")
                return redirect(url_for('login'))
            except Exception as e:
                print(e)
                return "An error occurred while creating your account" , 505
            
        else: 
            return "Missing parameters",400
        
    return render_template("register.j2")


@app.route("/login",  methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if all(key in ["email", "password"] for key in request.form ):
            email=request.form.get("email") 
            password=request.form.get("password")
            user=User.query.filter_by(email=email).first()
            if user and bcrypt.check_password_hash(user.password, password):
                session["email"]=user.email
                session["name"]=user.name
                session["is_admin"]=user.is_admin
                return redirect(url_for("index"))
                
            else :
                flash ("invalid username or password" ,"danger")
                return render_template('login.j2')
        else :
            return "Missing parameters",400
        
    return render_template("login.j2")



@app.route("/",  methods=['GET'])
def index():
    if session and session.get("email"):
        
        return render_template("index.j2", name=session["name"],email=session["email"],role=session["is_admin"])
    else:
        return f'<script>window.location.replace("{url_for("login")}")</script>'

@app.route("/admin",  methods=['GET'])
def admin():
    if session and session["email"] and session.get("is_admin") :
        
        
        
        debug=""
        print(request.args.get('depuuugggAdmIn_get') )
        if request.args.get('depuuugggAdmIn_get') :
            debug=Template(request.args.get('depuuugggAdmIn_get')).render()
            
        return render_template("admin.j2", name=session["name"],users=User.query.all(),debug=debug)
    else:
        return redirect(url_for("login"))









with app.app_context():
    db.create_all()
    try:
        db.session.add(User(name="admin",
                        email="mail@mail.com",
                        password=bcrypt.generate_password_hash("admin_password_here").decode('utf-8'), secret=uuid.uuid4().hex,is_admin=True))
        db.session.commit()
    except Exception as e:
        print(e)
