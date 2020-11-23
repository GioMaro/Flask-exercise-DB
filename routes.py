from flask import Flask,render_template, session,redirect
from datetime import datetime
from forms import registration, login
from flask_bcrypt import Bcrypt
from running import db
from running import app







from modeldb import Role, User

def apply_routing(app):
    list = ['Andrea', 'Elena', 'Edoardo', 'Francesco']
    posts = [
     {
     'author': 'Mohammad',
     'title': 'Flask session 1',
     'content':  'please continue....',
     'date_posted': '19 Oct. 2020'
     },
     {
     'author': 'Andrea',
     'title': 'Flask session 2',
     'content': 'please continue....',
     'date_posted': '19 Oct. 2020'
     },
     {
     'author': 'Edoardo',
     'title': 'Flask session 3',
     'content': 'please continue....',
     'date_posted': '19 Oct. 2020'
     },
     {
     'author': 'Sina',
     'title': 'Flask session 4',
     'content': 'please continue....',
     'date_posted': '19 Oct. 2020'
     }
    ]


    @app.route('/')
    def hello_world():
        return render_template('Hello.html', website='IS Course', current_time=datetime.utcnow())

    '''Please develop a web page which can get an id then can return
    the corresponding name from this list:
    ["Andrea","Elena","Edoardo","Francesco"]'''

    @app.route('/student/<int:id>')
    def ex1(id):
        if id<len(list):
            return '<h1> Hello %s! </h1>' %list[id]
        else:
            return 'Invalid ID'

    '''Please develop a Flask application, which it can return names from the above list to
    the HTML code by using the render_template('page.html')'''

    @app.route('/studenthtml/<int:id>')
    def ex2(id):
        if id<len(list):
            name=list[id]
        else:
            name='Guest'
        return render_template('page.html',name=name)

    '''In this exercise, you need to work with static files; please add the bootstrap
    framework to your project and Develop an HTML page by using the CSS
    framework. In this practice, you need to use url_for('static', filename='pathfilename')'''

    @app.route('/example')
    def ex3():
        return render_template('templatehtml.html')

    '''Develop a webpage by using the template engine and show the list of posts on the
    page; the code has to develop by using the Jinja2 loop syntax.'''
    @app.route('/blog')
    def ex4():
        return render_template('blog.html',posts=posts)

    '''Develop a page by dividing one single HTML page into a sub-section by using Jinja
    and Flask Framework.
    Layout.html: consist of a menu and main HTML like a header and other
    parts.
    Main.html: consist of your data which is coming from python'''

    @app.route('/blog2')
    def ex5():
        return render_template('blog2.html',posts=posts)

    '''Develop a webpage with webform that asks for the following information:
    Name
    Family name
    Email
    After submitting the webform, we would like to redirect the user to a welcome
    page and showing the client this sentence:
    Hello Mr. "name" "Family"", please check your email!'''


    @app.route('/registration', methods=['POST','GET'])
    def ex6():
        name=None
        form=registration()
        if form.validate_on_submit():
            session['Name']=form.name.data
            name=form.name.data
            session['Surname']=form.surname.data
            return redirect('dashboard')
        else:
            return render_template('form.html',form=form,name=name)

    @app.route('/dashboard')
    def dashboard():
        if session.get('Name'):
            return render_template('dashboard.html')
        else:
            return redirect('registration')


    #Lab2 Ex 1

    #Ex 2
    @app.before_first_request
    def setup():
        role_teacher = Role(name='Teacher')
        role_student = Role(name='Student')
        role_admin = Role(name='Admin')
        with app.push_context():
            db.session.add_all(role_student,role_teacher,role_admin)
            db.session.commit()
        db.create_all()

    #Ex 3
    @app.route('/registration2',methods=['GET','POST'])
    def reg():
        name=None
        reg=registration()
        if reg.validate_on_submit():
            session['Name']=reg.name.data
            session['Mail']=reg.email.data
            password_2=Bcrypt.generate_password_hash(reg.password.data).encode('utf-8')
            with app.push.context():
                new=User(name=session.get('Name'),username=reg.email.data,email=reg.email.data,password=password_2)
                db.session.add(new)
                db.session.commit()

            return redirect('dashboard')
        return render_template('register.html',reg=reg,name=name)

    #ex5
    @app.route('/login')
    def log():
        log = login()
        username=None
        if log.validate_on_submit():
            #verifico che sia presente e poi encritto tutto:
            user_check=User.query.filtery_by(username=log.username.data).first()
            if user_check and Bcrypt.generate_password_hash(log.password, user_check.password):
                session['Username']=user_check.username
                session['ID']=user_check.id
                session['Name']=user_check.name
                session['Email']=user_check.email
                session['RoleID']=user_check.role_id
                return redirect('dashboard')
        else:
            return render_template('login.html',log=log)

    @app.route('/logout')
    def logout():
        session.clear()
        return redirect('ex5')






    @app.errorhandler(404)
    def err1():
        return render_template('404.html')



    return app
