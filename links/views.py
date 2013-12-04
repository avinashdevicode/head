# Create your views here.

from links.models import Link, Vote, UserProfile, comment
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.context_processors import csrf
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from head.forms import ProfileUpdateForm
from links.forms import link_creation_form, update_form, Comment
from django.views.generic import CreateView


def home_view(request):
    link_list = Link.with_votes.all()
    number_of_shows = 6
    paginator = Paginator(link_list, number_of_shows)
    page = request.GET.get('page')
    try:
        links = paginator.page(page)
        page_index = 1
        if int(page) != 1:
            page_index = (int(page)-1) * number_of_shows
    except PageNotAnInteger:
        links = paginator.page(1)
        page_index = 1
    except EmptyPage:
        links = paginator.page(paginator.num_pages)
    return render_to_response('links/home.html', context_instance= RequestContext(request, {'links':links,'page_index':page_index}))

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

def create_link_view(request):
    if request.method == 'POST':
        user= User.objects.get(username = request.user.username)
        f = link_creation_form(request.POST)
        if f.is_valid():
            links = f.save(commit = False);
            user= User.objects.get(username = request.user.username)
            links.submitter = user
            links.save()
            return HttpResponseRedirect('/links/home/')
    c= {}
    c.update(csrf(request))
    c['formset'] = link_creation_form
    return render_to_response('links/link_creation.html',context_instance = RequestContext(request, c))

def update_link_view(request,pk):
    id = pk
    if request.method == "POST":
        form = update_form(request.POST, request.FILES)
        if form.is_valid():
            print dir(form)
            print form
        title = form.cleaned_data['title']
        url = form.cleaned_data['url']
        description = form.cleaned_data['description']
        user = User.objects.get(username = request.user.username)
        link = Link.objects.filter(id=id).update(
                title = title, url = url,description =description, submitter=user)
        return HttpResponseRedirect('/link/%d' % int(id))
    link = Link.objects.filter(id=id)
    c = {}
    c.update(csrf(request))
    c['form'] = update_form
    c['id'] = id
    c['link'] = link
    return  render_to_response('links/update_link.html',context_instance = RequestContext(request,c))



def delete_link_view(request, pk):
    Link.objects.filter(id=pk).delete()
    return HttpResponseRedirect('/links/home/')
        
       
def detail_view(request, pk):
    id = pk
    link = Link.objects.all().filter(id=id)
    print 1
    print request.method
    if request.method == 'POST':
        print 2
        form = Comment(request.POST)
        if form.is_valid():
            f= form.save(commit=False)
            link1 = Link.objects.get(id =id)
            f.link = link1
            user = User.objects.get(username= request.user.username)
            f.commenter = user
            f.save()
    c = {}
    c.update(csrf(request))
    c['link'] = link
    c['form'] = Comment
    comments = comment.objects.filter(link=link)
    c['comments'] = comments
    return render_to_response('links/detail.html', c)




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
