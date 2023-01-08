from django import forms
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from markdown2 import markdown
from . import util
from random import choice

class NewEntryForm(forms.Form):
    title = forms.CharField(label="Title:", widget=forms.TextInput(attrs={'size': 40}))
    content = forms.CharField(label="Content:", widget=forms.Textarea())

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entry):
    page = util.get_entry(entry)
    if not page:
        return render(request, "encyclopedia/error.html")

    else:
        return render(request, "encyclopedia/entry.html", {
            "entry": entry,
            "content": markdown(page)
        })

def search(request):
    if request.method == "POST":
        title = request.POST["q"]
        page = util.get_entry(title)

        if page:
            return render(request, "encyclopedia/entry.html", {
                "entry": title,
                "content": markdown(page)
            })
            
        else:
            search_results = []
            entries = util.list_entries()
            for entry in entries:
                if title.lower() in entry.lower():
                    search_results.append(entry)
                    
            return render(request, "encyclopedia/search.html", {
                "title": title,
                "results": search_results
            })

    else:
        return HttpResponseRedirect(reverse("index"))


def create(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            page = util.get_entry(title)
            if not page:
                util.save_entry(title, content)
                return HttpResponseRedirect(f"/wiki/{title}")

            else:
                return render(request, "encyclopedia/create.html", {
                    "form": NewEntryForm(),
                    "failure": True
                })

        else:
            return render(request, "encyclopedia/create.html", {
                "form": NewEntryForm()
            })

    else:
        return render(request, "encyclopedia/create.html", {
            "form": NewEntryForm()
        })

    
def edit(request, title):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            util.save_entry(title, content)
            return HttpResponseRedirect(f"/wiki/{title}")

        else:
            return render(request, "encyclopedia/edit.html", {
                "form": NewEntryForm({'title':title, 'content': page}),
                "title": title
            })


    else:
        page = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
            "form": NewEntryForm({'title':title, 'content': page}),
            "title": title
        })

def random(request):
    return HttpResponseRedirect(f"/wiki/{ choice( util.list_entries())}")


    