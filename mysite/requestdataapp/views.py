from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from django.http import *

from  .forms import *
# Create your views here.
def process_get_view(request: HttpRequest) -> HttpResponse:
    a=request.GET.get('a','')
    b=request.GET.get('b','')
    result=a+b
    context = {
        'a': a,
        'b': b,
        'result': result
    }
    return render(request, "requestdataapp/request-query-params.html", context=context)


def user_form_view(request: HttpRequest) -> HttpResponse:
    context = {
        'form': UserBioForm(),

    }
    return render(request,  "requestdataapp/user-bio-form.html", context=context)


def handle_file_upload(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            #     name = form.cleaned_data['name']
            #     price = form.cleaned_data['price']
            myfile = form.cleaned_data['file']
            print(myfile.name)
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            print(filename)
    else:
        form = UploadFileForm()
    context = {
        "form": form,
    }
    return render(request, "requestdataapp/file-upload.html", context=context)