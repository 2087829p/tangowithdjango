from django.http import HttpResponse ,HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from rango.models import Category,Page,UserProfile
from rango.utils import *
from rango.forms import CategoryForm,PageForm,UserProfileForm,UserForm
from django.contrib.auth import authenticate, login ,logout
from django.contrib.auth.decorators import login_required
from datetime import datetime
from rango.bing_search import run_query

def get_category_list():
    category_list=Category.objects.order_by('-likes')[:5]
    for category in category_list:
        category.url = encode_url(category.name)
    return category_list

def index(request):
    #request.session.set_test_cookie()

    context = RequestContext(request)
    category_list=get_category_list()
    page_list=Page.objects.order_by('-views')[:5]
    context_dict = {'cat_list':category_list,'pages':page_list}
    #### NEW CODE ####
    if request.session.get('last_visit'):
        # The session has a value for the last visit
        last_visit_time = request.session.get('last_visit')
        visits = request.session.get('visits', 0)
        if (datetime.now() - datetime.strptime(last_visit_time[:-7], "%Y-%m-%d %H:%M:%S")).seconds >5:
            request.session['visits'] = visits + 1
            request.session['last_visit'] = str(datetime.now())
    else:
        # The get returns None, and the session does not have a value for the last visit.
        request.session['last_visit'] = str(datetime.now())
        request.session['visits'] = 1
    #### END NEW CODE ####

    # Render and return the rendered response back to the user.
    return render_to_response('rango/index.html', context_dict, context)
	
def about(request):
    context = RequestContext(request)
    count=0
    if request.session.get('visits'):
        count = request.session.get('visits')
    context_dict = {'student_name': "Anton Petrov",'student_number':'2087829','visits':count}
    return render_to_response('rango/about.html', context_dict, context)
    #return HttpResponse("Rango says:Here is the about page!")

def category(request, category_name_url):
    context = RequestContext(request)
    result_list = []
    if request.method == 'POST':
        query = request.POST['query'].strip()
        if query:
            # Run our Bing function to get the results list!
            result_list = run_query(query)
    category_name = decode_url(category_name_url)
    category_list=get_category_list()
    context_dict = {'category_name': category_name,'category_url':category_name_url,'cat_list':category_list,'result_list':result_list}
    try:
        category = Category.objects.get(name=category_name)
        pages = Page.objects.filter(category=category)
        context_dict['pages'] = pages
        context_dict['category'] = category
    except Category.DoesNotExist:
        pass
    return render_to_response('rango/category.html', context_dict, context)

def add_category(request):
    context = RequestContext(request)
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return index(request)
        else:
            print form.errors
    else:
        form = CategoryForm()
    return render_to_response('rango/add_category.html', {'form': form}, context)

def add_page(request, category_name_url):
    context = RequestContext(request)
    category_name = decode_url(category_name_url)
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            # This time we cannot commit straight away.
            # Not all fields are automatically populated!
            page = form.save(commit=False)
            # Retrieve the associated Category object so we can add it.
            # Wrap the code in a try block - check if the category actually exists!
            try:
                cat = Category.objects.get(name=category_name)
                page.category = cat
            except Category.DoesNotExist:
                # If we get here, the category does not exist.
                # Go back and render the add category form as a way of saying the category does not exist.
                return render_to_response('rango/add_category.html', {}, context)
            # Also, create a default value for the number of views.
            page.views = 0
            # With this, we can then save our new model instance.
            page.save()
            # Now that the page is saved, display the category instead.
            return category(request, category_name_url)
        else:
            print form.errors
    else:
        form = PageForm()
    return render_to_response( 'rango/add_page.html',
            {'category_name_url': category_name_url,
             'category_name': category_name, 'form': form},
             context)

def register(request):
    if request.session.test_cookie_worked():
        print ">>>> TEST COOKIE WORKED!"
        request.session.delete_test_cookie()
    context = RequestContext(request)
    registered = False
    if request.method == 'POST':       
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():            
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            profile.save()
            registered = True
        else:
            print user_form.errors, profile_form.errors
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    return render_to_response(
            'rango/register.html',
            {'user_form': user_form, 'profile_form': profile_form, 'registered': registered},
            context)
			
def user_login(request):    
    context = RequestContext(request)
    if request.method == 'POST':       
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:            
            if user.is_active:                
                login(request, user)
                return HttpResponseRedirect('/rango/')
            else:                
                return HttpResponse("Your Rango account is disabled.")
        else:
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")
    else:       
        return render_to_response('rango/login.html', {}, context)

@login_required
def restricted(request):
    context = RequestContext(request)    
    return render_to_response('rango/restricted.html',{}, context)
    #return HttpResponse("Since you're logged in, you can see this text!")
	
@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)
    # Take the user back to the homepage.
    return HttpResponseRedirect('/rango/')
	
def search(request):
    context = RequestContext(request)
    result_list = []
    if request.method == 'POST':
        query = request.POST['query'].strip()
        if query:
            # Run our Bing function to get the results list!
            result_list = run_query(query)
    return render_to_response('rango/search.html', {'result_list': result_list}, context)

def profile(request):
    context=RequestContext(request)
    #usr=None
    #if request.user.is_authenticated:
        #usr=UserProfile.objects.get(user_id=request.user.id)
    return render_to_response('rango/profile.html',{'user':request.user},context)
def track_url(request):
    context=RequestContext(request)
    page_id=None
    if request.method == 'GET':
        if 'page_id' in request.GET:
            page_id = request.GET['page_id']
            if page_id:
                page=Page.objects.get(id=page_id)
                page.views+=1
                page.save()
                return HttpResponseRedirect(page.url)
    return render_to_response('rango/index.html',context)
