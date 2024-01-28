from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django import forms
from django.urls import reverse
from . import util
import logging
import random

logger = logging.getLogger("encyclopedia.views")

class NewForm(forms.Form):
    search = forms.CharField(required= False,
    widget= forms.TextInput
    (attrs={'placeholder':'Title','style':'margin-bottom:2px;'}),
    label='')

class NewTextArea(forms.Form):
    title = forms.CharField(required= False,
    widget= forms.TextInput
    (attrs={'placeholder':'Title','class':'col-sm-8', 'style':'margin:2px;'}),
    label='')
    
    content = forms.CharField(
        widget=forms.Textarea
        (attrs={'class':'col-sm-8', 'style':'margin:2px; height: 50%;', 'placeholder':'Content'}),
    label='')

text_area= NewTextArea()
form = NewForm()


def index(request):
      
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form":form
    })

def new_page(request):

    if request.method == "POST":
        content_form = NewTextArea(request.POST)
        if content_form.is_valid():
            title = content_form.cleaned_data["title"].lower()
            content = content_form.cleaned_data["content"]

            all_topics = util.list_entries()
            all_topics = list(map(lambda x: x.lower(), all_topics))
            if title in all_topics:
                return render(request, "encyclopedia/error.html", {
                    "title": title,
                    "error": " already exist",
                    "form":form
                })
            else:
                util.save_entry(title,content)
                return render(request, "encyclopedia/title.html", {
                    "title": title,
                    "content": content,
                    "form":form
                })
        else:
            return render(request, "encyclopedia/new_page.html", {
                "text_area": text_area,
                "form":form
            })

    return render(request, "encyclopedia/new_page.html", {
        "text_area": text_area,
        "form": form
    })

def random_page(request):  
    topic_list = util.list_entries()
    random_topic = random.choice(topic_list)
    return title(request,random_topic)

def save(request):   
    return render(request, "encyclopedia/random_page.html")

def edit(request, title):

    if request.method == "GET":
        content = util.get_entry(title)
        pre_populated_form= NewTextArea(initial={'title': title, 'content': content})

        return render(request, "encyclopedia/edit.html", {  
            "pre_populated_form":pre_populated_form,
            "form": form 
        }) 
    else:
        content = request.POST.get("content")
        if content == "":
            return render(request, "encyclopedia/error.html", {
                    "title": title,
                    "error": "Empty content try again",
                    "form":form
                })
        else:
            util.save_entry(title, content)
            return redirect("title", title=title)

    
def title(request,title):
    
    content = util.get_entry(title)

    if content is None:
        return render(request,"encyclopedia/not_found.html",{
        "title": title,
        "form":form
    })
    
    else:
        return render(request, "encyclopedia/title.html", {
        "title": title,
        "content": content,
        "form":form
    })

def search_results(request):

    if request.method == "GET":
        form = NewForm(request.GET)

        if form.is_valid():
            title = form.cleaned_data["search"].lower()
            content = util.get_entry(title)
            if content == None:
                similar_strings = []
                for string in util.list_entries():
                    if title in string:
                        similar_strings.append(string)
                 
                return render(request, "encyclopedia/not_found.html", {
                "title": title,
                "similar_topics": similar_strings,
                "form":form
                })
            else:
                return render(request, "encyclopedia/title.html", {
                    "title": title,
                    "content": content,
                    "form":form
                })

   