from django import forms
from .models import GeneralPost
import re
from django.contrib import admin
from ckeditor.widgets import CKEditorWidget



class GeneralPostCreateAlterForm(forms.ModelForm):
	title = forms.CharField(label='Enter Title',max_length=100)
	content = forms.CharField(label='Enter Content',max_length=1000, widget=CKEditorWidget())
	tag = forms.CharField(label='Tag',max_length=100)
	class Meta:
		model = GeneralPost
		fields = ('title','content')

	def clean_tag(self):
		data = self.cleaned_data['tag']
		print(data)
		tag_list = re.findall(r'(?<!#)[#]{1}[\w]+', data)
		print(tag_list)
		subtracted_data = re.sub(r'(?<!#)[#]{1}[\w]+', '', data)
		print(subtracted_data)
		subtracted_data = re.sub(r' ', '', subtracted_data)
		print(subtracted_data)
		if len(tag_list) > 10:
			raise forms.ValidationError("No more than 10 Tags!")
		if subtracted_data:
			raise forms.ValidationError("Hash tag must have only one Hash")		
		tag_list = set(tag_list)
		return tag_list



class GeneralPostDeleteForm(forms.ModelForm):

	class Meta:
		model = GeneralPost
		fields = ()

