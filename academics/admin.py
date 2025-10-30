from django.contrib import admin
from .models import Student, Marks, Subject, Attendance, Department,Teacher,TeacherSubject

# -----------------------------
# Custom Semester Filter
# -----------------------------
class SemesterListFilter(admin.SimpleListFilter):
    title = 'Semester'
    parameter_name = 'semester'

    def lookups(self, request, model_admin):
        return [(i, f"Semester {i}") for i in range(1, 9)]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(semester=self.value())
        return queryset


# -----------------------------
# Admin for Subject
# -----------------------------
@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'semester', 'department')
    list_filter = ('department', SemesterListFilter)
    search_fields = ('name',)
    ordering = ('department', 'semester', 'name')


# -----------------------------
# Admin for Department
# -----------------------------
@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')
    search_fields = ('code', 'name')


@admin.register(Marks)
class MarksAdmin(admin.ModelAdmin):
    list_display = ("student", "subject", "marks_obtained", "max_marks")

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "subject":
            if request.GET.get("student"):  # if student is chosen in admin URL
                try:
                    student_id = request.GET.get("student")
                    student = Student.objects.get(id=student_id)
                    kwargs["queryset"] = Subject.objects.filter(
                        department=student.department,
                        semester=student.semester
                    )
                except Student.DoesNotExist:
                    pass
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

# -----------------------------
# Register remaining models
# -----------------------------
admin.site.register(Student)

admin.site.register(Attendance)

admin.site.register(Teacher)
admin.site.register(TeacherSubject)