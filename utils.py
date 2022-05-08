import secrets
import os
from flask_login import current_user
from flask import current_app
from PIL import Image


def save_picture(form_picture):
    random_hex = secrets.token_hex(16)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    road_for_path = os.path.join(current_app.root_path, 'static', 'img', 'profile_pics')
    if not os.path.isdir(road_for_path):
        os.makedirs(road_for_path)
    picture_path = os.path.join(road_for_path, picture_fn)
    i = Image.open(form_picture)
    i.save(picture_path)
    return picture_fn


def save_user_picture(form_picture):
    random_hex = secrets.token_hex(16)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    road_for_path = os.path.join(current_app.root_path, 'static', 'img', 'user_photo', current_user.name)
    if not os.path.isdir(road_for_path):
        os.makedirs(road_for_path)
    picture_path = os.path.join(road_for_path, picture_fn)
    i = Image.open(form_picture)
    i.save(picture_path)
    return picture_fn