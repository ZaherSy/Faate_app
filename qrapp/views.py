from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt,ensure_csrf_cookie
import json
from .models import *
from django.forms.models import model_to_dict
from django.http import JsonResponse,HttpResponse
from django.conf import settings
from django.core.files import File
import base64
from django.core.files.base import ContentFile
# import cv2
# import numpy as np

###########################################################################
#########################Student#########################
###########################################################################
#delete

appUrl="http://192.168.43.224:8000"

@csrf_exempt		
def student_login(request):
	try:   
		body=request.body.decode('utf-8')
		body=json.loads(body)
		id_num=body['id_num']
		password=body['password']
		u=Student.objects.get(id_num=id_num,password=password)
		ujs=model_to_dict(u)
		del ujs["password"]
		ujs["image"]=appUrl+u.image.url
		ujs["department"]=u.department.name
		return JsonResponse({'response':'ok','data':ujs})
	except Exception as e:
		print(e)
		return JsonResponse({'response':'error'})

@csrf_exempt		
def scan_qr(request):
	try:   
		body=request.body.decode('utf-8')
		body=json.loads(body)
		qr=body['qr']
		student_id=body['student_id']
		stu=Student.objects.get(id=student_id)
		sess=Session.objects.get(qr=qr)
		obj=StudentSession.objects.get(student=stu,session=sess)
		obj.exist=1
		obj.save()
		return JsonResponse({'response':'ok'})
	except Exception as e:
		print(e)
		return JsonResponse({'response':'error'})		
		
@csrf_exempt		
def get_student_sessions_by_student(request):
	try:   
		body=request.body.decode('utf-8')
		body=json.loads(body)
		student_id=body['student_id']
		stu=Student.objects.get(id=student_id)
		
		obj=StudentSession.objects.filter(student=stu)
		courses=set()
		data=[]
		
		for o in obj:
			courses.add(o.session.course)
		courses_list=list(courses)
		for cou in courses_list:
			d={}
			d["name"]=cou.name
			d["sessions_num"]=cou.sessions_num
			d["type"]=cou.type
			d["department"]=cou.department.name
			d["sessions"]=[]
			for ses in Session.objects.filter(course=cou):
				for o in StudentSession.objects.filter(student=stu,session=ses):
					s={}
					s["order"]=ses.order
					s["date"]=ses.date 
					s["exist"]=o.exist 
					d["sessions"].append(s)
			data.append(d)
		return JsonResponse({'response':'ok','data':data})
	except Exception as e:
		print(e)
		return JsonResponse({'response':'error'})

@csrf_exempt		
def get_courses_student(request):
	try:   
		body=request.body.decode('utf-8')
		body=json.loads(body)
		student_id=body['student_id']
		obj=CourseStudent.objects.filter(student=Student.objects.get(id=student_id))
		data=[]
		for cou in obj:
			d={}
			d["course_id"]=cou.course.id
			d["name"]=cou.course.name
			d["sessions_num"]=cou.course.sessions_num
			d["type"]=cou.course.type
			d["department"]=cou.course.department.name
			d['course_year'] =cou.course.course_year
			data.append(d)
		return JsonResponse({'response':'ok','data':data})
	except Exception as e:
		print(e)
		return JsonResponse({'response':'error'})			
###########################################################################
#########################Teacher#########################
###########################################################################
@csrf_exempt		
def teacher_login(request):
	try:   
		body=request.body.decode('utf-8')
		body=json.loads(body)
		id_num=body['id_num']
		password=body['password']
		u=Teacher.objects.get(id_num=id_num,password=password)
		ujs=model_to_dict(u)
		del ujs["password"]
		ujs["image"]=appUrl+u.image.url
		ujs["department"]=u.department.name
		return JsonResponse({'response':'ok','data':ujs})
	except Exception as e:
		print(e)
		return JsonResponse({'response':'error'})

@csrf_exempt		
def create_session(request):
	try:
		body = request.body.decode('utf-8')
		body=json.loads(body)
		course_id=body['course_id']
		teacher_id=body['teacher_id']
		order=body['order']
		qr=body['qr']
		group=body['group']
		c=Course.objects.get(id=course_id)
		t=Teacher.objects.get(id=teacher_id)
		try:
			CourseTeacher.objects.get(course=c,teacher=t)
		except:
			CourseTeacher(course=c,teacher=t).save()
		ses=Session(course=c,teacher=t,order=order ,qr=qr,group=group)
		ses.save()
		for stu in CourseStudent.objects.filter(course=c):
			if stu.student.group == group:
				StudentSession(student=stu.student,session=ses,exist=0).save()
		return JsonResponse({'response':'ok'})
	except Exception as e:
		print(e)
		return JsonResponse({'response':'error'})
	
@csrf_exempt		
def get_teacher_courses(request):
	try:
		body = request.body.decode('utf-8')
		body=json.loads(body)
		teacher_id=body['teacher_id']
		data=[]
		for c in CourseTeacher.objects.filter(teacher=Teacher.objects.get(id=teacher_id)):
			dic={}
			dic["course_id"]=c.course.id
			dic["name"]=c.course.name
			dic["sessions_num"]=c.course.sessions_num
			dic["type"]=c.course.type
			dic["department"]=c.course.department.name
			dic["course_year"]=c.course.course_year
			data.append(dic)
		return JsonResponse({'response':'ok','data':data})
	except Exception as e:
		print(e)
		return JsonResponse({'response':'error'})

@csrf_exempt		
def get_teacher_course_sessions(request):
	try:
		body = request.body.decode('utf-8')
		body=json.loads(body)
		teacher_id=body['teacher_id']
		course_id=body['course_id']
		data=[]
		for c in Session.objects.filter(teacher=Teacher.objects.get(id=teacher_id),course=Course.objects.get(id=course_id)):
			dic={}
			dic["id"]=c.id
			dic["order"]=c.order
			dic["date"]=c.date
			dic["qr"]=c.qr
			dic["group"]=c.group
			dic["num_exists"]=len(StudentSession.objects.filter(session=c,exist=1))
			dic["num_not_exists"]=len(StudentSession.objects.filter(session=c,exist=0))
			data.append(dic)
		return JsonResponse({'response':'ok','data':data})
	except Exception as e:
		print(e)
		return JsonResponse({'response':'error'})


@csrf_exempt		
def get_session_details(request):
	try:
		body = request.body.decode('utf-8')
		body=json.loads(body)
		session_id=body['session_id']
		sess=Session.objects.get(id=session_id)
		data=[]
		for obj in StudentSession.objects.filter(session=sess):
			dic={}
			dic["student_name"]=obj.student.name
			dic["student_id_num"]=obj.student.id_num
			dic['student_image']=appUrl+obj.student.image.url
			dic["exist"]=obj.exist
			data.append(dic)
		return JsonResponse({'response':'ok','data':data})
	except Exception as e:
		print(e)
		return JsonResponse({'response':'error'})

@csrf_exempt		
def get_student_sessions(request):
	try:
		body = request.body.decode('utf-8')
		body=json.loads(body)
		student_id=body['student_id']
		course_id=body['course_id']
		c=Course.objects.get(id=course_id)
		data=[]
		for ss in StudentSession.objects.filter(student=Student.objects.get(id=student_id)):
			if ss.session.course==c:
				dic={}
				dic["session_order"]=ss.session.order
				dic["session_date"]=ss.session.date
				dic["exist"]=ss.exist
				data.append(dic)
		return JsonResponse({'response':'ok','data':data})
	except Exception as e:
		print(e)
		return JsonResponse({'response':'error'})
	
