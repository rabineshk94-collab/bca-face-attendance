import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bca_project.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import UserProfile, Department, Student, Attendance, FaceEncoding
from django.utils import timezone

def seed():
    print("--- Initializing BCA Project Database & Seeding Sample Data ---")

    # 1. Create Admin User & UserProfile
    admin_user, created = User.objects.get_or_create(username='admin', defaults={'email': 'admin@bca.edu', 'is_staff': True, 'is_superuser': True})
    if created:
        admin_user.set_password('admin123')
        admin_user.save()
        print("[OK] Admin superuser created: admin / admin123")
    else:
        print("[OK] Admin superuser already exists.")

    prof, _ = UserProfile.objects.get_or_create(user=admin_user)
    prof.role = 'ADMIN'
    prof.save()

    # 2. Create Departments
    bca, _ = Department.objects.get_or_create(name='Bachelor of Computer Applications', code='BCA')
    bsc_cs, _ = Department.objects.get_or_create(name='B.Sc Computer Science', code='B.Sc CS')
    btech, _ = Department.objects.get_or_create(name='B.Tech Computer Science & Eng.', code='B.Tech CSE')
    print("[OK] Departments initialized (BCA, B.Sc CS, B.Tech CSE).")

    # 3. Create Sample Students
    sample_students = [
        {'id': 'BCA2026001', 'roll': '2026-BCA-001', 'name': 'Aarav Sharma', 'dept': bca, 'year': '3rd Year / Final Year', 'email': 'aarav.sharma@bca.edu', 'phone': '+91 9876543210'},
        {'id': 'BCA2026002', 'roll': '2026-BCA-002', 'name': 'Priya Patel', 'dept': bca, 'year': '3rd Year / Final Year', 'email': 'priya.patel@bca.edu', 'phone': '+91 9876543211'},
        {'id': 'CS2026015', 'roll': '2026-CS-015', 'name': 'Rohan Verma', 'dept': bsc_cs, 'year': '2nd Year', 'email': 'rohan.v@bca.edu', 'phone': '+91 9876543212'},
        {'id': 'CSE2026033', 'roll': '2026-CSE-033', 'name': 'Ananya Sen', 'dept': btech, 'year': '3rd Year / Final Year', 'email': 'ananya.sen@bca.edu', 'phone': '+91 9876543213'},
        {'id': 'BCA2026045', 'roll': '2026-BCA-045', 'name': 'Vikram Reddy', 'dept': bca, 'year': '1st Year', 'email': 'vikram.r@bca.edu', 'phone': '+91 9876543214'},
    ]

    students_objs = []
    for sdata in sample_students:
        st, created = Student.objects.get_or_create(
            roll_number=sdata['roll'],
            defaults={
                'student_id': sdata['id'],
                'name': sdata['name'],
                'department': sdata['dept'],
                'year': sdata['year'],
                'email': sdata['email'],
                'phone': sdata['phone']
            }
        )
        students_objs.append(st)

        if not FaceEncoding.objects.filter(student=st).exists():
            enc = FaceEncoding(student=st)
            enc.set_encoding([(0.1 * i) % 1.0 for i in range(128)])
            enc.save()

    print(f"[OK] {len(students_objs)} sample students and face encodings initialized.")

    # 4. Create Sample Attendance Logs for Today
    today = timezone.now().date()
    for st in students_objs[:4]:
        Attendance.objects.get_or_create(
            student=st,
            date=today,
            defaults={
                'department': st.department,
                'status': 'Present',
                'confidence_score': 98.4,
                'method': 'Face Recognition'
            }
        )
    print("[OK] Daily attendance records seeded.")
    print("--- Database Setup Complete! ---")

if __name__ == '__main__':
    seed()
