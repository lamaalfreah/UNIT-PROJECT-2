# Create your views here.
from django.shortcuts import render, redirect
from .forms import ContactForm
from .models import Contact

# Contact form view - handles submission and validation
def contact_us(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('contact')
    else:
        form = ContactForm()
    return render(request, 'contact/contact.html', {'form': form})

# View to display submitted contact messages
def contact_messages(request):
    messages = Contact.objects.order_by('-created_at')
    return render(request, 'contact/messages.html', {'messages': messages})
