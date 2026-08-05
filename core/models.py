from django.db import models
from django.contrib.auth.models import User
import json

class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('ADMIN', 'Administrator'),
        ('TEACHER', 'Teacher / Faculty'),
        ('STUDENT', 'Student'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='STUDENT')
    phone = models.CharField(max_length=20, blank=True, null=True)
    preferred_language = models.CharField(max_length=10, default='EN') # 'EN' or 'TA'

    def __str__(self):
        return f"{self.user.username} ({self.role})"

class Department(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.code})"

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher_profile', null=True, blank=True)
    staff_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=150)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='teachers')
    designation = models.CharField(max_length=100, default='Assistant Professor')
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.staff_id})"

class Subject(models.Model):
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=150)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='subjects')
    semester = models.CharField(max_length=20, default='Semester 6')

    def __str__(self):
        return f"{self.code} - {self.name}"

class Student(models.Model):
    YEAR_CHOICES = [
        ('1st Year', '1st Year'),
        ('2nd Year', '2nd Year'),
        ('3rd Year / Final Year', '3rd Year / Final Year'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile', null=True, blank=True)
    student_id = models.CharField(max_length=50, unique=True)
    roll_number = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=150)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='students')
    year = models.CharField(max_length=30, choices=YEAR_CHOICES, default='3rd Year / Final Year')
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    photo = models.ImageField(upload_to='student_photos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.roll_number})"

    def attendance_percentage(self):
        total = Attendance.objects.filter(student=self).count()
        if total == 0:
            return 100.0
        present = Attendance.objects.filter(student=self, status__in=['Present', 'Late']).count()
        return round((present / total) * 100, 1)

class FaceEncoding(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='encodings')
    image_path = models.CharField(max_length=255, blank=True, null=True)
    encoding_json = models.TextField() # Stores JSON representation of 128D encoding array
    created_at = models.DateTimeField(auto_now_add=True)

    def get_encoding(self):
        try:
            return json.loads(self.encoding_json)
        except Exception:
            return []

    def set_encoding(self, encoding_list):
        self.encoding_json = json.dumps(encoding_list)

    def __str__(self):
        return f"Encoding for {self.student.name} ({self.id})"

class Attendance(models.Model):
    STATUS_CHOICES = [
        ('Present', 'Present'),
        ('Absent', 'Absent'),
        ('Late', 'Late'),
        ('On Leave', 'On Leave'),
    ]

    METHOD_CHOICES = [
        ('Face Recognition', 'Face Recognition'),
        ('QR Backup', 'QR Backup'),
        ('Manual', 'Manual'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendances')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='attendances')
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, blank=True, related_name='attendances')
    date = models.DateField()
    time_in = models.TimeField(auto_now_add=True)
    time_out = models.TimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Present')
    is_late = models.BooleanField(default=False)
    confidence_score = models.FloatField(default=98.5)
    method = models.CharField(max_length=30, choices=METHOD_CHOICES, default='Face Recognition')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'date')

    def __str__(self):
        return f"{self.student.name} - {self.date} ({self.status})"

class LeaveRequest(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='leave_requests')
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Leave for {self.student.name} ({self.status})"

class ActivityLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=255)
    ip_address = models.CharField(max_length=50, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.timestamp} - {self.action}"
