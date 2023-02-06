from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.db import IntegrityError
from datetime import datetime
from .models import User, Record

# Create your views here.
def index(request):
    return render(request, "finance/index.html")

def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        if not username or not password:
            return render(request, "finance/login.html", {
                "message": "Incomplete fields. Please try again."
            })

        user = authenticate(request, username=username, password=password)

        if user is not None :
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        elif user is None:
            return render(request, "finance/login.html", {
                "message": "Incorrect username or password. Please try again."
            })
        else:
            return render(request, "finance/login.html", {
                "message": "An unknown error occured. Please try again."
            })

    else:
        try:
            # Try and retrieve message if any
            message = request.session.get("message")
            success = request.session.get("success")

            # Delete message from request.session to only show it once 
            del request.session["message"]
            del request.session["success"]

            return render(request, "finance/login.html", {
                "message": message,
                "success": success
            })

        except:
            return render(request, "finance/login.html")


def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        if not username or not password or not confirmation:
            return render(request, "finance/register.html", {
                "message": "Incomplete fields. Please try again."
            })

        if password != confirmation:
            return render(request, "finance/register.html", {
                "message": "Passwords do not match. Please try again."
            })

        try:
            user = User.objects.create_user(username, "", password)
            user.save()

            # Save context as session variable to retrieve later
            # This is because HttpResponseRedirect does not support passing context data
            request.session["message"] = "Account created successfully. Please attempt to login now."
            request.session["success"] = True

            return HttpResponseRedirect(reverse("login"))

        except IntegrityError:
            return render(request, "finance/register.html", {
                "message": "Username already taken. Please try again."
            })

        except:
            return render(request, "finance/register.html", {
                "message": "An unknown error occured. Please try again."
            })

    else:
        return render(request, "finance/register.html")

def records(request):
    if request.method == "POST":
        user = request.user
        record_type = request.POST["type"]
        category = request.POST["category"]
        amount = request.POST["amount"]
        comment = request.POST["comment"]
        time = datetime.now()

        print(record_type)
        print(type(record_type))

        if not record_type or not category or not amount:
            return render(request, "finance/records.html", {
                "types": Record.TYPE_CHOICES,
                "categories": Record.CATEGORY_CHOICES,
                "message": "Incomplete fields. Please try again."
            })

        # TODO: 0.0 VALIDATION FOR AMOUNT

        try: 
            record_type = int(record_type)
            category = int(category)
            amount = float(amount)

            new_record = Record(
                user = user,
                record_type = record_type,
                category = category,
                amount = amount,
                comment = comment,
                time = time
            )
            new_record.save()

            return render(request, "finance/records.html", {
                "types": Record.TYPE_CHOICES,
                "categories": Record.CATEGORY_CHOICES,
                "records": Record.objects.all()
            })            

        except:
            return render(request, "finance/records.html", {
                "message": "An unknown error occured. Please try again.",
                "types": Record.TYPE_CHOICES,
                "categories": Record.CATEGORY_CHOICES,
                "records": Record.objects.all()
            })

    else:
        return render(request, "finance/records.html", {
            "types": Record.TYPE_CHOICES,
            "categories": Record.CATEGORY_CHOICES,
            "records": Record.objects.all()
        })


