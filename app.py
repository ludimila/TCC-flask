from flask import Flask
from flask.ext import excel
from flask_bootstrap import Bootstrap
from flask import request, redirect, url_for, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore, RoleMixin, UserMixin, login_required
from datetime import datetime
from flask_security.forms import RegisterForm
from wtforms import StringField
from flask.ext.login import current_user



app = Flask(__name__)
Bootstrap(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ludimila:tcc2@localhost/gamifier'
app.debug = True
app.config['SECRET_KEY'] = 'super-secret'
app.config['SECURITY_REGISTERABLE'] = True
app.config['SECURITY_POST_LOGIN_VIEW'] = '/profile'

db = SQLAlchemy(app)



# Define models
roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class User(db.Model,UserMixin):
  id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.String(255), unique=True)
  username = db.Column(db.String(255), unique=False)
  password = db.Column(db.String(255))
  active = db.Column(db.Boolean())
  confirmed_at = db.Column(db.DateTime())
  roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))
  projects = db.relationship('GamificationProject', backref='user',
                              lazy='dynamic')

  def __init__(self, username, email, password, confirmed_at, active):
      self.username = username
      self.email = email
      self.password = password
      self.confirmed_at = confirmed_at
      self.active = active


#setup security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app,user_datastore)

# class ExtendedRegisterForm(RegisterForm):
#   username = StringField('Username',[Required()])

# security = Security(app, user_datastore,
#          register_form=ExtendedRegisterForm)




projects_types = db.Table('projects_types',
        db.Column('gamification_project_id', db.Integer(), db.ForeignKey('gamification_project.id')),
        db.Column('gamification_type_id', db.Integer(), db.ForeignKey('gamification_type.id')))

projects_techniques = db.Table('projects_techniques',
        db.Column('gamification_tecnique_id', db.Integer(), db.ForeignKey('gamification_technique.id')),
        db.Column('gamification_project_id', db.Integer(), db.ForeignKey('gamification_project.id')))

class GamificationProject(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name_project = db.Column(db.String(80), unique=True)
    description_project = db.Column(db.String(3000))
    creation_date = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    techniques = db.relationship('GamificationTechnique', secondary=projects_techniques, 
                                  backref=db.backref('techniques', lazy='dynamic'))

    def __init__(self, name_project, description_project, creation_date, user_id):
      self.name_project = name_project
      self.description_project = description_project
      self.creation_date = creation_date
      self.user_id = user_id


class GamificationType(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name_gamification_type = db.Column(db.String(255), unique=True)
    description_gamification_type = db.Column(db.String(5000))
    types = db.relationship('GamificationType', secondary=projects_types,
                            backref=db.backref('projects', lazy='dynamic'))


#many_GamificationProject_has_many_CoreDrive
projects_coredrivers = db.Table('projects_coredrivres',
   db.Column('gamification_project_id', db.Integer, db.ForeignKey('gamification_project.id')),
   db.Column('core_drive_id', db.Integer, db.ForeignKey('core_drive.id'))
)


#many_CoreDrive_has_many_GamificationTechnique
cores_techiques = db.Table('cores_techiques',
   db.Column('core_drive_id', db.Integer, db.ForeignKey('core_drive.id')),
   db.Column('gamification_technique_id', db.Integer, db.ForeignKey('gamification_technique.id'))
)

class CoreDrive(db.Model):
	id = db.Column(db.Integer(), primary_key=True)
	name_core_drive = db.Column(db.String(80), unique=True)
	description_core_drive = db.Column(db.String(3000))
	techniques = db.relationship('GamificationTechnique', secondary=cores_techiques,
       backref=db.backref('core_drives', lazy='dynamic'))

class TechniquesAtributtes(db.Model):
    __tablename__ = 'techniques_atributtes'
    gamification_technique_id = db.Column(db.Integer(), db.ForeignKey('gamification_technique.id'), primary_key=True)
    atributte_id = db.Column(db.Integer(), db.ForeignKey('atributte.id'), primary_key=True)
    likert = db.Column(db.Float())
    atributte = db.relationship("Atributte", back_populates="gamificationtechniques")
    technique = db.relationship("GamificationTechnique", back_populates="atributtes")

class GamificationTechnique(db.Model):
  __tablename__ = 'gamification_technique'
  id = db.Column(db.Integer(), primary_key=True)
  name_gamification_technique = db.Column(db.String(80), unique=True)
  description_gamification_technique = db.Column(db.String(3000))
  number_gamification_technique = db.Column(db.Integer())
  number_core = db.Column(db.Integer())
  atributtes = db.relationship("TechniquesAtributtes", back_populates="technique")

  #classe de atributos das técnicas
class Atributte(db.Model):
  __tablename__ = 'atributte'
  id = db.Column(db.Integer(), primary_key=True)
  name_atributte = db.Column(db.String(80), unique=True)
  description_atributte = db.Column(db.String(3000))
  gamificationtechniques = db.relationship("TechniquesAtributtes", back_populates="atributte")


#rotas para as páginas
@app.route('/')
def index():
  return render_template('index.html')


@app.route('/profile')
def profile():
  cores = CoreDrive.query.all()
  my_user = User.query.all()
  my_technique = GamificationTechnique.query.all()

  if request.method == 'POST':
    user = User(request.form['name'],request.form['email'],request.form['password'],datetime.now(), True)
    db.session.add(user)
    db.session.commit()
    return render_template('profile.html',my_user=my_user,my_technique=my_technique)
  else:
    return render_template('profile.html',my_user=my_user,my_technique=my_technique)


@app.route('/projects')
def projects():
  projects = GamificationProject.query.filter_by(user_id = current_user.id).all()
  return render_template('projects.html',projects=projects)


@app.route('/dashboard',methods=['POST'])
@login_required
def dashboard():

  attention = 0
  persistence = 0
  participation = 0
  mastery = 0
  social = 0
  work_involvement = 0

  my_core = CoreDrive.query.all()
  my_result = GamificationType.query.all()
  my_atributte = Atributte.query.all()

  techniques = request.form['id_technique'].split(' ')
  techniques = list(filter(None, techniques))
  int_techniques = list(map(int, techniques))
  my_project = GamificationProject.query.all()
  current_user_form = request.form['current_user']
  current_project = GamificationProject(request.form['project_name'],request.form['project_description'],datetime.now(), current_user_form)

  for technique in int_techniques:
    currents_techniques = GamificationTechnique.query.filter_by(id = technique).first()
    current_project.techniques.append(currents_techniques)


    for att in currents_techniques.atributtes:
      if att.atributte_id == 1:
        attention += att.likert
      elif att.atributte_id == 2:
        persistence += att.likert
      elif att.atributte_id == 3:
        participation += att.likert
      elif att.atributte_id == 4:
        mastery += att.likert
      elif att.atributte_id == 5:
        social += att.likert
      elif att.atributte_id == 6:
        work_involvement += att.likert

  content = {'attention':attention,
             'persistence':persistence,
             'participation':participation,
             'mastery':mastery,
             'social':social,
             'work_involvement':work_involvement}
  db.session.add(current_project)
  db.session.commit()
  return render_template('dashboard.html',my_atributte = my_atributte, my_result = my_result, my_core = my_core, 
    current_project = current_project, currents_techniques = currents_techniques, content = content)
    
 
@app.route("/csv_export", methods=['GET'])
def csvexport():
  projects_user = GamificationProject.query.filter_by(user_id = current_user.id).all()
  column_names = ['id','name_project', 'description_project','creation_date','user_id','techniques']
  return excel.make_response_from_query_sets(projects_user, column_names, "csv")


@app.route('/login', methods=['GET', 'POST'])
def login():
   
    form = LoginForm()
    if form.validate_on_submit():

        login_user(user)

        flask.flash('Logged in successfully.')

        next = flask.request.args.get('next')
        if not next_is_valid(next):
            return flask.abort(400)

        return flask.redirect(next or flask.url_for('profile'))
    return flask.render_template('login.html', form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect('index')


if __name__ == '__main__':
	app.run()