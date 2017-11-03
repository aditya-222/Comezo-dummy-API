# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from mongoengine import *
from models import *
import datetime
import json
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

def test(request):
	return HttpResponse('Comezo app running successfully')

def read(request):
	comezo_data = []
	reponse_data = {'response':[],'error': 0 , 'error_msg':''}
	item_per_page = 3
	try:
		if request.method == 'GET':
			tag_value = request.GET.get('tag','')
			question_id = request.GET.get('id','')
			text_match = request.GET.get('text','')
			page_number = request.GET.get('page','1')
			offset = (int(page_number)-1)*item_per_page
			if question_id:
				question_data = comezo_questions.objects(id = str(question_id))
			elif tag_value :
				question_data = comezo_questions.objects(tags = tag_value).skip( offset ).limit(item_per_page)	
			elif text_match:
				question_data = comezo_questions.objects(question_text__contains = text_match)
			elif tag_value == '' and question_id == '' and text_match== '':
				question_data = comezo_questions.objects.skip( offset ).limit(item_per_page)
			if question_data:
				for question in question_data:
					comezo_dict = {}
					comezo_dict['created_by'] = question.created_by
					comezo_dict['created_at'] = question.created_at
					comezo_dict['modified_at'] = question.modified_at
					comezo_dict['question_text'] = question.question_text
					comezo_dict['tags'] = question.tags
					comezo_dict['answers'] = question.answers
					comezo_dict['hints'] = question.hints
					comezo_data.append(comezo_dict)
				reponse_data['response'] = comezo_data 
				json_data = json.dumps(reponse_data , indent = 2)
				return HttpResponse(json_data, content_type='application/json')
			else:
				raise Exception('no result found for the search parameter')
	except Exception, e :
		reponse_data['error'] = 1
		reponse_data['error_msg'] = str (e)
		json_data = json.dumps(reponse_data , indent = 2)
		return HttpResponse (json_data , content_type='application/json')

@csrf_exempt
def create(request):
	reponse_data = {'response':'Okay','error': 0}
	try:
		if request.method == 'POST':
			question = comezo_questions()
			question.question_text = request.POST['question_text'] 
			question.tags = (request.POST['tags']).split(',')
			question.answers = (request.POST['answers']).split(',')
			question.hints = request.POST['hints']
			question.created_at = datetime.datetime.now().isoformat()
			question.modified_at = ''
			question.created_by = request.POST['created_by']
			question.save() 
			json_data = json.dumps(reponse_data , indent = 2)
			return HttpResponse(json_data, content_type='application/json')
	except Exception , e:
		reponse_data['error'] = 1
		reponse_data['response'] = str (e)
		json_data = json.dumps(reponse_data , indent = 2)
		return HttpResponse (json_data , content_type='application/json')

@csrf_exempt
def update(request):
	reponse_data = {'response':'Okay','error': 0 }
	try:
		if request.method == 'POST':
			question_id = request.GET.get('id','')
			question_tag = request.GET.get('tag','')
			if question_id :
				question_data = comezo_questions.objects(id = str(question_id))
			if question_data:
				for question in question_data:
					for key,value in request.POST.items():
						if key == 'question_text' and value != '':
							question.question_text = value
						if key == 'answers' and value != '':
							answers_list = value.split(',')
							question.answers = answers_list
						if key == 'tags' and value != '':
							tags_list = value.split(',')
							question.tags = tags_list
						if key == 'hints' and value != '':
							question.hints = value
					question.modified_at = datetime.datetime.now().isoformat()
					question.save()
				json_data = json.dumps(reponse_data , indent = 2)
				return HttpResponse(json_data, content_type='application/json')
			else: 
				raise Exception("No record found with given id")
	except Exception,e:
		reponse_data['error'] = 1
		reponse_data['response'] = str (e)
		json_data = json.dumps(reponse_data , indent = 2)
		return HttpResponse (json_data , content_type='application/json')