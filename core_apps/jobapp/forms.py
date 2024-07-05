from decimal import Decimal
from django import forms as d_forms
from allauth.account.forms import SignupForm, LoginForm
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.db.models import Q, Sum
from crispy_forms.layout import Layout, Field, Div, HTML, Submit, Row,Column, Button, ButtonHolder  # Fieldset, ButtonHolder
from crispy_forms.helper import FormHelper
from django.apps import apps
from .models import JobPost
from django.utils.translation import gettext as _ , gettext_lazy as trans
import re
import json
from core_apps.common.models import Skill, Qualification 




class CreateJobPostForm(d_forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        self.created_by = kwargs.pop('created_by', False)
        super(CreateJobPostForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-indigo-600 focus:border-indigo-600 block w-full p-2.5',
                'placeholder': field.label,
            })
            
        self.fields['skills'].widget.attrs.update({
            'multiple': 'multiple',
            'class': 'bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-indigo-600 focus:border-indigo-600 block w-full p-2.5',
        })
        
        self.helper = FormHelper()
        self.helper.layout = Layout(
            HTML(
                f"""<div class="text-left  mb-4"">
                    <label for="id_title" class="block mb-2 text-sm font-medium text-gray-900 requiredField">Title</label>
                    {self['title']}
                </div>
                <div class="text-left  mb-4"">
                    <label for="id_skills" class="block mb-2 text-sm font-medium text-gray-900 requiredField">Skills</label>
                    {self['skills']}
                </div>
                <div class="text-left mb-4">
                    <label class="block mb-2 text-sm font-medium text-gray-900 requiredField">Experience</label>
                    <div class="flex space-x-4">
                        <div class="flex-1">
                        {self['experience_years']}
                        </div>
                        <div class="flex-1">
                        {self['experience_months']}
                        </div>
                    </div>
                </div>
                <div class="text-left  mb-4"">
                <label for="description" class="block mb-2 text-sm font-medium text-gray-900 requiredField">Description</label>
                {self['description']}
                </div>
                <button
                    type="submit"
                    data-ripple-light="true"
                    class="align-middle select-none font-sans font-bold text-center uppercase transition-all disabled:opacity-50 disabled:shadow-none disabled:pointer-events-none text-xs py-3 px-6 rounded-lg bg-gray-900 text-white shadow-md shadow-gray-900/10 hover:shadow-lg hover:shadow-gray-900/20 focus:opacity-[0.85] focus:shadow-none active:opacity-[0.85] active:shadow-none"
                    >
                    Create Job Post
                </button>
            """
            ),
        )
        
        self.fields['title'].required = True
        self.fields['skills'].required = True
        self.fields['experience_years'].required = True
        self.fields['experience_months'].required = True
        self.fields['description'].required = True
          

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data


    class Meta:
        model = JobPost
        fields = ("title", "skills", "experience_years", "experience_months", "description")
        widgets = {
            'skills': d_forms.SelectMultiple()
        }
    