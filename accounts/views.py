from django.shortcuts import render,redirect
from django.contrib import messages,auth
# user model come with django as default
from django.contrib.auth.models import User
from contacts.models import Contact
def register(request):
    if request.method == 'POST':
        # Get Form Values
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        #check if password match
        if password == password2:
            #Check username
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username is taken')
                return redirect('register')
            else:
                # Checking if email is exists in database or not
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'Email is being used')
                    return redirect('register')
                else:
                    #look good
                    # Now if everything is unique we will
                    #create anew user and enter the data in the user database
                    user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
                    # login after register
                    # auth.login(request, user)
                    user.save()
                    messages.success(request, 'You are now registered and can login')
                    return redirect('login')

                    


        else:
            messages.error(request, 'Passwords do not match')
            return redirect('register')
    else:
        return render(request, 'accounts/register.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # checking if username and its password matches or not
        user = auth.authenticate(username=username, password=password)

        # If it matches user can login
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are now logged in')
            return redirect('dashboard')
        # Otherwise it will throw an error 
        else:
            messages.error(request, 'Invalid Credential')
            return redirect('login')
    else:
        return render(request, 'accounts/login.html')

def dashboard(request):
    user_contacts = Contact.objects.order_by('-contact_date').filter(user_id=request.user.id)

    context = {
        'contacts': user_contacts
    }
    return render(request, 'accounts/dashboard.html',context)

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, 'You are now logged out')
        return redirect('index')