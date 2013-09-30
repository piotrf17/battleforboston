# Top-level views for www.battleforboston.com.
# TODO(piotrf): Find a better organization for these files.

from django.shortcuts import render

def index(request):
  return render(request, 'index.html', {})

def events(request):
  return render(request, 'events.html', {})

def directions(request):
  return render(request, 'directions.html', {})

def contact(request):
  return render(request, 'contact.html', {})

def tabata(request):
  return render(request, 'tabata.html', {})

def thanks(request):
  return render(request, 'thanks.html', {})
