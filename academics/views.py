from .models import Student, Department, Subject
from .models import Department, Subject, Teacher, TeacherSubject
from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages


def student_profile(request, student_id):
    student = get_object_or_404(Student, id=student_id)

    return render(request, "accounts/student_profile.html", {
        "student": student,
        "subjects": student.subjects.all()
    })


def create_student_step1(request):
    departments = Department.objects.all()
    semesters = range(1, 9)

    if request.method == "POST":
        department_id = request.POST.get("department")
        semester = request.POST.get("semester")

        # Save to session
        request.session["department_id"] = department_id
        request.session["semester"] = semester

        return redirect("create_student_step2")

    return render(request, "accounts/create_step1.html", {
        "departments": departments,
        "semesters": semesters
    })


def create_student_step2(request):
    department_id = request.session.get("department_id")
    semester = request.session.get("semester")

    if not department_id or not semester:
        messages.error(request, "Please select department and semester first.")
        return redirect("create_student_step1")

    department = Department.objects.get(id=department_id)

    if request.method == "POST":
        enrollment_no = request.POST.get("enrollment_no")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        address = request.POST.get("address")
        dob = request.POST.get("date_of_birth")
        password = request.POST.get("password")
        profile_picture = request.FILES.get("profile_picture")  # 👈 file comes here

        # Check duplicates
        if Student.objects.filter(enrollment_no=enrollment_no).exists():
            messages.error(request, "Enrollment number already exists.")
            return redirect("create_student_step2")
        if Student.objects.filter(email=email).exists() or User.objects.filter(username=email).exists():
            messages.error(request, "Email already exists.")
            return redirect("create_student_step2")

        # Create User
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )

        # Create Student
        student = Student.objects.create(
            enrollment_no=enrollment_no,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            address=address,
            profile_picture=profile_picture,   # 👈 save image
            date_of_birth=datetime.strptime(dob, "%Y-%m-%d").date() if dob else None,
            department=department,
            semester=int(semester)
        )

        # Auto-assign department + semester subjects
        subjects = Subject.objects.filter(department=department, semester=semester)
        student.subjects.set(subjects)

        messages.success(
            request,
            f"Student {first_name} {last_name} registered successfully with {subjects.count()} subjects."
        )
        return redirect("create_student_step1")

    return render(request, "accounts/create_step2.html", {
        "department": department,
        "semester": semester
    })


def create_teacher_step1(request):
    if request.method == "POST":
        dept_id = request.POST.get('department')
        semester = request.POST.get('semester')
        if dept_id and semester:
            # redirect to step2 with query params
            return redirect(f"/academics/create-teacher-step2/?dept={dept_id}&sem={semester}")
        else:
            messages.error(request, "Please select department and semester.")

    departments = Department.objects.all()
    semesters = range(1, 9)
    context = {
        "departments": departments,
        "semesters": semesters
    }
    return render(request, "academics/teacher/teacher_step1.html", context)


# Step 2: Teacher Profile + Subject Selection
from django.shortcuts import render, redirect
from .models import Teacher, TeacherSubject, Subject

DESIGNATION_CHOICES = Teacher.DESIGNATION_CHOICES

def create_teacher_step2(request):
    dept_id = request.GET.get('dept')
    semester = request.GET.get('sem')

    subjects = Subject.objects.filter(department_id=dept_id, semester=semester)

    if request.method == "POST":
        # handle form submission
        employee_id = request.POST['employee_id']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        phone = request.POST.get('phone', '')
        address = request.POST.get('address', '')
        salary = request.POST.get('salary', None)
        designation = request.POST['designation']
        profile_picture = request.FILES.get('profile_picture', None)
        subjects_selected = request.POST.getlist('subjects')  # 👈 important for multiple subjects

        teacher = Teacher.objects.create(
            employee_id=employee_id,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            address=address,
            salary=salary,
            designation=designation,
            profile_picture=profile_picture
        )

        for subj_id in subjects_selected:
            TeacherSubject.objects.create(teacher=teacher, subject_id=subj_id)

        return redirect('teacher_list')  # change to your list page

    context = {
        "dept_id": dept_id,
        "semester": semester,
        "subjects": subjects,
        "designations": DESIGNATION_CHOICES,  # 👈 pass this to template
    }
    return render(request, 'academics/teacher/teacher_step2.html', context)

def teacher_profile(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)
    subjects = TeacherSubject.objects.filter(teacher=teacher)

    context = {
        'teacher': teacher,
        'subjects': subjects,
    }
    return render(request, 'academics/teacher/teacher_profile.html', context)




def teacher_list(request):
    teachers = Teacher.objects.all().order_by('id')
    return render(request, 'academics/teacher/teacher_list.html', {'teachers': teachers})














def computer_engineering(request):
    return render(request, 'academics/computer_engineering.html')

def it_engineering(request):
    return render(request, 'academics/it_engineering.html')

def electrical_engineering(request):
    return render(request, 'academics/electrical_engineering.html')

def ai_ds_engineering(request):
    return render(request, 'academics/ai_ds_engineering.html')

def civil_engineering(request):
    return render(request, 'academics/civil_engineering.html')

def mechanical_engineering(request):
    return render(request, 'academics/mechanical_engineering.html')

def electronics_telecom_engineering(request):
    return render(request, 'academics/electronics_telecom_engineering.html')
