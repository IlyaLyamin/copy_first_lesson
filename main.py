from flask import Flask, redirect, render_template, request, abort, jsonify
from data import db_session
from flask_login import LoginManager, login_user, login_required, current_user
from data.users import User
from forms.login import LoginForm
from forms.job_form import JobForm
from data.jobs import Jobs
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
    return render_template("index.html", jobs=jobs, title="Главная")


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
    return render_template('login.html', title='Авторизация', form=form)


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
    return render_template('job.html', title='Добавление задачи',
                           form=form)


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
                           form=form
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


def main():
    db_session.global_init("db/marsian.sqlite")
    app.register_blueprint(jobs_api.blueprint)
    app.run()


if __name__ == '__main__':
    main()