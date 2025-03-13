from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.student import Student, db, bcrypt

student_bp = Blueprint('student', __name__)

@student_bp.route('/')
def home():
    return render_template('home.html')

@student_bp.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        course = request.form['course']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash('รหัสผ่านและยืนยันรหัสผ่านไม่ตรงกัน', 'danger')
            return redirect(url_for('student.index'))

        password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

        new_student = Student(name=name, email=email, course=course, password_hash=password_hash)
        db.session.add(new_student)
        db.session.commit()

        flash('สมัครเรียนสำเร็จ!', 'success')
        return redirect(url_for('student.success'))

    return render_template('index.html')

@student_bp.route('/checklist')
def checklist():
    students = Student.query.all()
    return render_template('checklist.html', students=students)

@student_bp.route('/success')
def success():
    return render_template('success.html')

@student_bp.route('/update_student', methods=['GET', 'POST'])
def update_student():
    if 'user_id' not in session:
        flash('กรุณาล็อกอินก่อนที่จะเข้าถึงหน้าข้อมูลส่วนตัว', 'danger')
        return redirect(url_for('auth.login'))

    student = Student.query.filter_by(id=session.get('user_id')).first()

    if request.method == 'POST':
        password = request.form['password']

        if not bcrypt.check_password_hash(student.password_hash, password):
            flash('รหัสผ่านไม่ถูกต้อง', 'danger')
            return redirect(url_for('student.update_student'))

        student.name = request.form['name']
        student.email = request.form['email']
        student.course = request.form['course']

        new_password = request.form.get('new_password')
        if new_password:
            password_hash = bcrypt.generate_password_hash(new_password).decode('utf-8')
            student.password_hash = password_hash

        db.session.commit()

        flash('อัปเดตข้อมูลสำเร็จ!', 'success')
        return redirect(url_for('student.profile'))

    return render_template('update_student.html', student=student)

@student_bp.route('/profile')
def profile():
    # ตรวจสอบการเข้าสู่ระบบ
    if 'user_id' not in session:
        flash('กรุณาล็อกอินก่อนที่จะเข้าถึงหน้าข้อมูลส่วนตัว', 'danger')
        return redirect(url_for('login'))  # ถ้ายังไม่ได้ล็อกอิน ให้ไปที่หน้า login

    student = Student.query.filter_by(id=session.get('user_id')).first()
    return render_template('profile.html', student=student)


@student_bp.route('/about')
def about():
    return render_template('about.html')


@student_bp.route('/contact') 
def contact():
    return render_template('contact.html')   


@student_bp.route('/delete/<int:student_id>', methods=['GET'])
def delete_student(student_id):
    student = Student.query.get(student_id)
    if student:
        db.session.delete(student)
        db.session.commit()
        flash('ลบข้อมูลสำเร็จ!', 'success')

    return redirect(url_for('student.checklist'))  # แก้ให้ใช้ Blueprint


@student_bp.route('/edit/<int:student_id>', methods=['GET', 'POST'])
def edit_student(student_id):
    student = Student.query.get(student_id)

    if request.method == 'POST':
        student.name = request.form['name']
        student.email = request.form['email']
        student.course = request.form['course']
        db.session.commit()

        flash('อัปเดตข้อมูลสำเร็จ!', 'success')
        return redirect(url_for('student.checklist'))  # ใช้ Blueprint

    return render_template('edit_student.html', student=student)