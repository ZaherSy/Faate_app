from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
	path("get_student_sessions/", views.get_student_sessions, name="get_student_sessions"),
	path("student_login/", views.student_login, name="student_login"),
	path("scan_qr/", views.scan_qr, name="scan_qr"),
	path("teacher_login/", views.teacher_login, name="teacher_login"),
	path("create_session/", views.create_session, name="create_session"),
	path("get_courses_student/", views.get_courses_student, name="get_courses_student"),
	path("get_teacher_courses/", views.get_teacher_courses, name="get_teacher_courses"),
	path("get_teacher_course_sessions/", views.get_teacher_course_sessions, name="get_teacher_course_sessions"),
	path("get_session_details/", views.get_session_details, name="get_session_details"),
	path("get_student_sessions_by_student/", views.get_student_sessions_by_student, name="get_student_sessions_by_student"),
	
	]
