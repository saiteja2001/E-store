from flask import Blueprint,render_template,request,redirect,url_for
from flask.helpers import flash
from .auth import login_flag

views = Blueprint('views',__name__)


