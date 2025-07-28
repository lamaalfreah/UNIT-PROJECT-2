# Create your views here.
from django.shortcuts import render, redirect
from .forms import ContactForm
from .models import Contact
from django.http import HttpRequest

# Contact form view - handles submission and validation
def contact_us(request:HttpRequest):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')

    else:
        form = ContactForm()
    return render(request, 'contact/contact.html', {'form': form})