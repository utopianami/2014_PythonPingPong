from flask import Blueprint, request, render_template, session, redirect, url_for, json


mod = Blueprint('rank', __name__, url_prefix='/rank')