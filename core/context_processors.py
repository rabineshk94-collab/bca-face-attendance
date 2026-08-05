def translation_processor(request):
    lang = request.session.get('django_language', 'EN')
    is_ta = (lang == 'TA')

    t = {
        # Brand & Nav
        'brand_title': 'FaceVision AI' if not is_ta else 'ஃபேஸ்விஷன் AI',
        'nav_home': 'Home' if not is_ta else 'முகப்பு',
        'nav_dashboard': 'Dashboard' if not is_ta else 'டாஷ்போர்டு',
        'nav_scanner': 'Live Scanner' if not is_ta else 'நேரடி ஸ்கேனர்',
        'nav_students': 'Students' if not is_ta else 'மாணவர்கள் பட்டியல்',
        'nav_leaves': 'Leaves' if not is_ta else 'விடுப்பு மேலாண்மை',
        'nav_history': 'History' if not is_ta else 'வருகைப் பதிவு வரலாறு',
        'nav_reports': 'Reports' if not is_ta else 'அறிக்கைகள் & பகுப்பாய்வு',
        'nav_audit': 'Audit Logs' if not is_ta else 'பாதுகாப்பு தணிக்கைப் பதிவேடு',
        'nav_backup': 'Manual Backup' if not is_ta else 'மேனுவல் பேக்கப்',
        'nav_info': 'Project Info' if not is_ta else 'திட்ட ஆவணங்கள்',
        'nav_menu': 'MENU' if not is_ta else 'மெனு',
        'nav_logout': 'Logout Account' if not is_ta else 'கணக்கிலிருந்து வெளியேறு',
        'nav_login': 'Login Account' if not is_ta else 'கணக்கில் உள்நுழை',

        # Home Page Full Translations
        'hm_badge': 'BCA Final-Year Major Project' if not is_ta else 'BCA இறுதி ஆண்டு முதன்மை பட்டப்படிப்பு திட்டம்',
        'hm_title': 'AI-Powered Face Recognition Attendance System' if not is_ta else 'செயற்கை நுண்ணறிவு முக அங்கீகார வருகைப் பதிவு அமைப்பு',
        'hm_lead': 'An automated biometric attendance management system built with Python, Django, OpenCV, and SQLite. Eliminates proxy attendance with real-time face detection, confidence score analysis, anti-spoofing photo detection, and instant CSV/PDF reporting.' if not is_ta else 'Python, Django, OpenCV மற்றும் SQLite கொண்டு உருவாக்கப்பட்ட தானியங்கி பயோமெட்ரிக் வருகைப் பதிவு அமைப்பு. போலி வருகைப் பதிவுகளைத் தடுத்து நேரடி முக அங்கீகாரம், புகைப்படக் கண்டறிதல் மற்றும் உடனடி எக்செல்/PDF அறிக்கைகளை வழங்குகிறது.',
        'hm_btn_dash': 'Go to Admin Dashboard' if not is_ta else 'நிர்வாக டாஷ்போர்டிற்குச் செல்',
        'hm_btn_scan': 'Start Live Scanner' if not is_ta else 'நேரடி ஸ்கேனரைத் தொடங்கு',
        'hm_btn_login': 'Admin Login' if not is_ta else 'நிர்வாகி உள்நுழைவு',
        'hm_btn_specs': 'Read Project Specs' if not is_ta else 'திட்ட விவரங்களைப் படிக்கவும்',
        'hm_engine_title': 'Real-Time OpenCV Engine' if not is_ta else 'நேரடி OpenCV இஞ்சின்',
        'hm_engine_desc': 'Webcam facial detection with 128D descriptor matching & anti-spoof liveness verification.' if not is_ta else '128D வெக்டார் பொருத்தம் மற்றும் போலி புகைப்படத் தடுப்பு சரிபார்ப்புடன் கூடிய கேமரா முகக் கண்டறிதல்.',
        'hm_modules_title': 'Key Project Modules' if not is_ta else 'முக்கிய திட்ட தொகுதிகள்',
        'm1_title': '1. Admin Auth & Dashboard' if not is_ta else '1. நிர்வாக உள்நுழைவு & டாஷ்போர்டு',
        'm1_desc': 'Secure authentication, session control, total student counts, daily attendance rate, and interactive analytics.' if not is_ta else 'பாதுகாப்பான அங்கீகாரம், அமர்வு கட்டுப்பாடு, மொத்த மாணவர் எண்ணிக்கை மற்றும் வருகை புள்ளிவிவரங்கள்.',
        'm2_title': '2. Face Registration & Encodings' if not is_ta else '2. முகப் பதிவு & குறியாக்கம்',
        'm2_desc': 'Capture multi-angle webcam photos for each student, extract 128D feature encodings, and store in relational database.' if not is_ta else 'ஒவ்வொரு மாணவருக்கும் பல கோண புகைப்படங்களைப் பதிவு செய்து 128D குறியாக்கங்களை சேமித்தல்.',
        'm3_title': '3. Recognition & Anti-Spoof' if not is_ta else '3. முக அங்கீகாரம் & போலித் தடுப்பு',
        'm3_desc': 'Live recognition HUD displaying bounding box, match confidence score %, duplicate prevention, and screen photo spoof detection.' if not is_ta else 'நேரடி பாக்ஸ், பொருத்தம் %, இரட்டைப் பதிவு தடுப்பு மற்றும் திரைப் புகைப்பட போலி கண்டறிதல்.',
        'm4_title': '4. Records & Excel/PDF Export' if not is_ta else '4. பதிவுகள் & எக்செல்/PDF ஏற்றுமதி',
        'm4_desc': 'Filter daily attendance by date, roll number, or department. One-click Excel CSV export and printable PDF reports.' if not is_ta else 'தேதி, ரோல் எண் அல்லது துறை வாரியாக வடிகட்டி எக்செல் CSV மற்றும் PDF அறிக்கைகளை பதிவிறக்கம் செய்யுங்கள்.',
        'm5_title': '5. Shortage Warning (<75%)' if not is_ta else '5. வருகைக் குறைபாடு எச்சரிக்கை (<75%)',
        'm5_desc': 'Automatic percentage calculator flagging students below mandatory attendance threshold with condonation alerts.' if not is_ta else 'கட்டாய 75% வருகைக்குக் குறைவாக உள்ள மாணவர்களைத் தானாகக் கண்டறிந்து எச்சரிக்கும் அமைப்பு.',
        'm6_title': '6. Manual Backup System' if not is_ta else '6. மேனுவல் வருகைப் பதிவு பேக்கப்',
        'm6_desc': 'Fallback manual attendance logging method in case of hardware webcam failure.' if not is_ta else 'கேமரா கோளாறுகளின் போது கைமுறையாக ரோல் எண் மூலம் வருகையைப் பதிவு செய்யும் மாற்று முறை.',

        # Dashboard Metrics
        'dash_title': 'Dashboard Overview' if not is_ta else 'டாஷ்போர்டு மேலோட்டம்',
        'dash_subtitle': 'Real-time attendance analytics & biometric system stats' if not is_ta else 'நேரடி வருகைப் பதிவு பகுப்பாய்வு மற்றும் கணினி புள்ளிவிவரங்கள்',
        'dash_total_students': 'Total Registered Students' if not is_ta else 'பதிவு செய்யப்பட்ட மொத்த மாணவர்கள்',
        'dash_departments': 'Active Departments' if not is_ta else 'செயலில் உள்ள கல்விக் களங்கள்',
        'dash_today_present': 'Today Present' if not is_ta else 'இன்று வருகை தந்தவர்கள்',
        'dash_today_absent': 'Today Absent' if not is_ta else 'இன்று வரவில்லை',
        'dash_pending_leaves': 'Pending Leave Requests' if not is_ta else 'நிலுவையில் உள்ள விடுப்பு மனுக்கள்',
        'dash_recent_activity': 'Recent Live Scanner Check-Ins' if not is_ta else 'சமீபத்திய நேரடி ஸ்கேனர் பதிவுகள்',
        'dash_dept_performance': 'Department Attendance Rates' if not is_ta else 'துறை வாரியான வருகைப் பதிவு விகிதம்',

        # Live Scanner
        'scanner_title': 'Live Face Recognition Scanner' if not is_ta else 'நேரடி முக அங்கீகார ஸ்கேனர்',
        'scanner_subtitle': 'Automatic attendance logging synced with your laptop date' if not is_ta else 'உங்கள் கணினி தேதியுடன் இணைக்கப்பட்ட தானியங்கி வருகைப் பதிவு',
        'btn_reset_logs': 'Reset Date Logs' if not is_ta else 'தேதி பதிவுகளை மீட்டமை',
        'btn_pause': 'Pause' if not is_ta else 'இடைநிறுத்து',
        'btn_resume': 'Resume' if not is_ta else 'தொடர்',
        'target_result': 'Recognition Target Result' if not is_ta else 'அங்கீகார இலக்கு முடிவு',

        # Students Roster
        'st_list_title': 'Student Roster Directory' if not is_ta else 'மாணவர்கள் பட்டியல் விவரப்பகம்',
        'st_add_btn': 'Add New Student' if not is_ta else 'புதிய மாணவரைச் சேர்',
        'st_search_ph': 'Search by Name or Roll Number...' if not is_ta else 'பெயர் அல்லது ரோல் எண்ணை உள்ளிடுக...',
        'th_name': 'Student Name' if not is_ta else 'மாணவர் பெயர்',
        'th_roll': 'Roll Number' if not is_ta else 'ரோல் எண்',
        'th_dept': 'Department' if not is_ta else 'துறை',
        'th_year': 'Year' if not is_ta else 'ஆண்டு',
        'th_id_card': 'Digital ID Card' if not is_ta else 'டிஜிட்டல் அடையாள அட்டை',
        'th_face': 'Face Encodings' if not is_ta else 'முகக் குறியாக்கம்',
        'th_action': 'Actions' if not is_ta else 'செயல்கள்',

        # Leaves & Attendance Corrections
        'leaves_title': 'Leave Requests & Attendance Corrections' if not is_ta else 'விடுப்பு விண்ணப்பங்கள் & வருகைத் திருத்தங்கள்',
        'leaves_subtitle': 'Apply for leaves, track approval status, and manage student attendance corrections' if not is_ta else 'விடுப்புகளுக்கு விண்ணப்பிக்கவும், ஒப்புதல் நிலையை கண்காணிக்கவும், திருத்தங்களை நிர்வகிக்கவும்',
        'leaves_apply': 'Apply for Leave' if not is_ta else 'விடுப்பிற்கு விண்ணப்பிக்கவும்',
        'leaves_select_st': 'Select Student *' if not is_ta else 'மாணவரைத் தேர்ந்தெடுக்கவும் *',
        'leaves_start': 'Start Date *' if not is_ta else 'தொடக்க தேதி *',
        'leaves_end': 'End Date *' if not is_ta else 'முடிவு தேதி *',
        'leaves_reason': 'Reason for Leave *' if not is_ta else 'விடுப்பிற்கான காரணம் *',
        'btn_submit_leave': 'Submit Leave Request' if not is_ta else 'விடுப்பு விண்ணப்பத்தை சமர்ப்பி',
        'corr_title': 'Manual Attendance Correction' if not is_ta else 'கைமுறை வருகைப் பதிவு திருத்தம்',
        'corr_target_date': 'Target Date *' if not is_ta else 'இலக்கு தேதி *',
        'corr_status': 'Corrected Status *' if not is_ta else 'திருத்தப்பட்ட நிலை *',
        'btn_save_corr': 'Update & Save Correction' if not is_ta else 'திருத்தத்தைப் புதுப்பித்துச் சேமி',

        # Attendance History
        'hist_title': 'Attendance Audit History Logs' if not is_ta else 'வருகைப் பதிவு வரலாறு & தணிக்கைப் பதிவேடு',
        'hist_subtitle': 'Search, filter, inspect, and export time-stamped attendance records' if not is_ta else 'கால முத்திரையிடப்பட்ட வருகைப் பதிவுப் பதிவுகளைத் தேடி, ஏற்றுமதி செய்யுங்கள்',
        'btn_auto_absent': 'Auto-Mark Absent' if not is_ta else 'தானியங்கி ஆப்சென்ட் பதிவு',
        'btn_export_csv': 'Export Excel (CSV)' if not is_ta else 'எக்செல் ஏற்றுமதி (CSV)',
        'btn_print_pdf': 'Print PDF Report' if not is_ta else 'PDF அறிக்கையை அச்சிடு',
        'lbl_select_date': 'Select Date' if not is_ta else 'தேதியைத் தேர்ந்தெடுக்கவும்',
        'lbl_filter_dept': 'Filter Department' if not is_ta else 'துறையை வடிகட்டு',
        'btn_filter': 'Filter Logs' if not is_ta else 'பதிவுகளை வடிகட்டு',
        'btn_clear': 'Clear' if not is_ta else 'அழி',

        # Manual Backup System
        'mb_title': 'Manual Attendance Backup System' if not is_ta else 'மேனுவல் வருகைப் பதிவு பேக்கப் அமைப்பு',
        'mb_subtitle': 'Manually log attendance by Roll Number, Student ID, or Dropdown Selection' if not is_ta else 'ரோல் எண் அல்லது பட்டியலிலிருந்து கைமுறையாக வருகையைப் பதிவு செய்யுங்கள்',
        'btn_mark_present': 'Mark Attendance PRESENT' if not is_ta else 'பிரசண்ட் (PRESENT) எனப் பதிவு செய்',

        # General Statuses & Badges
        'status_present': 'Present' if not is_ta else 'வந்துள்ளார் (Present)',
        'status_absent': 'Absent' if not is_ta else 'வரவில்லை (Absent)',
        'status_late': 'Late' if not is_ta else 'தாமதம் (Late)',
        'status_leave': 'Present (On Leave)' if not is_ta else 'விடுப்பில் (On Leave)',

        # Footer
        'footer_text': 'Face Recognition Attendance System — Advanced Enterprise BCA Project' if not is_ta else 'முக அங்கீகார வருகைப் பதிவு அமைப்பு — மேம்பட்ட BCA பட்டப்படிப்பு திட்டம்',
        'is_ta': is_ta
    }

    return {'tr': t}
