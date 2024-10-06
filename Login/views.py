from django.shortcuts import render, redirect 
from django.http import JsonResponse
from .form import TeacherForm ,AdminSignupForm,StudentForm,AdminLoginForm,StudentLoginForm,TeacherLoginForm,AdminUserForm
from assignStudentToTeacher.models import StudentTeacherAssignment
from assignClassToTeacher.models import ClassAssignment
from TeacherRegistration.models import Teacher
from django.contrib import messages
from .models import Admin
from StudentRegistration.models import Student
from django.contrib.auth.models import User  # Django's built-in user model

# Create your views here.
def signup_view(request):
    if request.method == 'POST':
        form = AdminSignupForm(request.POST)
        if form.is_valid():
            form.save()  # Saves the form data to the database

            response = {"success": True, "data": "True", "message": "Admin signed up successfully "}
            return JsonResponse(response)
    else:
        form = AdminSignupForm()

    return render(request, 'login/signup.html', {'form': form})


def admin_login_view(request):
    context={}
    if request.method == 'POST':
        form = AdminLoginForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            email = form.cleaned_data.get('email')

            # Check if an admin exists with the provided name and email
            try:
                admin_user = Admin.objects.get(name=name, email=email)
                # Store admin_user in session
                request.session['admin_user_id'] = admin_user.id
                # Redirect to dashboard if successful login
                return redirect('admin_dashboard')
            except Admin.DoesNotExist:
                messages.error(request, "Invalid credentials")
    else:
        form = AdminLoginForm()

    return render(request, 'login/login_admin.html', {'form': form})
    
def admin_dashboard(request):
    # Get the admin user from the session
    admin_user_id = request.session.get('admin_user_id')
    
    if admin_user_id:
        try:
            admin_user = Admin.objects.get(id=admin_user_id)
        except Admin.DoesNotExist:
            admin_user = None
    else:
        admin_user = None

    # Pass the admin_user to the dashboard template
    return render(request, 'login/admin_dashboard.html', {'admin_user': admin_user})

def student_login_view(request):
    if request.method == 'POST':
        form = StudentLoginForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            email = form.cleaned_data.get('email')

            # Check if an admin exists with the provided name and email
            try:
                student_user = Student.objects.get(name=name, email=email)
                # Store admin_user in session
                request.session['student_user_id'] = student_user.id
                # Redirect to dashboard if successful login
                return redirect('student_dashboard')
            except Student.DoesNotExist:
                messages.error(request, "Invalid credentials")
    else:
        form = StudentLoginForm()

    return render(request, 'login/login_student.html', {'form': form})

    
def student_dashboard(request):
    # Get the admin user from the session
    student_user_id = request.session.get('student_user_id')
    
    if student_user_id:
        try:
            student_user = Student.objects.get(id=student_user_id)
             # Get all the assignments for this student
            assignments = StudentTeacherAssignment.objects.filter(assigned_student=student_user)

            # Extract the teachers from the assignments
            assigned_teachers = [assignment.teacher for assignment in assignments]

            print("student id: ",student_user)
            print("Assigned Teachers: ", assigned_teachers)
        except Student.DoesNotExist:
            student_user = None
            assigned_teachers = None
    else:
        student_user = None
        assigned_teachers = None

    # Pass the admin_user to the dashboard template
    return render(request, 'login/student_dashboard.html', {'student_user': student_user,'assigned_teachers': assigned_teachers,})  


def teacher_login_view(request):
    if request.method == 'POST':
        form = TeacherLoginForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            email = form.cleaned_data.get('email')

            # Check if an admin exists with the provided name and email
            try:
                teacher_user = Teacher.objects.get(name=name, email=email)
                # Store admin_user in session
                request.session['teacher_user_id'] = teacher_user.id
                # Redirect to dashboard if successful login
                return redirect('teacher_dashboard')
            except Teacher.DoesNotExist:
                messages.error(request, "Invalid credentials")
    else:
        form = TeacherLoginForm()

    return render(request, 'login/login_teacher.html', {'form': form})

    
def teacher_dashboard(request):
    # Get the admin user from the session
    teacher_user_id = request.session.get('teacher_user_id')
    
    if teacher_user_id:
        try:
            teacher_user = Teacher.objects.get(id=teacher_user_id)
            
            student_assignments = StudentTeacherAssignment.objects.filter(teacher=teacher_user)
            
            # Extract the students from the assignments
            assigned_students = [assignment.assigned_student for assignment in student_assignments]

            # Get all the class assignments for this teacher
            class_assignments = ClassAssignment.objects.filter(teacher=teacher_user)
            
            # Extract the classes from the assignments
            assigned_classes = [assignment.assigned_class for assignment in class_assignments]

            print("Teacher ID: ", teacher_user)
            print("Assigned Students: ", assigned_students)
            print("Assigned Classes: ", assigned_classes)
        except Teacher.DoesNotExist:
            teacher_user = None
            assigned_students = None
            assigned_classes=None
    else:
        teacher_user = None
        assigned_students = None
        assigned_classes=None

    # Pass the admin_user to the dashboard template
    return render(request, 'login/teacher_dashboard.html', {'teacher_user': teacher_user,'assigned_students': assigned_students,'assigned_classes':assigned_classes,})  



def custom_admin_user_form(request):
    if request.method == 'POST':
        form = AdminUserForm(request.POST)
        if form.is_valid():
            # Save the form data to the database
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            
            # Save to the database (adjust to your needs)
            admin_user = Admin(name=name, email=email)
            admin_user.save()
            
            # Success message
            messages.success(request, "Admin user saved successfully!")
            return redirect('/admin/')  # Redirect to the admin home page
    else:
        form = AdminUserForm()

    return render(request, 'admin/custom_admin_form.html', {'form': form})
