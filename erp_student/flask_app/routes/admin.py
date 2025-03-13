from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.student import Student

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        password = request.form['password']
        admin_password = 'oasis69'

        if password == admin_password:
            session['is_admin'] = True
            flash('เข้าสู่ระบบแอดมินสำเร็จ!', 'success')
            return redirect(url_for('admin.admin_dashboard'))
        else:
            flash('รหัสผ่านไม่ถูกต้อง!', 'danger')

    return render_template('admin_login.html')

@admin_bp.route('/admin_dashboard', methods=['GET'])
def admin_dashboard():
    if not session.get('is_admin'):
        flash('คุณต้องเข้าสู่ระบบแอดมินก่อน!', 'danger')
        return redirect(url_for('admin.admin_login'))

    students = Student.query.all()
    return render_template('admin_dashboard.html', students=students)
