from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import SimpleSignUpForm, SimpleLoginForm
from django.contrib.auth.decorators import login_required


def signup_view(request):
	if request.method == 'POST':
		form = SimpleSignUpForm(request.POST)
		if form.is_valid():
			user = form.save()
			# Log the user in
			login(request, user)
			return redirect('dashboard')
	else:
		form = SimpleSignUpForm()
	return render(request, 'accounts/signup.html', {'form': form})


def login_view(request):
	if request.method == 'POST':
		form = SimpleLoginForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			user = authenticate(request, username=username, password=password)
			if user is not None:
				login(request, user)
				return redirect('dashboard')
			else:
				form.add_error(None, 'Invalid credentials')
	else:
		form = SimpleLoginForm()
	return render(request, 'accounts/login.html', {'form': form})


@login_required
def logout_view(request):
	logout(request)
	return redirect('login')
