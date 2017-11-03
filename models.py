# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from mongoengine import *

# Create your models here.

class comezo_questions(Document):
	created_by = StringField()
	created_at = StringField()
	modified_at = StringField()
	question_text = StringField()
	tags = ListField()
	answers = ListField()
	hints = StringField()


class comezo_tags(Document):
	name = StringField()
	type = StringField()
