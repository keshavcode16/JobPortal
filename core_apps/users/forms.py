from decimal import Decimal
from django import forms as d_forms
from allauth.account.forms import SignupForm, LoginForm
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.db.models import Q, Sum
from crispy_forms.layout import Layout, Field, Div, HTML, Submit, Row,Column, Button, ButtonHolder  # Fieldset, ButtonHolder
from crispy_forms.helper import FormHelper
from django.apps import apps
from .models import User, UserGroup, Employer, JobSeeker
from django.utils.translation import gettext as _ , gettext_lazy as trans
import re
import json
from core_apps.common.models import Skill, Qualification 

    

class AuthForm(d_forms.Form):
    username = d_forms.CharField(label='Username')
    password = d_forms.CharField(label='Password', widget=d_forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(AuthForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-indigo-600 focus:border-indigo-600 block w-full p-2.5',
                'placeholder': field.label,
            })

        self.helper = FormHelper()
        self.helper.attrs = {'class': 'space-y-4 md:space-y-6'}
        self.helper.layout = Layout(
            HTML(
                f"""
                <div class="text-left">
                    <label for="id_username" class="block mb-2 text-sm font-medium text-gray-900 requiredField">Username</label>
                    {self['username']}
                </div>
                <div class="text-left">
                <label for="password" class="block mb-2 text-sm font-medium text-gray-900 requiredField">Password</label>
                {self['password']}
                </div>
                <button
                type="submit"
                class="w-full text-white bg-indigo-600 hover:bg-indigo-700 focus:ring-4 focus:outline-none focus:ring-indigo-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center"
                >
                Sign In
                </button>
                <p class="text-sm font-light text-gray-500">
                Already have an account
                <a class="font-medium text-indigo-600 hover:underline" href="/">Sign Up</a>
                </p>
            """
            ),
        )
        
        self.fields['username'].required = True
        self.fields['password'].required = True

    def clean(self):
        cleaned_data = super().clean()
        cleaned_username =  cleaned_data.get('username',None)
        cleaned_username = cleaned_username.strip()
        password = cleaned_data.get('password')
        # validations for password field
        reg = r'^(?=.*\d)(?=.*[a-zA-Z]).{8,}$'
        if not re.match(reg, password):
            raise d_forms.ValidationError("Password must be alphanumeric and contain at least 8 characters including a special character.")
        
        return cleaned_data
    
    
    

class CreateEmployerForm(d_forms.ModelForm):
    password = d_forms.CharField(label='Password', widget=d_forms.PasswordInput)
    password2 = d_forms.CharField(label='Confirm Password', widget=d_forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(CreateEmployerForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-indigo-600 focus:border-indigo-600 block w-full p-2.5',
                'placeholder': field.label,
            })
        

        self.helper = FormHelper()


        self.helper.layout = Layout(
            HTML(
                f"""<div class="text-left">
                        <label for="id_first_name" class="block mb-2 text-sm font-medium text-gray-900 requiredField">First Name</label>
                        {self['first_name']}
                    </div>
                    <div class="text-left">
                        <label for="id_last_name" class="block mb-2 text-sm font-medium text-gray-900 requiredField">Last Name</label>
                        {self['last_name']}
                    </div>
                    </div>
                    <div class="text-left">
                    <label for="id_email" class="block mb-2 text-sm font-medium text-gray-900 requiredField">Your email</label>
                    {self['email']}
                    </div>
                    <div class="grid grid-cols-2 gap-4">
                    <div class="text-left">
                        <label for="id_username" class="block mb-2 text-sm font-medium text-gray-900 requiredField">Username</label>
                        {self['username']}
                    </div>
                    <div class="text-left">
                        <label for="id_company_name" class="block mb-2 text-sm font-medium text-gray-900 requiredField">Company Name</label>
                        {self['company_name']}
                    </div>
                    </div>
                    <div class="text-left">
                    <label for="password" class="block mb-2 text-sm font-medium text-gray-900 requiredField">Password</label>
                    {self['password']}
                    </div>
                    <div class="text-left">
                    <label for="id_password2" class="block mb-2 text-sm font-medium text-gray-900 requiredField">Confirm Password</label>
                    {self['password2']}
                    </div>
                    <button
                    type="submit"
                    class="w-full text-white bg-indigo-600 hover:bg-indigo-700 focus:ring-4 focus:outline-none focus:ring-indigo-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center"
                    >
                    Register
                    </button>
                    <p class="text-sm font-light text-gray-500">
                    Already have an account
                    <a class="font-medium text-indigo-600 hover:underline" href="/auth/login">Sign In</a>
                    </p>
            """
            ),
        )
        
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['username'].required = True
        self.fields['email'].required = True
        self.fields['company_name'].required = True
        self.fields['password'].required = True
        self.fields['password2'].required = True  # Set password2 as required

    def clean(self):
        cleaned_data = super().clean()
        cleaned_email =  cleaned_data.get('email',None)
        cleaned_email = cleaned_email.strip()
        cleaned_username =  cleaned_data.get('username',None)
        if cleaned_email is not None and cleaned_username is not None:
            employer_qs = User.objects.filter(Q(email=cleaned_email) | Q(username=cleaned_username))
            if employer_qs.exists():
                raise d_forms.ValidationError("Email or Username is already registered with another account.")

        if not cleaned_data['first_name'].isalpha():
            raise d_forms.ValidationError("Please use right format in the Name Field. (E.g. James)")

        if not cleaned_data['last_name'].isalpha():
            raise d_forms.ValidationError("Please use right format in the Name Field. (E.g. Willam)")

        # validations for email field
        if cleaned_email:
            reg = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            if not (re.fullmatch(reg, cleaned_email)):
                raise d_forms.ValidationError("Please enter valid email id. (E.g: youremail@example.com)")
        
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')
        if password and password2 and password != password2:
            raise d_forms.ValidationError("Password didn't match!")

        if self.instance.pk:
            pass
        return cleaned_data


    class Meta:
        model = Employer
        fields = ("first_name", "last_name", "email",
                  "username", "company_name", "password")


class UpdateEmployerForm(d_forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UpdateEmployerForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'border-1 rounded-r px-4 py-2 w-full',
                'placeholder': field.label,
            })

        self.helper = FormHelper()

        self.helper.layout = Layout(
            HTML(
                f"""<div class="pb-6">
                        <label for="name" class="font-semibold text-gray-700 block pb-1">Name</label>
                        <div class="flex">
                            {self['first_name']}
                        </div>
                    </div>
                    <div class="pb-6">
                        <label for="name" class="font-semibold text-gray-700 block pb-1">Name</label>
                        <div class="flex">
                            {self['last_name']}
                        </div>
                    </div>
                    <div class="pb-6">
                        <label for="name" class="font-semibold text-gray-700 block pb-1">Name</label>
                        <div class="flex">
                            {self['email']}
                        </div>
                    </div>
                    <div class="pb-6">
                        <label for="name" class="font-semibold text-gray-700 block pb-1">Name</label>
                        <div class="flex">
                            {self['username']}
                        </div>
                    </div>
                    <div class="pb-6">
                        <label for="name" class="font-semibold text-gray-700 block pb-1">Name</label>
                        <div class="flex">
                            {self['company_name']}
                        </div>
                    </div>
                    <button
                        type="submit"
                        data-ripple-light="true"
                        class="align-middle select-none font-sans font-bold text-center uppercase transition-all disabled:opacity-50 disabled:shadow-none disabled:pointer-events-none text-xs py-3 px-6 rounded-lg bg-gray-900 text-white shadow-md shadow-gray-900/10 hover:shadow-lg hover:shadow-gray-900/20 focus:opacity-[0.85] focus:shadow-none active:opacity-[0.85] active:shadow-none"
                        >
                        Save Changes
                    </button>
                """
            ),
        )

        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['username'].required = True
        self.fields['email'].required = True
        self.fields['company_name'].required = True

    def clean(self):
        cleaned_data = super().clean()
        cleaned_email = cleaned_data.get('email', None)
        cleaned_email = cleaned_email.strip()
        cleaned_username = cleaned_data.get('username', None)
        if cleaned_email is not None and cleaned_username is not None:
            employer_qs = User.objects.filter(Q(email=cleaned_email) | Q(username=cleaned_username)).exclude(pk=self.instance.pk)
            if employer_qs.exists():
                raise d_forms.ValidationError("Email or Username is already registered with another account.")

        if not cleaned_data['first_name'].isalpha():
            raise d_forms.ValidationError("Please use right format in the Name Field. (E.g. James)")

        if not cleaned_data['last_name'].isalpha():
            raise d_forms.ValidationError("Please use right format in the Name Field. (E.g. William)")

        # validations for email field
        if cleaned_email:
            reg = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            if not (re.fullmatch(reg, cleaned_email)):
                raise d_forms.ValidationError("Please enter valid email id. (E.g: youremail@example.com)")

        return cleaned_data

    class Meta:
        model = Employer
        fields = ("first_name", "last_name", "email", "username", "company_name")



class JobSeekerForm(d_forms.ModelForm):
    password = d_forms.CharField(label='Password', widget=d_forms.PasswordInput, required=False)
    password2 = d_forms.CharField(label='Confirm Password', widget=d_forms.PasswordInput, required=False)
    primary_skills = d_forms.ModelMultipleChoiceField(queryset=Skill.objects.all(), widget=d_forms.SelectMultiple(attrs={'class': 'select2 w-full py-2 bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-indigo-600 focus:border-indigo-600'}))

    def __init__(self, *args, **kwargs):
        super(JobSeekerForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-indigo-600 focus:border-indigo-600 block w-full p-2.5',
                'placeholder': field.label,
            })

        self.helper = FormHelper()
        self.helper.layout = Layout(
            HTML(
                f"""<div class="text-left">
                    <label for="id_first_name" class="block mb-2 text-sm font-medium text-gray-900 requiredField">First Name</label>
                    {self['first_name']}
                  </div>
                  <div class="text-left">
                    <label for="id_last_name" class="block mb-2 text-sm font-medium text-gray-900 requiredField">Last Name</label>
                    {self['last_name']}
                  </div>
                  <div class="text-left">
                    <label for="id_email" class="block mb-2 text-sm font-medium text-gray-900 requiredField">Your email</label>
                    {self['email']}
                  </div>
                  <div class="text-left">
                    <label for="id_username" class="block mb-2 text-sm font-medium text-gray-900 requiredField">Username</label>
                    {self['username']}
                  </div>
                  <div class="text-left">
                    <label for="id_primary_skills" class="block mb-2 text-sm font-medium text-gray-900 requiredField">Primary Skill</label>
                    {self['primary_skills']}
                  </div>
                  <div class="text-left">
                    <label for="id_higher_qualification" class="block mb-2 text-sm font-medium text-gray-900 requiredField">Higher Qualification</label>
                    {self['higher_qualification']}
                  </div>
                """
            ),
        )

        # Conditionally add password fields for creation
        if not self.instance.pk:
            self.fields['password'].required = True
            self.fields['password2'].required = True
            self.helper.layout.extend([
                HTML(
                    f"""<div class="text-left">
                        <label for="password" class="block mb-2 text-sm font-medium text-gray-900 requiredField">Password</label>
                        {self['password']}
                      </div>
                      <div class="text-left">
                        <label for="id_password2" class="block mb-2 text-sm font-medium text-gray-900 requiredField">Confirm Password</label>
                        {self['password2']}
                      </div>
                      <button
                        type="submit"
                        class="w-full text-white bg-indigo-600 hover:bg-indigo-700 focus:ring-4 focus:outline-none focus:ring-indigo-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center"
                        >
                        Register
                      </button>
                    """
                ),
            ])
        else:
            # Remove password fields for update
            self.fields.pop('password')
            self.fields.pop('password2')
            self.helper.layout.extend([
                HTML(
                    f"""<button
                        type="submit"
                        class="w-full text-white bg-indigo-600 hover:bg-indigo-700 focus:ring-4 focus:outline-none focus:ring-indigo-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center"
                        >
                        Update Profile
                      </button>
                    """
                ),
            ])

    def clean(self):
        cleaned_data = super().clean()
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')
        email = cleaned_data.get('email')
        username = cleaned_data.get('username')

        if not first_name.isalpha():
            self.add_error('first_name', "Please use the correct format in the Name Field. (E.g. James)")

        if not last_name.isalpha():
            self.add_error('last_name', "Please use the correct format in the Name Field. (E.g. Willam)")

        if not email:
            raise d_forms.ValidationError("Please enter an Email to continue.")

        email = email.strip()

        if email and username:
            if JobSeeker.objects.filter(Q(email=email) | Q(username=username)).exclude(pk=self.instance.pk).exists():
                raise d_forms.ValidationError("Email or Username is already registered with another job seeker.")

        if email:
            email_reg = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            if not re.fullmatch(email_reg, email):
                raise d_forms.ValidationError("Please enter a valid email id. (E.g: youremail@example.com)")

        # Password validation for creation
        if not self.instance.pk:
            password = cleaned_data.get('password')
            password2 = cleaned_data.get('password2')

            if not password:
                raise d_forms.ValidationError("Password is required.")

            if password != password2:
                raise d_forms.ValidationError("Passwords do not match.")

            # Additional password strength validation
            reg = r'^(?=.*\d)(?=.*[a-zA-Z]).{8,}$'
            if not re.match(reg, password):
                raise d_forms.ValidationError("Password must be alphanumeric and contain at least 8 characters including a special character.")

        return cleaned_data

    class Meta:
        model = JobSeeker
        fields = ("first_name", "last_name", "email", "username", "primary_skills", "higher_qualification")



