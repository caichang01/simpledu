from flask import Blueprint, render_template, request, current_app, redirect, url_for, flash
from simpledu.decorators import admin_required
from simpledu.models import Course
from simpledu.forms import CourseForm, db

admin = Blueprint('admin', __name__, url_prefix='/admin')


@admin.route('/')
@admin_required
def index():
    return render_template('admin/index.html')


@admin.route('/courses')
@admin_required
def courses():
    page = request.args.get('page', default=1, type=int)
    pagination = Course.query.paginate(
        page=page,
        per_page=current_app.config['ADMIN_PER_PAGE'],
        error_out=False
    )
    return render_template('admin/courses.html', pagination=pagination)


@admin.route('/courses/create', methods=['GET', 'POST'])
@admin_required
def create_course():
    form = CourseForm()
    if form.validate_on_submit():
        form.create_course()
        flash('课程已成功创建！', 'success')
        return redirect(url_for('admin.courses'))
    return render_template('admin/create_courses.html', form=form)


@admin.route('/courses/<int:course_id>/update', methods=['GET', 'POST'])
@admin_required
def update_course(course_id):
    course = Course.query.get_or_404(course_id)
    form = CourseForm(obj=course)
    if form.validate_on_submit():
        form.update_course(course)
        flash('课程已成功更新！', 'success')
        return redirect(url_for('admin.courses'))
    return render_template('admin/update_courses.html', form=form, course=course)


@admin.route('/courses/<int:course_id>/delete')
@admin_required
def delete_course(course_id):
    course = Course.query.get_or_404(course_id)
    db.session.delete(course)
    db.session.commit()
    flash('课程已成功删除！', 'success')
    return redirect(url_for('admin.courses'))
