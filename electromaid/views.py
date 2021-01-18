from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.views import View
from .forms import Register, Support, Login, DatePicker
from .models import blog_request, Auth, Control_properties, Usage_properties
from django.core.mail import send_mail
from django.conf import settings
import json


def index(request):
    return render(request, 'electromaid/landing.html')


def blog(request):
    post = blog_request()
    oid_list = list()
    for i in range(post.__len__()):
        oid_list.append(post[i].get('_id').get('$oid'))

    print(oid_list)
    return render(request, 'electromaid/blog.html', {
        'posts': post,
        'oid': oid_list
    })


# def blog_id(request, id):
#     post = blog_request()
#     print(id)
#     return render(request, 'electromaid/blog_id.html', {'posts': post, 'id':id})


def pricing(request):
    return render(request, 'electromaid/pricing.html')


def learn_more(request):
    return render(request, 'electromaid/learn.html')


class Contact(View):
    form = Support

    def get(self, request):
        return render(request, 'electromaid/contact.html', {'form': self.form})

    def post(self, request):
        form = self.form(request.POST)
        data = self.request.POST
        print(data)
        if form.is_valid():
            print("Form valid")
            self.get_params()
            render(request, 'electromaid/contact.html', {
                'form': self.form,
                'status': 'success'
            })
        else:
            render(request, 'electromaid/contact.html', {
                'form': self.form,
                'status': 'failed'
            })

    def get_params(self):
        params = self.request.POST
        print("Halo")
        name = str(params['first_name']) + ' ' + str(params['last_name'])
        print(params)
        from_email = settings.EMAIL_HOST_USER
        to_email = str(params['email'])
        message = str(params['message'])
        send_mail('Message from customer', message, to_email, [from_email])
        print('terkirim')


class Login_view(View):
    form = Login
    auth = Auth()

    def get(self, request):
        return render(request, 'electromaid/auth/login.html',
                      {'form': self.form})

    def post(self, request):
        form = self.form(request.POST)
        if form.is_valid():
            params = self.request.POST
            self.auth.set_email(params['email'])
            self.auth.set_password(params['password'])

            if self.auth.login():
                self.request.session['email'] = self.auth.get_email()
                return HttpResponseRedirect('/electromaid/dashboard/usage')
            return HttpResponseRedirect('/electromaid/')
        else:
            return render(request, "electromaid/auth/login.html",
                          {'form': form})


class Register_view(View):
    form = Register
    auth = Auth()

    def get(self, request):
        return render(request, 'electromaid/auth/register.html',
                      {'form': self.form})

    def post(self, request):
        form = self.form(request.POST)
        if form.is_valid():
            params = self.request.POST
            self.auth.name = str(params['first_name']) + str(
                params['last_name'])
            self.auth.email = str(params['email'])
            self.auth.password = str(params['password'])
            self.auth.register()
            return HttpResponseRedirect('/electromaid/')
        else:
            return render(request, "electromaid/auth/register.html",
                          {'form': form})


class Usage(View):
    properties = Usage_properties()
    watt = 0

    def get(self, request):
        if 'email' in request.session:
            date = DatePicker
            self.properties.get_data()
            id = self.properties.get_id()
            master_id = self.properties.get_master_id()
            device = self.properties.get_device_by_id()
            for dev in device:
                self.watt += round(float(dev.get('daya')), 2)
            payment = self.payment()
            print(self.watt)
            return render(
                request, "electromaid/dashboard/usage.html", {
                    'id': id,
                    'master_id': master_id,
                    'watt': self.watt,
                    'payment': payment,
                    'devices': device,
                    'date_picker': date
                })
        else:
            return HttpResponseRedirect('/electromaid/')

    def payment(self):
        print(round(self.watt * 1447 / 1000))
        return round(self.watt * 1447 / 1000)


class Control_view(View):
    properties = Control_properties()
    response = ""

    def get(self, request):
        if 'email' in request.session:
            return render(request, "electromaid/dashboard/control.html",
                          {'devices': self.properties.get_device()})
        else:
            return HttpResponseRedirect('/electromaid/')

    def post(self, request):
        data = request.POST.copy()
        del data['csrfmiddlewaretoken']
        if data.get('action'):
            self.properties.get_from_data(data)
            self.properties.delete_data()
        else:
            payload = {'device': data}
            print(payload)
            self.properties.get_from_data(data)
            self.response = self.properties.put_data()
        if self.response:
            response = 'success'
            return render(request, "electromaid/dashboard/control.html",
                          {'devices': self.properties.get_device(), 'response': response})
        else:
            return JsonResponse({'response': 'failed'})


def logout(request):
    try:
        del request.session['email']
        print("session deleted")
    except KeyError:
        print("session not deleted")
        pass
    finally:
        return HttpResponseRedirect('/electromaid/')
