# AI-Powered Face Recognition Attendance System (BCA Major Project)

![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)
![Django](https://img.shields.io/badge/Django-5.0-green.svg)
![OpenCV](https://img.shields.io/badge/OpenCV-Computer%20Vision-orange.svg)
![SQLite](https://img.shields.io/badge/SQLite-Database-lightgrey.svg)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple.svg)

An enterprise-grade **Face Recognition Attendance System** developed for a **Bachelor of Computer Applications (BCA) Final-Year Major Project**.

---

## 🌟 Key Features

- **Admin, Teacher & Student Portals**: Role-based access control and dashboards.
- **Bilingual Multi-Language Support**: Toggle between **English** and **Tamil (தமிழ்)**.
- **OpenCV Face Engine**: Real-time multi-landmark detection with confidence score %.
- **Anti-Spoofing Protection**: Laplacian texture variance analysis detecting photo & screen spoofing.
- **Digital Student ID Card Generator**: Printable ID cards with student photos, QR codes, and **CODE128 Barcodes**.
- **Leave Application & Approvals**: Students apply for leave; Teachers/Admins approve or reject.
- **Attendance Audit Logs & Database Backup**: One-click SQLite backup download & security activity log viewer.
- **Excel & PDF Exports**: Download class attendance as Excel (CSV) or printable PDF reports.
- **QR Code Backup Attendance**: Secondary QR code roll scanner fallback.

---

## 🛠 Tech Stack

- **Backend**: Python 3.10+, Django 5.x
- **Computer Vision**: OpenCV (`opencv-python`), NumPy, Pillow
- **Database**: SQLite3
- **Frontend**: HTML5, CSS3, Bootstrap 5, Chart.js, JsBarcode, RemixIcons

---

## 🚀 Quick Setup Instructions

### 1. Clone & Install Dependencies
```bash
git clone https://github.com/your-username/bca-face-attendance.git
cd bca-face-attendance
pip install django opencv-python numpy pillow jsbarcode
```

### 2. Apply Migrations & Seed Sample Data
```bash
python manage.py makemigrations core
python manage.py migrate
python seed_db.py
```

### 3. Run Development Server
```bash
python manage.py runserver 8000
```
Open your browser at **[http://localhost:8000](http://localhost:8000)**  
- **Admin Username**: `admin`
- **Admin Password**: `admin123`

---

## 📄 License & Credits
Developed for BCA Final Year Major Project 2026 Academic Session.
