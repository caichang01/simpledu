from flask import Blueprint
from flask import render_template
from simpledu.models import Course

course = Blueprint('course', __name__, url_prefix='/courses')

@course.route('/<int:course_id>')
def detail(course_id):
    course = Course.query.get_or_404(course_id)
    return render_template('course/detail.html', course=course)
