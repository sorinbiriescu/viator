from flask import Blueprint, render_template

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('/main/index.html')

@main.route('/location')
def location():
    return render_template('/main/location.html')

@main.route('/attraction')
def attraction():
    return render_template('/main/attraction.html')

@main.route('/route')
def route():
    return render_template('/main/route.html')