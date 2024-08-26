from django.db import models

class Department(models.Model):
	name = models.CharField(max_length=100) #networks software general

class Course(models.Model):
	name = models.CharField(max_length=100)
	sessions_num =models.IntegerField()
	type=models.CharField(max_length=100)#practical - theoritical
	department=models.ForeignKey("Department", on_delete=models.CASCADE)	
	course_year=models.IntegerField(null=True)

class Student(models.Model):
	name = models.CharField(max_length=100)
	image =models.ImageField(upload_to='Student_images/')
	id_num =models.CharField(max_length=100)
	password=models.CharField(max_length=100)
	phone=models.CharField(max_length=100)
	year=models.CharField(max_length=100)
	department=models.ForeignKey("Department", on_delete=models.CASCADE)
	group=models.IntegerField()

class Teacher(models.Model):
	name = models.CharField(max_length=100)
	image =models.ImageField(upload_to='Teacher_images/')
	id_num =models.CharField(max_length=100)
	password=models.CharField(max_length=100)
	phone=models.CharField(max_length=100)
	level=models.CharField(max_length=100)#teacher - teacher assistant - professor - eng
	department=models.ForeignKey("Department", on_delete=models.CASCADE)

class CourseStudent(models.Model):
	course=models.ForeignKey("Course", on_delete=models.CASCADE)
	student=models.ForeignKey("Student", on_delete=models.CASCADE)
	
class CourseTeacher(models.Model):
	course=models.ForeignKey("Course", on_delete=models.CASCADE)
	teacher=models.ForeignKey("Teacher", on_delete=models.CASCADE)
	
class Session(models.Model):
	course=models.ForeignKey("Course", on_delete=models.CASCADE)
	teacher=models.ForeignKey("Teacher", on_delete=models.CASCADE)
	order=models.IntegerField()
	date=models.DateField(auto_now_add=True)
	qr=models.CharField(max_length=200)
	group=models.IntegerField()

class StudentSession(models.Model):
	student=models.ForeignKey("Student", on_delete=models.CASCADE)
	session=models.ForeignKey("Session", on_delete=models.CASCADE)
	exist=models.IntegerField()