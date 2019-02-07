from django import forms
import re
from django.contrib import admin
from .models import GeneralPost


class GeneralPostCreateAlterForm(forms.ModelForm):
	title = forms.CharField(label='Enter Title',max_length=100)
	content = forms.CharField(label='Enter Content',max_length=10000)
	tag = forms.CharField(label='Tag',max_length=100)
	class Meta:
		model = GeneralPost
		fields = ('title','content')

	def clean_tag(self):
		data = self.cleaned_data['tag']
		tag_list = re.findall(r'(?<!#)[#]{1}[\w]+', data)
		subtracted_data = re.sub(r'(?<!#)[#]{1}[\w]+', '', data)
		subtracted_data = re.sub(r' ', '', subtracted_data)
		if len(tag_list) > 10:
			raise forms.ValidationError("No more than 10 Tags!")
		if subtracted_data:
			raise forms.ValidationError("Hash tag must have only one Hash")
		tag_list = set(tag_list)
		return tag_list

		title = self.cleaned_data['title']


class GeneralPostDeleteForm(forms.ModelForm):

	class Meta:
		model = GeneralPost
		fields = ()