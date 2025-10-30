from django.db import models
from django.db.models import Avg, Count, Q


# ---------------- Department ----------------
class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return f"{self.code} - {self.name}"


# ---------------- Subject ----------------
class Subject(models.Model):
    SEMESTER_CHOICES = [(i, f"Semester {i}") for i in range(1, 9)]

    name = models.CharField(max_length=100)
    semester = models.IntegerField(choices=SEMESTER_CHOICES)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="subjects")

    def __str__(self):
        return f"{self.name} (Sem {self.semester}, {self.department.code})"


# ---------------- Student ----------------
class Student(models.Model):
    SEMESTER_CHOICES = [(i, f"Semester {i}") for i in range(1, 9)]

    enrollment_no = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to="students/profile_pics/", blank=True, null=True)

    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="students")
    semester = models.IntegerField(choices=SEMESTER_CHOICES)
    subjects = models.ManyToManyField("Subject", related_name="students")  # 👈 this is needed

    date_of_birth = models.DateField(blank=True, null=True)
    date_joined = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.enrollment_no} - {self.first_name} {self.last_name}"



# ---------------- Marks ----------------
class Marks(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="marks")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="marks")
    marks_obtained = models.DecimalField(max_digits=5, decimal_places=2)
    max_marks = models.DecimalField(max_digits=5, decimal_places=2, default=100)

    class Meta:
        unique_together = ('student', 'subject')  # One marks entry per student per subject

    def __str__(self):
        return f"{self.student.enrollment_no} - {self.subject.name}: {self.marks_obtained}/{self.max_marks}"


# ---------------- Attendance ----------------
class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="attendance")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="attendance")
    date = models.DateField()
    status = models.BooleanField(default=True)  # True = Present, False = Absent

    class Meta:
        unique_together = ('student', 'subject', 'date')

    def __str__(self):
        status = "Present" if self.status else "Absent"
        return f"{self.student.enrollment_no} - {self.subject.name} ({self.date}): {status}"




# ---------------- Teacher ----------------
class Teacher(models.Model):
    DESIGNATION_CHOICES = [
        ('HOD', 'Head of Department'),
        ('PROF', 'Professor'),
        ('ASS_PROF', 'Assistant Professor'),
        ('LECT', 'Lecturer'),
    ]

    employee_id = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to="teachers/profile_pics/", blank=True, null=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    designation = models.CharField(max_length=20, choices=DESIGNATION_CHOICES)
    date_joined = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.employee_id} - {self.first_name} {self.last_name}"


# ---------------- TeacherSubject ----------------
class TeacherSubject(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name="subjects")
    subject = models.ForeignKey("Subject", on_delete=models.CASCADE, related_name="teachers")

    def __str__(self):
        return f"{self.teacher} - {self.subject.name}"

    @property
    def average_marks(self) -> float:
        """
        Returns the average marks of all students for this subject.
        Rounded to 2 decimal places. Returns 0 if no marks exist.
        """
        result = self.subject.marks.aggregate(avg=Avg('marks_obtained'))
        return round(result['avg'] or 0, 2)

    @property
    def average_attendance(self) -> float:
        """
        Returns the average attendance percentage for this subject.
        Calculated as (total days present / total attendance entries) * 100.
        Rounded to 2 decimal places. Returns 0 if no attendance records exist.
        """
        attendance_data = self.subject.attendance.aggregate(
            total=Count('id'),
            present=Count('id', filter=Q(status=True))
        )
        if attendance_data['total'] == 0:
            return 0
        return round((attendance_data['present'] / attendance_data['total']) * 100, 2)
