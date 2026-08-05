import json
import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse, FileResponse
from django.db.models import Count, Q
from django.utils import timezone
from .models import UserProfile, Department, Teacher, Subject, Student, FaceEncoding, Attendance, LeaveRequest, ActivityLog
from .face_engine import face_engine
import csv
import os
from django.conf import settings

def get_user_profile(user):
    profile, created = UserProfile.objects.get_or_create(user=user)
    if created and (user.is_superuser or user.is_staff):
        profile.role = 'ADMIN'
        profile.save()
    elif user.is_superuser or user.is_staff:
        if profile.role != 'ADMIN':
            profile.role = 'ADMIN'
            profile.save()
    return profile

def log_activity(user, action, request=None):
    ip = None
    if request:
        ip = request.META.get('REMOTE_ADDR')
    ActivityLog.objects.create(user=user if user and user.is_authenticated else None, action=action, ip_address=ip)

# --- 1. HOME, ABOUT, CONTACT & LANGUAGE TOGGLE ---
def home_view(request):
    return render(request, 'home.html')

def about_view(request):
    return render(request, 'about.html')

def contact_view(request):
    if request.method == 'POST':
        messages.success(request, "Thank you! Your message has been sent successfully.")
        return redirect('contact')
    return render(request, 'contact.html')

def toggle_language(request):
    lang = request.GET.get('lang', 'EN')
    request.session['django_language'] = lang
    if request.user.is_authenticated:
        prof = get_user_profile(request.user)
        prof.preferred_language = lang
        prof.save()
    return redirect(request.META.get('HTTP_REFERER', '/'))

# --- 2. AUTHENTICATION (LOGIN / LOGOUT) ---
def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        u = request.POST.get('username')
        p = request.POST.get('password')
        user = authenticate(request, username=u, password=p)
        if user is not None:
            login(request, user)
            log_activity(user, f"User {user.username} logged in", request)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'login.html')

@login_required
def logout_view(request):
    log_activity(request.user, f"User {request.user.username} logged out", request)
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('login')

# --- 3. DASHBOARD ---
@login_required
def dashboard_view(request):
    today = timezone.now().date()
    total_students = Student.objects.count()
    total_departments = Department.objects.count()
    today_attendances = Attendance.objects.filter(date=today)
    today_present = today_attendances.filter(status__in=['Present', 'Late']).count()
    today_absent = today_attendances.filter(status='Absent').count()

    profile = get_user_profile(request.user)
    
    dept_stats = []
    departments = Department.objects.all()
    for d in departments:
        d_students = Student.objects.filter(department=d).count()
        d_present = Attendance.objects.filter(date=today, department=d, status__in=['Present', 'Late']).count()
        rate = round((d_present / d_students * 100), 1) if d_students > 0 else 0
        dept_stats.append({
            'name': d.name,
            'code': d.code,
            'students': d_students,
            'present': d_present,
            'rate': rate
        })

    recent_logs = today_attendances.select_related('student', 'department').order_by('-time_in')[:6]
    pending_leaves = LeaveRequest.objects.filter(status='PENDING').count()

    context = {
        'role': profile.role,
        'total_students': total_students,
        'total_departments': total_departments,
        'today_present': today_present,
        'today_absent': today_absent,
        'dept_stats': dept_stats,
        'recent_logs': recent_logs,
        'pending_leaves': pending_leaves,
        'today_date': today.strftime('%Y-%m-%d'),
    }
    return render(request, 'dashboard.html', context)

# --- 4. STUDENT MANAGEMENT (CRUD) & DIGITAL ID CARD ---
@login_required
def student_list_view(request):
    query = request.GET.get('q', '')
    dept_filter = request.GET.get('dept', '')

    students = Student.objects.select_related('department').all()

    if query:
        students = students.filter(
            Q(name__icontains=query) | Q(roll_number__icontains=query) | Q(student_id__icontains=query)
        )
    if dept_filter and dept_filter != 'ALL':
        students = students.filter(department__id=dept_filter)

    departments = Department.objects.all()

    context = {
        'students': students,
        'departments': departments,
        'query': query,
        'selected_dept': dept_filter,
    }
    return render(request, 'students/list.html', context)

@login_required
def student_add_view(request):
    departments = Department.objects.all()
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        roll_number = request.POST.get('roll_number')
        name = request.POST.get('name')
        dept_id = request.POST.get('department')
        year = request.POST.get('year')
        email = request.POST.get('email')
        phone = request.POST.get('phone')

        if Student.objects.filter(roll_number=roll_number).exists():
            messages.error(request, f"Student with Roll Number '{roll_number}' already exists.")
        else:
            dept = get_object_or_404(Department, id=dept_id)
            student = Student.objects.create(
                student_id=student_id,
                roll_number=roll_number,
                name=name,
                department=dept,
                year=year,
                email=email,
                phone=phone
            )
            log_activity(request.user, f"Added student {name} ({roll_number})", request)
            messages.success(request, f"Student '{student.name}' added successfully! Now register facial encodings.")
            return redirect('face_register', student_id=student.id)

    return render(request, 'students/form.html', {'departments': departments, 'action': 'Add'})

@login_required
def student_edit_view(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    departments = Department.objects.all()

    if request.method == 'POST':
        student.name = request.POST.get('name')
        dept_id = request.POST.get('department')
        student.department = get_object_or_404(Department, id=dept_id)
        student.year = request.POST.get('year')
        student.email = request.POST.get('email')
        student.phone = request.POST.get('phone')
        student.save()
        log_activity(request.user, f"Updated student profile for {student.name}", request)
        messages.success(request, f"Student details for '{student.name}' updated.")
        return redirect('student_list')

    context = {
        'student': student,
        'departments': departments,
        'action': 'Edit'
    }
    return render(request, 'students/form.html', context)

@login_required
def student_delete_view(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    name = student.name
    student.delete()
    log_activity(request.user, f"Deleted student profile for {name}", request)
    messages.success(request, f"Student '{name}' deleted.")
    return redirect('student_list')

@login_required
def student_id_card_view(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    return render(request, 'students/id_card.html', {'student': student})

# --- 5. FACE REGISTRATION ---
@login_required
def face_register_view(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    encodings_count = FaceEncoding.objects.filter(student=student).count()
    context = {
        'student': student,
        'encodings_count': encodings_count
    }
    return render(request, 'face_register.html', context)

@login_required
def api_save_face_encoding(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            student_id = data.get('student_id')
            image_data = data.get('image_data')

            student = get_object_or_404(Student, id=student_id)
            frame = face_engine.decode_base64_image(image_data)

            faces = face_engine.detect_faces(frame)
            if len(faces) == 0:
                return JsonResponse({'success': False, 'message': 'No face detected in frame. Align face clearly.'})

            descriptor = face_engine.extract_descriptor(frame, faces[0])
            if descriptor is None:
                return JsonResponse({'success': False, 'message': 'Failed to extract face descriptor.'})

            enc = FaceEncoding(student=student)
            enc.set_encoding(descriptor)
            enc.save()

            total_count = FaceEncoding.objects.filter(student=student).count()
            log_activity(request.user, f"Saved face encoding #{total_count} for {student.name}", request)
            return JsonResponse({'success': True, 'message': f'Face sample #{total_count} saved successfully!', 'count': total_count})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

    return JsonResponse({'success': False, 'message': 'Invalid request method.'})

# --- 6. LIVE FACE RECOGNITION ---
@login_required
def live_attendance_view(request):
    departments = Department.objects.all()
    subjects = Subject.objects.all()
    students = Student.objects.all()
    today_date = timezone.now().date()
    tomorrow_date = today_date + datetime.timedelta(days=1)
    
    context = {
        'departments': departments,
        'subjects': subjects,
        'students': students,
        'today_date': today_date.strftime('%Y-%m-%d'),
        'tomorrow_date': tomorrow_date.strftime('%Y-%m-%d')
    }
    return render(request, 'live_attendance.html', context)

@login_required
def api_process_recognition_frame(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            image_data = data.get('image_data')
            mode = data.get('mode', 'CHECKIN')
            target_date_str = data.get('target_date')

            if target_date_str:
                try:
                    target_date = datetime.datetime.strptime(target_date_str, '%Y-%m-%d').date()
                except ValueError:
                    target_date = timezone.now().date()
            else:
                target_date = timezone.now().date()

            frame = face_engine.decode_base64_image(image_data)
            if frame is None:
                return JsonResponse({'success': False, 'message': 'Invalid frame data.'})

            faces = face_engine.detect_faces(frame)
            if len(faces) == 0:
                return JsonResponse({'success': True, 'detected': False, 'message': 'Searching for faces...'})

            x, y, w, h = faces[0]
            face_roi = frame[y:y+h, x:x+w]

            # Anti-spoofing check
            is_real, anti_spoof_msg = face_engine.check_anti_spoofing(face_roi)
            if not is_real:
                return JsonResponse({
                    'success': True,
                    'detected': True,
                    'recognized': False,
                    'spoof_alert': True,
                    'message': 'SPOOF WARNING: Photo / Display Screen Detected!',
                    'box': {'x': int(x), 'y': int(y), 'w': int(w), 'h': int(h)}
                })

            descriptor = face_engine.extract_descriptor(frame, (x, y, w, h))

            all_encodings = FaceEncoding.objects.select_related('student', 'student__department').all()
            
            student_scores = {}
            for enc_model in all_encodings:
                stored_descriptor = enc_model.get_encoding()
                is_match, score = face_engine.compare_encodings(descriptor, stored_descriptor)
                if score >= 65.0:
                    st_id = enc_model.student.id
                    if st_id not in student_scores:
                        student_scores[st_id] = {'student': enc_model.student, 'scores': []}
                    student_scores[st_id]['scores'].append(score)

            ranked_students = []
            for st_id, data in student_scores.items():
                max_s = max(data['scores'])
                avg_s = sum(data['scores']) / len(data['scores'])
                composite = (max_s * 0.6) + (avg_s * 0.4)
                ranked_students.append((composite, max_s, data['student']))

            ranked_students.sort(key=lambda x: x[0], reverse=True)

            best_student = None
            best_score = 0.0

            if len(ranked_students) > 0:
                top_composite, top_max, top_student = ranked_students[0]

                if len(ranked_students) > 1:
                    second_composite, second_max, second_student = ranked_students[1]
                    margin = top_composite - second_composite
                    if margin >= 3.5 and top_composite >= 68.0:
                        best_student = top_student
                        best_score = top_composite
                    else:
                        best_student = None
                        best_score = 0.0
                else:
                    if top_composite >= 68.0:
                        best_student = top_student
                        best_score = top_composite

            now_time = timezone.now().time()

            if best_student and best_score >= 68.0:
                existing_att = Attendance.objects.filter(student=best_student, date=target_date).first()

                if existing_att:
                    if mode == 'CHECKOUT':
                        existing_att.time_out = now_time
                        existing_att.save()
                        status_msg = f"Check-Out Logged at {now_time.strftime('%H:%M:%S')} on Date: {target_date}"
                    else:
                        status_msg = f"Already Marked for Date ({target_date}) at {existing_att.time_in.strftime('%H:%M:%S')}"
                    created = False
                    att = existing_att
                else:
                    is_late_flag = now_time > datetime.time(9, 30)
                    att = Attendance.objects.create(
                        student=best_student,
                        department=best_student.department,
                        date=target_date,
                        status='Late' if is_late_flag else 'Present',
                        is_late=is_late_flag,
                        confidence_score=round(best_score, 1),
                        method='Face Recognition'
                    )
                    created = True
                    status_msg = f"Attendance Marked: {att.status} on Date: {target_date} at {att.time_in.strftime('%H:%M:%S')}"

                return JsonResponse({
                    'success': True,
                    'detected': True,
                    'recognized': True,
                    'student_name': best_student.name,
                    'roll_number': best_student.roll_number,
                    'department': best_student.department.name,
                    'confidence': f"{round(best_score, 1)}%",
                    'status': status_msg,
                    'is_new': created,
                    'date': target_date.strftime('%Y-%m-%d'),
                    'box': {'x': int(x), 'y': int(y), 'w': int(w), 'h': int(h)}
                })
            else:
                # Unregistered / Unmatched Face
                return JsonResponse({
                    'success': True,
                    'detected': True,
                    'recognized': False,
                    'student_name': 'Unregistered Person',
                    'confidence': '0.0%',
                    'message': 'Face Not Registered in Database',
                    'box': {'x': int(x), 'y': int(y), 'w': int(w), 'h': int(h)}
                })

        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

    return JsonResponse({'success': False, 'message': 'Invalid request.'})

@login_required
def api_auto_mark_absent(request):
    target_date_str = request.GET.get('date')
    if target_date_str:
        try:
            target_date = datetime.datetime.strptime(target_date_str, '%Y-%m-%d').date()
        except ValueError:
            target_date = timezone.now().date()
    else:
        target_date = timezone.now().date()

    students = Student.objects.all()

    absent_count = 0
    for student in students:
        att, created = Attendance.objects.get_or_create(
            student=student,
            date=target_date,
            defaults={
                'department': student.department,
                'status': 'Absent',
                'is_late': False,
                'confidence_score': 0.0,
                'method': 'Auto System'
            }
        )
        if created:
            absent_count += 1

    log_activity(request.user, f"Auto-marked {absent_count} un-scanned students as ABSENT for Date: {target_date}", request)
    messages.success(request, f"Auto-marked {absent_count} un-scanned students as ABSENT for Date: {target_date}.")
    return redirect(request.META.get('HTTP_REFERER', 'attendance_history'))

@login_required
def api_reset_today_attendance(request):
    target_date_str = request.GET.get('date')
    if target_date_str:
        try:
            target_date = datetime.datetime.strptime(target_date_str, '%Y-%m-%d').date()
        except ValueError:
            target_date = timezone.now().date()
    else:
        target_date = timezone.now().date()

    deleted_count, _ = Attendance.objects.filter(date=target_date).delete()
    log_activity(request.user, f"Cleared {deleted_count} attendance logs for Date: {target_date}", request)
    messages.success(request, f"Cleared attendance logs for Date: {target_date}! Ready for fresh scanning.")
    return redirect(request.META.get('HTTP_REFERER', 'live_attendance'))

# --- 7. LEAVE REQUEST & ATTENDANCE CORRECTION MANAGEMENT ---
@login_required
def leave_list_view(request):
    profile = get_user_profile(request.user)
    student = Student.objects.filter(user=request.user).first()
    students = Student.objects.select_related('department').all()

    leaves = LeaveRequest.objects.select_related('student', 'student__department').all().order_by('-created_at')

    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        reason = request.POST.get('reason')
        student_id = request.POST.get('student_id')

        target_student = None
        if student_id:
            target_student = Student.objects.filter(id=student_id).first()
        if not target_student:
            target_student = student or Student.objects.first()

        if target_student and start_date and end_date:
            LeaveRequest.objects.create(student=target_student, start_date=start_date, end_date=end_date, reason=reason)
            log_activity(request.user, f"Submitted leave request for {target_student.name} ({start_date} to {end_date})", request)
            messages.success(request, f"Leave application for '{target_student.name}' submitted successfully!")
        else:
            messages.error(request, "Unable to process leave request. Please ensure valid date inputs.")

        return redirect('leave_list')

    context = {
        'leaves': leaves,
        'role': profile.role,
        'is_student': bool(student),
        'students': students
    }
    return render(request, 'leaves.html', context)

@login_required
def leave_approve_view(request, leave_id, status_code):
    leave = get_object_or_404(LeaveRequest, id=leave_id)
    if status_code in ['APPROVED', 'REJECTED']:
        leave.status = status_code
        leave.reviewed_by = request.user
        leave.save()

        if status_code == 'APPROVED':
            curr_date = leave.start_date
            added_count = 0
            while curr_date <= leave.end_date:
                att, created = Attendance.objects.get_or_create(
                    student=leave.student,
                    date=curr_date,
                    defaults={
                        'department': leave.student.department,
                        'status': 'Present (On Leave)',
                        'confidence_score': 100.0,
                        'method': 'Approved Leave Exemption'
                    }
                )
                if not created and att.status == 'Absent':
                    att.status = 'Present (On Leave)'
                    att.save()
                curr_date += datetime.timedelta(days=1)
                added_count += 1
            messages.success(request, f"Approved Leave for {leave.student.name}! Automatically updated {added_count} attendance day records to 'Present (On Leave)'.")
        else:
            messages.warning(request, f"Leave request for {leave.student.name} marked as REJECTED.")

        log_activity(request.user, f"Marked leave #{leave.id} as {status_code} for {leave.student.name}", request)
    return redirect('leave_list')

@login_required
def api_correct_attendance(request):
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        target_date_str = request.POST.get('target_date')
        new_status = request.POST.get('status', 'Present')

        student = get_object_or_404(Student, id=student_id)
        try:
            target_date = datetime.datetime.strptime(target_date_str, '%Y-%m-%d').date()
        except Exception:
            target_date = timezone.now().date()

        att, created = Attendance.objects.get_or_create(
            student=student,
            date=target_date,
            defaults={
                'department': student.department,
                'status': new_status,
                'confidence_score': 100.0,
                'method': 'Admin Correction'
            }
        )

        att.status = new_status
        att.method = 'Admin Correction'
        att.save()

        log_activity(request.user, f"Corrected attendance for {student.name} on {target_date} to '{new_status}'", request)
        messages.success(request, f"Attendance record for '{student.name}' on {target_date} successfully corrected to '{new_status}'!")

    return redirect('leave_list')

# --- 8. ATTENDANCE HISTORY & REPORTS ---
@login_required
def attendance_history_view(request):
    date_filter = request.GET.get('date')
    dept_filter = request.GET.get('dept', 'ALL')
    query = request.GET.get('q', '')

    attendances = Attendance.objects.select_related('student', 'department').all().order_by('-date', '-time_in')

    if date_filter:
        try:
            d_obj = datetime.datetime.strptime(date_filter, '%Y-%m-%d').date()
            attendances = attendances.filter(date=d_obj)
        except ValueError:
            date_filter = ''

    if dept_filter and dept_filter != 'ALL':
        attendances = attendances.filter(department__id=dept_filter)

    if query:
        attendances = attendances.filter(
            Q(student__name__icontains=query) | Q(student__roll_number__icontains=query)
        )

    departments = Department.objects.all()
    today_str = timezone.now().date().strftime('%Y-%m-%d')

    context = {
        'attendances': attendances,
        'departments': departments,
        'selected_date': date_filter if date_filter else today_str,
        'is_filtered_date': bool(date_filter),
        'selected_dept': dept_filter,
        'query': query,
        'today_date': today_str
    }
    return render(request, 'attendance_history.html', context)

@login_required
def reports_view(request):
    students = Student.objects.select_related('department').all()
    departments = Department.objects.all()

    student_reports = []
    for s in students:
        pct = s.attendance_percentage()
        student_reports.append({
            'student': s,
            'percentage': pct,
            'status': 'Eligible' if pct >= 75.0 else 'Shortage Warning (<75%)'
        })

    dept_reports = []
    for d in departments:
        d_students = Student.objects.filter(department=d)
        total_st = d_students.count()
        avg_pct = round(sum(s.attendance_percentage() for s in d_students) / total_st, 1) if total_st > 0 else 0
        dept_reports.append({
            'department': d,
            'total_students': total_st,
            'avg_percentage': avg_pct
        })

    context = {
        'student_reports': student_reports,
        'dept_reports': dept_reports
    }
    return render(request, 'reports.html', context)

# --- 9. EXPORTS & BACKUP ---
@login_required
def export_excel_view(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="Attendance_Report_{timezone.now().date()}.csv"'

    writer = csv.writer(response)
    writer.writerow(['Attendance ID', 'Roll Number', 'Student Name', 'Department', 'Year', 'Date', 'Time In', 'Time Out', 'Status', 'Confidence Score', 'Method'])

    attendances = Attendance.objects.select_related('student', 'department').all().order_by('-date')
    for a in attendances:
        writer.writerow([
            a.id,
            a.student.roll_number,
            a.student.name,
            a.department.name,
            a.student.year,
            a.date,
            a.time_in.strftime('%H:%M:%S') if a.time_in else '--',
            a.time_out.strftime('%H:%M:%S') if a.time_out else '--',
            a.status,
            f"{a.confidence_score}%",
            a.method
        ])

    return response

@login_required
def export_pdf_view(request):
    attendances = Attendance.objects.select_related('student', 'department').all().order_by('-date')[:100]
    context = {
        'attendances': attendances,
        'generated_at': timezone.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    return render(request, 'reports_pdf_template.html', context)

@login_required
def export_backup_db(request):
    db_path = settings.DATABASES['default']['NAME']
    if os.path.exists(db_path):
        log_activity(request.user, "Exported Database Backup", request)
        return FileResponse(open(db_path, 'rb'), as_attachment=True, filename=f"sqlite_backup_{timezone.now().date()}.sqlite3")
    messages.error(request, "Database backup file not found.")
    return redirect('dashboard')

@login_required
def audit_logs_view(request):
    logs = ActivityLog.objects.select_related('user').all().order_by('-timestamp')[:100]
    return render(request, 'audit_logs.html', {'logs': logs})

# --- 10. MANUAL ATTENDANCE BACKUP SYSTEM ---
@login_required
def manual_backup_view(request):
    students = Student.objects.select_related('department').all()
    today_date = timezone.now().date()
    today_attendances = Attendance.objects.filter(date=today_date).select_related('student', 'department').order_by('-time_in')
    context = {
        'students': students,
        'today_attendances': today_attendances,
        'today_date': today_date.strftime('%Y-%m-%d')
    }
    return render(request, 'manual_backup.html', context)

@login_required
def api_manual_attendance(request):
    if request.method == 'POST':
        student_identifier = request.POST.get('roll_number', '').strip()
        selected_student_id = request.POST.get('student_id')
        target_date_str = request.POST.get('target_date')

        if target_date_str:
            try:
                target_date = datetime.datetime.strptime(target_date_str, '%Y-%m-%d').date()
            except ValueError:
                target_date = timezone.now().date()
        else:
            target_date = timezone.now().date()

        student = None
        if selected_student_id:
            student = Student.objects.filter(id=selected_student_id).first()

        if not student and student_identifier:
            student = Student.objects.filter(
                Q(roll_number__iexact=student_identifier) |
                Q(student_id__iexact=student_identifier) |
                Q(name__icontains=student_identifier)
            ).first()

        if student:
            att, created = Attendance.objects.get_or_create(
                student=student,
                date=target_date,
                defaults={
                    'department': student.department,
                    'status': 'Present',
                    'confidence_score': 100.0,
                    'method': 'Manual Backup'
                }
            )

            if created:
                msg = f"Manual Attendance Marked: PRESENT for {student.name} ({student.roll_number}) on Date: {target_date}!"
                messages.success(request, msg)
                log_activity(request.user, f"Manually marked attendance for {student.name} ({student.roll_number})", request)
            else:
                msg = f"Student {student.name} ({student.roll_number}) is ALREADY marked for Date: {target_date}!"
                messages.info(request, msg)
        else:
            messages.error(request, f"No student found matching Roll Number / Name: '{student_identifier}'. Please check spelling or select from dropdown.")

    return redirect('manual_backup')
