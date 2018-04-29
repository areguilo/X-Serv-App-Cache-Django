from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from cache.models import Page
from django.views.decorators.csrf import csrf_exempt
import urllib.request

form = """<form action="" method = "POST"><input type="text" name='url' value=""><br><input type="submit"value="Enviar"></form>"""

@csrf_exempt

def barra(request):

    if request.method == "POST":
        url = request.POST['url']
        if url == "":
            response = '<h1> No url introduced </h1><br>'+'<a href=http://localhost:8000/ >Return to Main Menu</a>'
            return HttpResponse(response)

        elif url.find("http://")==-1 and url.find("https://")==-1:
            url = "https://" + url

        try:
            page = Page.objects.get(name = url)
            response = '<h1> page already saved in cache </h1><br>' + '<a href=http://localhost:8000/ >Return to Main Menu</a>'
            return HttpResponse(response)
        except Page.DoesNotExist:
            content = (urllib.request.urlopen(url)).read()
            page = Page(name= url, page=content)
            page.save()

    response = '<ul><h2>'
    list = Page.objects.all()
    for item in list:
        print(item.name)
        response = response + '<li><a href=http://localhost:8000/' + str(item.name) + ">" + item.name + '</a></li>'
    response = response + '</ul></h2>' + '<h2>Add page</h2>'
    response = "<h1>Hi!, these are our contents managed:</h1>" + response + form
    return HttpResponse(response)

def get(request, name):
    try:
        page = Page.objects.get(name=name)
    except Page.DoesNotExist:
        return HttpResponse('<h1> La pagina no se encuentra en la cache </h1><br>' +'<a href=http://localhost:8000/ >Return to Main Menu</a>')
    response = page.page
    return HttpResponse(response)
