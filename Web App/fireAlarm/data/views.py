from email.headerregistry import Group
from fileinput import filename
from django.shortcuts import render
from django.http import HttpResponse
from .models import *
import random
from .decorators import *
from django.shortcuts import redirect
import pyrebase
from django.shortcuts import get_object_or_404, render
import datetime;
from django.utils.html import strip_tags
from django.urls import reverse, reverse_lazy
from django.shortcuts import render,HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string, get_template
from django.conf import settings
from django.core.mail import send_mail

from .forms import *
from templates import *
from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User

# import gspread
# gc=gspread.service_account(filename='credentials.json')
# sh=gc.open_by_key('15-itebVVyWrgPlr5qjMDYk3LNG55fhygj66YDEG9pdw')
# worksheet=sh.sheet1
# res=worksheet.get_all_records()
# smoke_sheet=worksheet.col_values(3)[1:]
# flame_sheet=worksheet.col_values(4)[1:]

# print("smoke values:")
# print(smoke_sheet)
# print("flame values: ")
# print(flame_sheet)
# print(res)

config = {
    'apiKey': "AIzaSyBV3jP5cl1AVP3HgO6_1J_wrjyffqQUfko",
    'authDomain': "iotproject-2800f.firebaseapp.com",
    'databaseURL': "https://iotproject-2800f-default-rtdb.firebaseio.com",
    'projectId': "iotproject-2800f",
    'storageBucket': "iotproject-2800f.appspot.com",
    'messagingSenderId': "863247827424",
    'appId': "1:863247827424:web:ba640e5eabf0b412062b85",
    'measurementId': "G-727CF3R175"
  }
firebase=pyrebase.initialize_app(config)
# Create your views here.

db=firebase.database()
data=db.child("15-itebVVyWrgPlr5qjMDYk3LNG55fhygj66YDEG9pdw/Sheet1").get().val()
#print(data)

# flame_val=[]
# smoke_val=[]
# for val in data:
# 		print(data[val]['flame_sensor'])
# 		flame_val.append(data[val]['flame_sensor'])
# 		smoke_val.append(data[val]['gas'])

# print(flame_val)


	

def index(request):
    return render(request,'index.html')
def send(request):
	return render(request,'send.html')
def registerPage(request):
	if request.user.is_authenticated:
		return redirect('dashboard')
	else:
		form = CreateUserForm()
		if request.method == 'POST':
			form = CreateUserForm(request.POST)
			if form.is_valid():
				form.save()
				user = form.cleaned_data.get('username')
				return HttpResponseRedirect('/loginpage')
		context = {'form':form}
		return render(request, 'signup.html', context)

def userpage(request):
	context={}
	return render(request,'normal.html',context)

def loginpage(request):
	if request.user.is_authenticated:
		return redirect('dashboard')
		#return render(request, 'dashboard.html',{'email':request.user.email})
	else:
		if request.method == 'POST':
			username = request.POST.get('username')
			password =request.POST.get('password')

			user = authenticate(request, username=username, password=password)

			if user is not None:
				login(request, user)
				return redirect('dashboard')
			else:
				messages.info(request, 'invalid credentials')
		return render(request, 'login.html')

def logoutuser(request):
    logout(request)
    return render(request,'index.html')

def given_access(request):
	users = User.objects.filter(groups__name='can_view')
	print(users)
	return render(request,'can_view_grp.html',{'req':users})
	#return HttpResponse("who has access!!!")

def add_to_grp(request,pk):
	#req=request_access_model.objects.all().values().distinct()
	for name in User.objects.all():
		print("username: ",name.username)
		print("email: ",name.email)
		if name.username == pk:
			print("pk: ",pk)
			# group=Group.objects.get(name='request_access_model')
			# name.groups.add(group)
			my_group = Group.objects.get(name='can_view') 
			my_group.user_set.add(name)
			if request_access_model.objects.filter(username=pk).exists():
				request_access_model.objects.filter(username=pk).delete()
			subject = 'Granted Access!!!'
			message = f'Hi {name.username}, you can now login into FIRE ALARM SYSTEM website!!!'
			email_from = settings.EMAIL_HOST_USER
			recipient_list = [name.email, ]
			send_mail( subject, message, email_from, recipient_list )

	return redirect('show_request')

def remove_from_grp(request,pk):
	#req=request_access_model.objects.all().values().distinct()
	for name in User.objects.all():
		print("username: ",name.username)
		print("email: ",name.email)
		if name.username == pk:
			print("pk: ",pk)
			# group=Group.objects.get(name='request_access_model')
			# name.groups.add(group)
			my_group = Group.objects.get(name='can_view') 
			my_group.user_set.remove(name)
			#User.objects.filter(username=username).exists()
			#remove_req=request_access_model.objects.get(username=pk).exists()
			if request_access_model.objects.filter(username=pk).exists():
				request_access_model.objects.filter(username=pk).delete()
			subject = 'Access cancelled!!!'
			message = f'Hi {name.username}, your access to FIRE ALARM SYSTEM website is no more!!!'
			email_from = settings.EMAIL_HOST_USER
			recipient_list = [name.email, ]
			send_mail( subject, message, email_from, recipient_list )
			
	return redirect('given_access')

def show_request(request):
	req=request_access_model.objects.all().values().distinct()
	print(req)
	return render(request,'show_request.html',{'req':req})
	return HttpResponse("show requests!!!")
@login_required(login_url='loginpage')
def dashboard(request):
	group=request.user.groups.all()
	print("group: ",len(group), request.user)
	if len(group)==0:
		return redirect('userpage')
	group=group[0].name
	print("group: ",group, request.user)
	if group=='admin':
		return render(request,'admin_dashboard.html',{'email':request.user.email})
	if group=='can_view' :
		return render(request,'dashboard.html',{'email':request.user.email})
	

def history(request):
	db=firebase.database()
	data=db.child("sensordata").get().val()
	#print(data)
	# flame_val1=[]
	# smoke_val1=[]
	# flame_val2=[]
	# smoke_val2=[]
	# flame_val3=[]
	# smoke_val3=[]
	# time=[]
	# for val in data:
	# 		#print(data[val]['flame_sensor'])
	# 		flame_val.append(data[val]['Flame'])
	# 		smoke_val.append(data[val]['Smoke'])
	# 		time.append(data[val]['Time'])
	# 		# #print(type(data[val]['curr_time']),type(data[val]['flame_sensor']))
	# 		# size=len(data[val]['Time'])
	# 		# list_val=data[val]['Time'][0:size-3].split(":")
	# 		# #tym=""
	# 		# tym = ''.join(list_val)
	# 		# # #print("tym: ",tym," actual: ",data[val]['curr_time'])
	# 		# time.append(int(tym))
	# print(flame_val)
	# print(smoke_val)
	# #print(time)
	# print(time)
	# flame_val.reverse()
	# smoke_val.reverse()
	# time.reverse()
	return render(request,'history.html',{'sensors_data':data})
	#return render(request,'history.html',{'flame_val': flame_val,'smoke_val':smoke_val})


def fire_history(request):
	db=firebase.database()
	data=db.child("sensordata").get().val()
	flame_val1=[]
	smoke_val1=[]
	flame_val2=[]
	smoke_val2=[]
	flame_val3=[]
	smoke_val3=[]
	time=[]
	count=0
	for key,val in data.items():
			#print(data[val]['flame_sensor'])
			# print("key: ",key)
			# print("val: ",val)
		#print(val['flame_value1'],val['flame_value2'],val['flame_value3'],val['smoke_value1']+val['smoke_value2']+val['smoke_value3'])
		if val['smoke_value1']>800 and val['smoke_value2']>800 and  (val['flame_value1']+val['flame_value2'])==0:
			print("satisfied!!!")
			count+=1
			flame_val1.append(val['flame_value1'])
			smoke_val1.append(val['smoke_value1'])

			flame_val2.append(val['flame_value2'])
			smoke_val2.append(val['smoke_value2'])

			# flame_val3.append(val['flame_value3'])
			# smoke_val3.append(val['smoke_value3'])
			#print(type(data[val]['Date']))
			# date=key
			# date_space=date.split(" ")
			# time_split=date_space[4].split(":")
			# tym=''.join(time_split)
			# print("modified_time: ",time)
			#time.append(key)
			#print(type(data[val]['curr_time']),type(data[val]['flame_sensor']))
			# print("time: ",data[val]['Time']," date: ",data[val]['Date'])
			# size=len(data[val]['Date'])
			# list_val=data[val]['Date'][0:size-3].split(":")
			# # #tym=""
			# tym = ''.join(list_val)
			# #print("tym: ",tym," actual: ",data[val]['curr_time'])
			time.append(key)
	# print(flame_val)
	# print(smoke_val)
	#print(time)
	# print(time)
	# flame_val.reverse()
	# smoke_val.reverse()
	# time.reverse()
	return render(request,'fire_history.html',{'flame_val1': flame_val1,'smoke_val1':smoke_val1,'time':time,
	'flame_val2': flame_val2,'smoke_val2':smoke_val2,'count':range(count)})

def request_access(request):
	form=send_request()
	username=request.user 
	email=request.user.email
	print("form: ",form.errors)
	print(request.method)
	
	print("valid!!!")
	post=form.save(commit = False)
	post.username=username
	post.email=email
	post.save()
	context = {'form':form,'username':username,'email':email}
	return render(request,'request_access.html',context)
	#return render(request,'request_access.html')
	# return render(request,'base.html',context)

def detail(request,pk):
	db=firebase.database()
	data=db.child("sensordata").get().val()[pk]
	print(data)
	val=[]
	val.append(data['smoke_value1'])
	val.append(data['smoke_value2'])
	#val.append(data['smoke_value3'])
	print(val)
	return render(request,'detail.html',{'val':val})



def graph(request):
	db=firebase.database()
	data=db.child("sensordata").get().val()
	flame_val1=[]
	smoke_val1=[]
	flame_val2=[]
	smoke_val2=[]
	# flame_val3=[]
	# smoke_val3=[]
	time=[]
	for key,val in data.items():
			#print(data[val]['flame_sensor'])
			# print("key: ",key)
			# print("val: ",val)
			flame_val1.append(val['flame_value1'])
			smoke_val1.append(val['smoke_value1'])

			flame_val2.append(val['flame_value2'])
			smoke_val2.append(val['smoke_value2'])

			# flame_val3.append(val['flame_value3'])
			# smoke_val3.append(val['smoke_value3'])
			#print(type(data[val]['Date']))
			date=key
			date_space=date.split(" ")
			time_split=date_space[4].split(":")
			tym=''.join(time_split)
			# print("modified_time: ",time)
			#time.append(key)
			#print(type(data[val]['curr_time']),type(data[val]['flame_sensor']))
			# print("time: ",data[val]['Time']," date: ",data[val]['Date'])
			# size=len(data[val]['Date'])
			# list_val=data[val]['Date'][0:size-3].split(":")
			# # #tym=""
			# tym = ''.join(list_val)
			# #print("tym: ",tym," actual: ",data[val]['curr_time'])
			time.append(int(tym))
	# print(flame_val)
	# print(smoke_val)
	#print(time)
	# print(time)
	# flame_val.reverse()
	# smoke_val.reverse()
	# time.reverse()
	return render(request,'graph.html',{'flame_val1': flame_val1,'smoke_val1':smoke_val1,'time':time,
	'flame_val2': flame_val2,'smoke_val2':smoke_val2})
	#return render(request,'graph.html',{'flame_val': flame_val,'smoke_val':smoke_val})

def send_fire_alert(request):
	subject = 'FIRE ALERT🔥🔥🔥'
	message = f'Hi vamsi,\n Warning: This is fire alert. Fire is detected!!!\nBe cautious and take necessary actions...\nSmoke value1: 560\nFlame value1: 0\nSmoke value2:582\nFlame value2:1\n'
	email_from = settings.EMAIL_HOST_USER
	recipient_list = ["pravallikakodi26@mail.com"]
	send_mail( subject, message, email_from, recipient_list)
	return redirect('dashboard')


# From : "iit2019234@iiita.ac.in",
# Subject : "FIRE ALERT🔥🔥🔥",
# Body : "Warning: This is fire alert. Fire is detected!!!<br/> Be cautious and take necessary actions...<br/> "+
# "flame_value1: "+flame1+"<br/>smoke_value1: "+smoke1+"<br/>flame_value2: "+flame2+"<br/>smoke_value2: "+smoke2



