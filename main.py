from flask import Flask, redirect, render_template, request, abort, jsonify, url_for
from data import db_session
from flask_login import LoginManager, login_user, login_required, current_user, logout_user

from utils import save_picture, save_user_picture

from forms.login import LoginForm
from forms.job_form import JobForm
from forms.register_form import RegisterForm
from forms.department_form import DepartmentForm
from forms.galery_form import GaleryForm
from forms.load_photo_form import UserPhotoForm

from data.jobs import Jobs
from data.users import User
from data.departments import Department
from data.photo import Photo

import datetime
from data import db_session, jobs_api
from flask import make_response


app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/')
def index():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    return render_template("index.html",
                           jobs=jobs,
                           title="Главная",
                           j_or_d='j')


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.hashed_password:
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html',
                           title='Авторизация',
                           form=form)


@app.route('/register', methods=['GET', 'POST'])
def registration():
    form = RegisterForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user:
            return render_template('registration.html',
                                   form=form,
                                   title='Регистрация',
                                   message='Такой пользователь уже зарегистрирован')
        if form.password.data != form.repeat_password.data:
            return render_template('registration.html',
                                   form=form,
                                   title='Регистрация',
                                   message='Пароли не совпадают')
        user = User()
        user.email = form.email.data
        user.hashed_password = form.password.data
        user.surname = form.surname.data
        user.name = form.name.data
        user.age = form.age.data
        user.position = form.position.data
        user.speciality = form.speciality.data
        user.address = form.address.data
        db_sess.add(user)
        db_sess.commit()
        return redirect('/')
    return render_template('registration.html',
                           form=form,
                           title='Регистрация')


@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')


@app.route('/job', methods=['GET', 'POST'])
@login_required
def add_jobs():
    form = JobForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        job = Jobs()
        job.team_leader = form.team_leader.data
        job.job = form.job_title.data
        job.work_size = form.size.data
        job.collaborators = form.collaborators.data
        job.is_finished = form.is_finished.data
        job.start_date = datetime.datetime.now()
        current_user.jobs.append(job)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect("/")
    return render_template('job.html',
                           title='Добавление задачи',
                           form=form,
                           j_or_d='j')


@app.route('/job/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_jobs(id):
    form = JobForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        jobs = db_sess.query(Jobs).filter(Jobs.id == id,
                                          Jobs.team_leader == current_user.id or current_user.id == 1
                                          ).first()
        if jobs:
            form.job_title.data = jobs.job
            form.team_leader.data = jobs.team_leader
            form.size.data = jobs.work_size
            form.collaborators.data = jobs.collaborators
            form.is_finished.data = jobs.is_finished
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        jobs = db_sess.query(Jobs).filter(Jobs.id == id,
                                          Jobs.team_leader == current_user.id or current_user.id == 1
                                          ).first()
        if jobs:
            jobs.job = form.job_title.data
            jobs.team_leader = form.team_leader.data
            jobs.work_size = form.size.data
            jobs.collaborators = form.collaborators.data
            jobs.is_finished = form.is_finished.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('job.html',
                           title='Редактирование новости',
                           form=form,
                           j_or_d='j'
                           )


@app.route('/job_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def job_delete(id):
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).filter(Jobs.id == id,
                                      Jobs.team_leader == current_user.id or current_user.id == 1
                                      ).first()
    if jobs:
        db_sess.delete(jobs)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


@app.route('/departments')
def departments():
    db_sess = db_session.create_session()
    dep = db_sess.query(Department).all()
    return render_template('departments.html',
                           dep=dep)


@app.route('/add_department', methods=['GET', 'POST'])
def add_department():
    form = DepartmentForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        dep = db_sess.query(Department).filter(Department.title == form.title.data).first()
        if dep:
            return render_template('cerate_department.html',
                                   form=form,
                                   message='Department with this name, was created')
        dep = Department()
        dep.title = form.title.data
        dep.chief = form.chief.data
        dep.members = form.members.data
        dep.email = form.email.data
        db_sess.add(dep)
        db_sess.commit()
        return redirect('/departments')
    return render_template('cerate_department.html',
                           form=form)


@app.route('/edit_department/<int:id>', methods=['GET', 'POST'])
def edit_department(id):
    form = DepartmentForm()
    if request.method == 'GET':
        db_sess = db_session.create_session()
        dep = db_sess.query(Department).filter(Department.id == id).first()
        if dep:
            form.title.data = dep.title
            form.chief.data = dep.chief
            form.members.data = dep.members
            form.email.data = dep.email
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        dep = db_sess.query(Department).filter(Department.id == id).first()
        if dep:
            dep.title = form.title.data
            dep.chief = form.chief.data
            dep.members = form.members.data
            dep.email = form.email.data
            db_sess.commit()
            return redirect('/departments')
        else:
            abort(404)
    return render_template('cerate_department.html',
                           form=form)


@app.route('/delete_department/<int:id>', methods=['GET', 'POST'])
def delete_department(id):
    db_sess = db_session.create_session()
    dep = db_sess.query(Department).filter(Department.id == id).first()
    if dep:
        db_sess.delete(dep)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/departments')


@app.route('/galery', methods=['GET', 'POST'])
def galery():
    form = GaleryForm()
    if request.method == 'GET':
        db_sess = db_session.create_session()
        photos_from_base = db_sess.query(Photo).all()
        photos = []
        for i in photos_from_base:
            photos.append(url_for('static', filename='profile_pics/' + current_user.name + '/' + i.photo))
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        photo = Photo()
        if form.photo.data:
            photo_file = save_picture(form.photo.data)
        else:
            return redirect('/galery')
        photo.photo = photo_file
        db_sess.add(photo)
        db_sess.commit()
        return redirect('/galery')
    ln = len(photos_from_base)
    if photos_from_base:
        return render_template('galery.html', photos=photos_from_base, form=form, ln=ln)
    else:
        return render_template('galery.html', form=form,)


@app.route('/carousel')
def carousel():
    return render_template('carousel.html')


@app.route('/load_photo', methods=['GET', 'POST'])
def load_photo():
    form = UserPhotoForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        photo_n = (db_sess.query(User).filter(User.id == current_user.id).first()).photo
        if not photo_n:
            return render_template('load_photo.html', form=form)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.id == current_user.id).first()
        user.photo = save_user_picture(form.photo.data)
        db_sess.commit()
        return redirect('/load_photo')
    photo = url_for('static', filename='img/user_photo/' + current_user.name + '/' + photo_n)
    return render_template('load_photo.html', form=form, photo=photo)


def main():
    db_session.global_init("db/marsian.sqlite")
    app.register_blueprint(jobs_api.blueprint)
    app.run()


if __name__ == '__main__':
    main()