from django.contrib import admin
from .models import UserProfile, Department, Teacher, Subject, Student, FaceEncoding, Attendance, LeaveRequest, ActivityLog

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'preferred_language')
    list_filter = ('role', 'preferred_language')

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'created_at')
    search_fields = ('name', 'code')

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('staff_id', 'name', 'department', 'designation', 'email')
    search_fields = ('name', 'staff_id', 'email')

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'department', 'semester')
    list_filter = ('department', 'semester')

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('roll_number', 'name', 'department', 'year', 'email', 'phone', 'created_at')
    list_filter = ('department', 'year')
    search_fields = ('name', 'roll_number', 'student_id', 'email')

@admin.register(FaceEncoding)
class FaceEncodingAdmin(admin.ModelAdmin):
    list_display = ('student', 'image_path', 'created_at')
    search_fields = ('student__name', 'student__roll_number')

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'department', 'date', 'time_in', 'time_out', 'status', 'is_late', 'confidence_score', 'method')
    list_filter = ('date', 'department', 'status', 'is_late', 'method')
    search_fields = ('student__name', 'student__roll_number')

@admin.register(LeaveRequest)
class LeaveRequestAdmin(admin.ModelAdmin):
    list_display = ('student', 'start_date', 'end_date', 'status', 'created_at')
    list_filter = ('status', 'start_date')

@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'user', 'action', 'ip_address')
    search_fields = ('action', 'user__username')
