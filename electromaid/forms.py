from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.core.mail import send_mail
from bootstrap_datepicker_plus import DatePickerInput


class Register(forms.Form):
    first_name = forms.CharField(label='First Name', widget=forms.TextInput())
    last_name = forms.CharField(label='Last Name')
    email = forms.CharField(label='Email Address', widget=forms.EmailInput())
    password = forms.CharField(widget=forms.PasswordInput, label='Password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = 'contact-form'
        self.helper.field_class = 'col-md-6'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit', css_class='btn-success mt-3'))


class Login(forms.Form):
    email = forms.CharField(label='Email')
    password = forms.CharField(label='Password', widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super(Login, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = 'login-form'
        self.helper.form_class = ' d-grip gap-2 '
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Login', css_class='btn btn-success mt-3 btn-lg'))


class Support(forms.Form):
    first_name = forms.CharField(label='First Name')
    last_name = forms.CharField(label='Last Name')
    email = forms.CharField(widget=forms.EmailInput(), label='Email')
    message = forms.CharField(widget=forms.Textarea(), label='Message')
    


class DatePicker(forms.Form):
    date = forms.DateField(
        widget=DatePickerInput(format='%m/%d/%Y')
    )
