from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.student import Student, db, bcrypt

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        student = Student.query.filter_by(email=email).first()

        if student and bcrypt.check_password_hash(student.password_hash, password):
            session['user_id'] = student.id
            flash('เข้าสู่ระบบสำเร็จ!', 'success')
            return redirect(url_for('student.update_student'))
        else:
            flash('อีเมลหรือรหัสผ่านไม่ถูกต้อง', 'danger')

    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.pop('is_admin', None)
    session.pop('user_id', None)
    flash('ออกจากระบบแล้ว', 'success')
    return redirect(url_for('student.home'))
