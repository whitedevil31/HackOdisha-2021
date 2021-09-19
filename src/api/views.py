from django.http import HttpResponse
from django.http import response
from django.http.response import HttpResponseRedirect
from django.template import loader
from django.shortcuts import render,redirect
from .forms import NameForm
from django.urls import reverse
from django.core.mail import EmailMessage
from django.views.decorators.csrf import csrf_exempt


# sys.path.append('../')
# from django.core.mail import EmailMessage
import time
from .nlp import search 
# from .temp import testing
def formView(request):
    #nlp funct -> web scrap -> return 1->file created -> return 1 -> create download link
  
    return render(request,'success.html')


# def baseView(request):
#     form = NameForm(request.POST)
#     if request.method=="POST" and form.is_valid():
#         url = form.cleaned_data['url']
#         value=search(url)
#         if value==1:
#             return redirect('/success')
#     return render(request,'index.html')
@csrf_exempt
def baseView(request):
    form = NameForm(request.POST)
    if request.method=="POST" and form.is_valid():
        url = form.cleaned_data['url']
        email = form.cleaned_data['email']

        value = search(url)
        #email= EmailMessage('django test mail','django body','magz3116@gmail.com',['np6771@srmist.edu.in'])
        #email.attach_file('final_list1.csv')
        #email.send()
        # value=search(url)
        if value==1:
            email= EmailMessage('django test mail','django body','magz3116@gmail.com',[email])
            email.attach_file('final_list1.csv')
            email.send()
            with open("final_list1.csv","r+") as v:
                v.truncate(0)
            return redirect('/success')
    return render(request,'index.html')    





