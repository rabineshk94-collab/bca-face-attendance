from django.urls import path
from . import views

urlpatterns = [
    # 1. Public Pages
    path('', views.home_view, name='home'),
    path('about/', views.about_view, name='about'),
    path('contact/', views.contact_view, name='contact'),
    path('toggle-language/', views.toggle_language, name='toggle_language'),

    # 2. Authentication
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # 3. Dashboard
    path('dashboard/', views.dashboard_view, name='dashboard'),

    # 4. Student Management & Digital ID Card (CRUD)
    path('students/', views.student_list_view, name='student_list'),
    path('students/add/', views.student_add_view, name='student_add'),
    path('students/edit/<int:student_id>/', views.student_edit_view, name='student_edit'),
    path('students/delete/<int:student_id>/', views.student_delete_view, name='student_delete'),
    path('students/id-card/<int:student_id>/', views.student_id_card_view, name='student_id_card'),

    # 5. Face Registration
    path('students/register-face/<int:student_id>/', views.face_register_view, name='face_register'),
    path('api/save-face-encoding/', views.api_save_face_encoding, name='api_save_face_encoding'),

    # 6. Live Face Recognition Attendance (Check-In / Check-Out)
    path('live-attendance/', views.live_attendance_view, name='live_attendance'),
    path('api/process-frame/', views.api_process_recognition_frame, name='api_process_frame'),
    path('api/reset-today-attendance/', views.api_reset_today_attendance, name='api_reset_today_attendance'),
    path('api/auto-mark-absent/', views.api_auto_mark_absent, name='api_auto_mark_absent'),

    # 7. Leave Applications & Attendance Corrections
    path('leaves/', views.leave_list_view, name='leave_list'),
    path('leaves/approve/<int:leave_id>/<str:status_code>/', views.leave_approve_view, name='leave_approve'),
    path('api/correct-attendance/', views.api_correct_attendance, name='api_correct_attendance'),

    # 8. Attendance Records & Audit Logs
    path('attendance-history/', views.attendance_history_view, name='attendance_history'),
    path('reports/', views.reports_view, name='reports'),
    path('audit-logs/', views.audit_logs_view, name='audit_logs'),

    # 9. Exports & Backup
    path('export/excel/', views.export_excel_view, name='export_excel'),
    path('export/pdf/', views.export_pdf_view, name='export_pdf'),
    path('export/backup-db/', views.export_backup_db, name='export_backup_db'),

    # 10. Manual Attendance Backup System
    path('manual-backup/', views.manual_backup_view, name='manual_backup'),
    path('api/manual-attendance/', views.api_manual_attendance, name='api_manual_attendance'),

    # Legacy QR fallback route for backwards compatibility
    path('qr-backup/', views.manual_backup_view, name='qr_backup'),
    path('api/qr-attendance/', views.api_manual_attendance, name='api_qr_attendance'),
]
