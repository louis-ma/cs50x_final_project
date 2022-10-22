from django.shortcuts import render

from . import util

from markdown import markdown

from django import forms 

from random import randint

class NewEntryForm(forms.Form):
    title = forms.CharField()
    content = forms.CharField(widget=forms.Textarea)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
    })

def entry(request, title):
    entry = util.get_entry(title)
    if not entry:
        return render(request, "encyclopedia/error.html", {
            "message": "Cannot find that title of the encyclopedia entry"
        })
    return render(request, "encyclopedia/entry.html", {
        "content": markdown(util.get_entry(title)),
        "title": title
    })

def search(request):
    if request.method == "GET":
        input = request.GET.get('q','')
        
        search_result =[]
        for entry in util.list_entries():
            # If exactly match
            if input.lower() == entry.lower():
                return render(request, "encyclopedia/entry.html", {
                    "content": markdown(util.get_entry(entry)),
                    "title": entry
                })
            # If patial match
            if input.lower() in entry.lower():
                search_result.append(entry)


    return render(request, "encyclopedia/search_result.html", {
        "title":input,
        "search_result":search_result
    })

def create(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            util.save_entry(title, content)
            return render(request, "encyclopedia/entry.html", {
                "content": markdown(content),
                "title": title
            })
        else:
            render(request, "encyclopedia/create.html", {
                "form":form
            })

    return render(request, "encyclopedia/create.html", {
        "form":NewEntryForm()
    })

def edit(request, title):
    # Retrive the previous md content 
    content = util.get_entry(title)

    form = NewEntryForm()
    form.fields["title"].initial = title 
    form.fields["title"].widget = forms.HiddenInput()
    form.fields["content"].initial = content 

    return render(request, "encyclopedia/create.html", {
        "title":title,
        "content":content,
        "form":form
    })

def random(request):
    titles = util.list_entries()
    title = titles[randint(0, len(titles) - 1)]
    return render(request, "encyclopedia/entry.html", {
        "content": markdown(util.get_entry(title)),
        "title": title
    })