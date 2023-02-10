from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.db import IntegrityError
from django.utils import timezone
from datetime import datetime, timedelta
from .models import User, Record
import json

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("dashboard"))    
    else:
        return HttpResponseRedirect(reverse("welcome"))

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
            return HttpResponseRedirect(reverse("dashboard"))
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


def welcome(request):
    return render(request, "finance/welcome.html")

def dashboard(request):
    user = request.user

    current_date = datetime.now().date()
    past_seven_days = current_date - timedelta(days=6)
    past_thirty_days = current_date - timedelta(days=29)

    past_7_income = Record.objects.filter(user=user, record_type=1, time__range=(past_seven_days, current_date + timedelta(days=1)))
    past_7_expense = Record.objects.filter(user=user, record_type=2, time__range=(past_seven_days, current_date + timedelta(days=1)))
    past_30_expense = Record.objects.filter(user=user, record_type=2, time__range=(past_thirty_days, current_date + timedelta(days=1)))
    
    # Determining average income and expense (past 7 days) for HTML card
    past_7_total_income = 0
    past_7_total_expense = 0

    for record in past_7_income:
        past_7_total_income += record.amount
    
    for record in past_7_expense:
        past_7_total_expense -= record.amount

    past_7_average_expense = round(past_7_total_expense / 7, 2)

    # Making a dictionary for line chart data
    line_data = {}

    for i in range(30):
        date = current_date - timedelta(days=(29-i))
        line_data[date] = 0

    for record in past_30_expense:
        if record.record_type == 2:
            line_data[record.time.date()] -= record.amount

    for record in past_7_expense:
        print(record)

    # Making a dictionary for pie chart data
    pie_data = {}

    for record in Record.objects.all():
        category = Record.CATEGORY_CHOICES[record.category-1][1]

        if record.record_type == 2:
            if category not in pie_data:
                pie_data[category] = -(record.amount)
            else:
                pie_data[category] += -(record.amount)


    return render(request, "finance/dashboard.html", {
        "records": Record.objects.filter(user=user).order_by("-time")[:10],
        "categories": Record.CATEGORY_CHOICES,
        "past_7_total_income": past_7_total_income,
        "past_7_total_expense": past_7_total_expense,
        "past_7_average_expense": past_7_average_expense,
        "pie_data": pie_data,
        "line_data": line_data,
    })

def records(request):
    user = request.user

    if request.method == "POST":
        record_type = request.POST["type"]
        category = request.POST["category"]
        amount = request.POST["amount"]
        comment = request.POST["comment"]
        time = datetime.now()

        if not record_type or not category or not amount:
            return render(request, "finance/records.html", {
                "types": Record.TYPE_CHOICES,
                "categories": Record.CATEGORY_CHOICES,
                "message": "Incomplete fields. Please try again."
            })

        try: 
            record_type = int(record_type)
            category = int(category)

            if record_type == 1:
                amount = float(amount)
            else: 
                amount = -(float(amount))
                
            if amount == 0:
                return render(request, "finance/records.html", {
                    "message": "Amount cannot be 0. Please try again.",
                    "types": Record.TYPE_CHOICES,
                    "categories": Record.CATEGORY_CHOICES,
                    "records": Record.objects.filter(user=user).order_by("-time")
                })                

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
                "records": Record.objects.filter(user=user).order_by("-time")
            })            

        except:
            return render(request, "finance/records.html", {
                "message": "An unknown error occured. Please try again.",
                "types": Record.TYPE_CHOICES,
                "categories": Record.CATEGORY_CHOICES,
                "records": Record.objects.filter(user=user).order_by("-time")
            })

    else:
        return render(request, "finance/records.html", {
            "types": Record.TYPE_CHOICES,
            "categories": Record.CATEGORY_CHOICES,
            "records": Record.objects.filter(user=user).order_by("-time")
        })

