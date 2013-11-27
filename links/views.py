# Create your views here.

from links.models import Link, Vote, UserProfile
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.context_processors import csrf
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from head.forms import ProfileUpdateForm


def home_view(request):
    link_list = Link.with_votes.all()
    paginator = Paginator(link_list,5)
    page = request.GET.get('page')
    try:
        links = paginator.page(page)
    except PageNotAnInteger:
        links = paginator.page(1)
    except EmptyPage:
        links = paginator.page(paginator.num_pages)
    return render_to_response('links/home.html', context_instance= RequestContext(request, {'links':links}))

def profile_view(request):
    user = User.objects.get(username__iexact= request.user.username)
    bio = UserProfile.objects.get(user=user.id)
    return render_to_response('profile.html',context_instance = RequestContext(request,{'user':user,'bio':bio}))
 
def profile_update_view(request):
    if request.method=='POST':
        form = ProfileUpdateForm(request.POST,request.FILES)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.filter(username__iexact= request.user.username).update(email=email)
            return HttpResponseRedirect('/profile/')
            
    c= {}
    c.update(csrf(request))
    c['form'] = ProfileUpdateForm
    return render_to_response('profile_update.html', context_instance= RequestContext(request,c))   





def register_view(request):
    error = ''
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']
        email = request.POST['password']
        if password==password2:
            
            try:
                user = User.objects.create(username=username,password= password, email=email)
                user.set_password(password)
                user.is_active= True
                user.save()
                return HttpResponseRedirect('/login/')
            except:
                error = "User name already exits"
                #return render_to_response('register.html', e)
        else:
            error = 'Password doesn\'t match'
    c ={}
    c.update(csrf(request))
    c['error'] = error
    return render_to_response('register.html', c)

#@login_required(login_url='/login/')
def login_view(request):
    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/profile/')
        else:
            error = 'Username or password are wrong'
            return error
    c = {}
    c.update(csrf(request))
    return render_to_response('login.html',c)

def logout_view(request):
    logout(request);
    return HttpResponseRedirect('/accounts/login/')
