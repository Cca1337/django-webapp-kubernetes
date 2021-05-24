import os
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, StreamingHttpResponse
from .models import ToDoList, Item, Note, Picture
from .forms import CreateNewList
from django.contrib import messages
from .engine.weather_forecast import get_weather_scrape
from .engine.weather_forecast_API import get_weather_api
from .engine.stock_prediction import stock_price_prediction
from .engine.face_detection import generate
from .engine.eye_detection import generate1
import json
from django.http import JsonResponse
from django.http import FileResponse

import cloudinary.api

from . import ALLOWED_EXTENSIONS

# Create your views here.

from django.contrib.auth.decorators import login_required


def home(response):
    return render(response, "main/home.html", {})

def index(response, id):
    ls = ToDoList.objects.get(id=id)

    if response.method == "POST":

        if response.POST.get("save"):
            for item in ls.item_set.all():
                if response.POST.get("c" + str(item.id)) == "clicked":
                    item.complete = True

                else:
                    item.complete = False

                item.save()

        elif response.POST.get("newItem"):
            txt = response.POST.get("new")

            if len(txt) > 2:
                ls.item_set.create(text=txt, complete=False)
            else:
                print("invalid")


    return render(response, "main/list.html", {"ls": ls})

def create(response):

    if response.method == 'POST':
        form = CreateNewList(response.POST)

        if form.is_valid():
            n = form.cleaned_data["name"]
            t = ToDoList(name=n)
            t.save()
            response.user.todolist_add(t)


        return HttpResponseRedirect("/%i" %t.id)

    else:

        form = CreateNewList()
    return render(response, "main/create.html", {"form": form})

def view(response):
    return render(response, "main/view.html", {})


def gallery(response):
    return render(response, "main/gallery.html", {})

def gallery3d(response):
    return render(response, "main/3dgallery.html", {})

def videos(response):
    return render(response, "main/videos.html", {})

def carousel(response):
    return render(response, "main/carousel.html", {})

def scrape(response):

    if response.method == "POST":
       mesto = response.POST.get("mesto")

       if len(mesto) < 1:
           messages.error(response, "I bet there is no city which such a short name! [%s]." % mesto)
       else:
           try:
               pocasie = get_weather_scrape(mesto)
               messages.success(response, f"{pocasie}")
               return render(response, "main/scrape.html", {})

           except AttributeError as err:
               messages.error(response, f"[ERROR] Problem with city name: [{mesto}]. Try again!")
               return render(response, "main/scrape.html", {})


    return render(response, "main/scrape.html", {})

def weather(response):

    if response.method == "POST":
       mesto = response.POST.get("mesto")

       if len(mesto) < 1:
           messages.error(response, "I bet there is no city which such a short name! [%s]." % mesto)
       else:
           try:
               pocasie = get_weather_api(mesto)
               messages.success(response, f"{pocasie}")
               return render(response, "main/scrape.html", {})

           except KeyError as err:
               messages.error(response, f"[ERROR] Problem with city name: [{mesto}]. Try again!")
               return render(response, "main/scrape.html", {})


    return render(response, "main/scrape.html", {})

def prediction(response):

    if response.method == "POST":

        days = response.POST.get('days')
        company = response.POST.get('company')
        try:
            days = int(days)

        except ValueError as err:
            messages.error(response, f"[ERROR]Cant translate {days} to Int")

        if days == 0:
            messages.error(response, f"You cant get the prediction for 0 days")

        elif len(company) > 7 or len(company) < 2:
            messages.error(response, f"You put [{company}] as a company ticker name which doesnt work")

        elif days == "":
            messages.error(response, f"You cant get the prediction for empty field")

        else:
            prediction, last_value, filepath = stock_price_prediction(days, company)
            link = f"{filepath}/{company}_{days}_prediction.png"
            messages.success(response, f"You asked for Stock market value prediction after {days}(day/s) for {company} company! Result is {prediction}. Last known value is {last_value}")
            return render(response, "main/vysledok.html", {"last_value": last_value,
                                                           "prediction": prediction,
                                                           "company": company,
                                                           "days": days,
                                                           "link": link})

    return render(response, "main/stocks-prediction.html", {})


def face_detection(response):

    if response.method == "POST":
        boolean = True
        messages.success(response, f"Face detection started!")
        img = StreamingHttpResponse(generate(), content_type='multipart/x-mixed-replace; boundary=frame')
        return render(response, "main/face_detection.html", {"boolean": boolean, "img": img})

    else:

        return render(response, "main/face_detection.html", {})

def video_feed(response):

    return StreamingHttpResponse(generate(), content_type='multipart/x-mixed-replace; boundary=frame')



def eye_detection(response):

    if response.method == "POST":
        boolean = True
        messages.success(response, f"Eye detection started!")
        img = StreamingHttpResponse(generate1(), content_type='multipart/x-mixed-replace; boundary=frame')
        return render(response, "main/eye_detection.html", {"boolean": boolean, "img": img})

    else:

        return render(response, "main/eye_detection.html", {})

def video_feed1(response):

    return StreamingHttpResponse(generate1(), content_type='multipart/x-mixed-replace; boundary=frame')


#------------------------------------------UPLOAD FILES---------------
@login_required(login_url='/login/')
def upload(response):

    if response.method == "POST":

        current_user = response.user

        file = response.FILES['inputFile']
        mimetype = file.content_type.split('/')[-1]

        if file.size > 20000:
            messages.error(response, "File is toooo big!")


        elif mimetype not in ALLOWED_EXTENSIONS:

            messages.error(response, "Filetype is not supported!")


        else:
            description = response.POST.get("text")
            picturename = file

            new_picture = Picture(user_id=current_user.id, name=picturename,
                                  description=description, mimetype=mimetype,
                                  file=file)
            new_picture.save()
            messages.success(response, "File saved to DB")


    return render(response, "main/upload.html", {})


@login_required(login_url='/login/')
def obrazky_update(response):

    current_user = response.user
    allpictures = Picture.objects.all()
    userpictures = Picture.objects.filter(user__id=current_user.id).values()

    return render(response, 'main/obrazky_update.html', {"userpictures": userpictures})


@login_required(login_url='/login/')
def return_files(response, filename):

    image = Picture.objects.get(name=filename)
    file_path = image.file.url
    split = file_path.split("/")[6]
    insert = file_path.find(split)

    serve_file = file_path[:insert] + "fl_attachment/" + file_path[insert:]

#    response = FileResponse(open(b, 'rb'), as_attachment=True)
    response = HttpResponseRedirect(serve_file)
    return response



@login_required(login_url='/login/')
def delete_picture(response):

    pic = json.loads(response.body.decode("utf-8"))
    picId = pic['picId']

    pic = Picture.objects.get(id=picId)

    if pic:
        current_user = response.user

        if pic.user_id == current_user.id:
        
            cloudinary.api.delete_resources(pic.file.public_id)
            pic.delete()
            messages.error(response, f"Note: {pic.name} has been deleted!")


    return JsonResponse({})

#-------------------------------------------NOTES----------
@login_required(login_url='/login/')
def notes(response):

    allnotes = Note.objects.all()

    current_user = response.user
    userNotes = Note.objects.filter(user__id=current_user.id).values()

    if response.method == "POST":
        note = response.POST.get('note')

        if len(note) < 1:
            messages.error(response, f"Note is too short!")

        else:
            new_note = Note(note=note, user=current_user)
            new_note.save()
            messages.success(response, f"Note [%s] added!" %note)

    return render(response, "main/notes.html", {"userNotes": userNotes})

@login_required(login_url='/login/')
def update(response, id):

    note = Note.objects.get(id=id)

    if response.method == "POST":

        note.note = response.POST.get('content')
        note.save()
        messages.success(response, "Note updated!")

        return HttpResponseRedirect('/notes')

    else:

        return render(response, "main/update.html", {"note": note})

@login_required(login_url='/login/')
def delete_note(response):

    current_user = response.user

    post_data = json.loads(response.body.decode("utf-8"))
    noteId = post_data['noteId']
    note = Note.objects.get(id=noteId)

    if note:
        if note.user_id == current_user.id:
            note.delete()
            messages.error(response, f"Note [%s] deleted" % note.note)

    return JsonResponse({})
