from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

def register(request):
    '''Register new user'''
    if request.method != 'POST':
        # Displays an empty registration form
        form = UserCreationForm()
    else:
        # Processing of the completed form
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()
            # logging in and redirecting to the home page
            login(request, new_user)
            return redirect('learning_logs:index')
        
    # Output an empty or invalid form
    context = {'form': form}
    return render(request, 'users/register.html', context)