from django.shortcuts import render, redirect
from django import forms
import pysnooper
from django.http import HttpResponseRedirect
from django.urls import reverse
import random

import pysnooper

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def page_search(request, page_name):
    page = util.get_entry(page_name)
    if page:
        return render(request, "encyclopedia/page.html", {"page": page})
    else:
        return render(request, "encyclopedia/file_not_found.html")


@pysnooper.snoop()
def search(request):
    if request.method == "POST":
        query = request.POST["q"]
        docs = [word.lower() for word in util.list_entries()]
        possible_refs = []
        ref_dict = {}
        if util.get_entry(query):
            return redirect('wiki', page_name=query)
        for doc in docs:
            if query in doc:
                possible_refs.append(doc)
        if possible_refs:
            for ref in possible_refs:
                ref_dict[ref] = str(f'wiki/{ref}')
            return render(request, "encyclopedia/search.html", {"ref_dict": ref_dict
                                                   })
        else:
            return render(request, "encyclopedia/file_not_found.html")


@pysnooper.snoop()
def random_page(request):
    docs = util.list_entries()
    selected = random.choice(docs)
    return redirect('wiki', page_name=selected)


class ArticleForm(forms.Form):
    title = forms.CharField(label="title")
    text = forms.CharField(widget=forms.Textarea, label="content")


def new_page(request):
    if request.method == "POST":
        form = ArticleForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            text = form.cleaned_data["text"]
            existing = [doc.lower() for doc in util.list_entries()]
            if title.lower() not in existing:
                with open(f"entries/{title}.md", "a") as f:
                    f.write(text)
                return redirect('wiki', page_name=title)
            else:
                return render(request, "encyclopedia/file_exists.html")
    else:
        return render(request, "encyclopedia/new_page.html", {"form": ArticleForm()})


def edit_page(request, name):
    return render(request, "encyclopedia/edit.html")
