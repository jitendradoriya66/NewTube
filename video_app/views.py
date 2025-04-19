from django.shortcuts import render,HttpResponse,redirect,get_object_or_404
from .models import *
from django.core.mail import send_mail
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.paginator import Paginator

# Create your views here.

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        photo = request.FILES.get('photo')

        if User.objects.filter(email=email).exists():
            pass  # You can add a message here for feedback
        else:
            user = User.objects.create(username=username, email=email, password=password,photo=photo)
            if photo:
                user.photo.save(photo.name, photo)
            user.save()
            return redirect('login')  
        
    return render(request, 'registration.html')

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        user = User.objects.filter(email=email).exists()
        if user:
            u=User.objects.get(email=email)
            if u.password==password:
                request.session['email']=email
                return redirect(index)
            else:
                return render(request, 'login.html', {'error': 'Incorrect password.'})
                
        else:
            return render(request, 'login.html', {'error': 'Incorrect password.'})
    
    return render(request, 'login.html')


import random
def forget(request):
    if request.POST:
        email=request.POST['email']
        print(email)
        uid=User.objects.filter(email=email).exists()   
        otp=random.randint(1000,9999)
        print(otp)
        if uid:
            uid=User.objects.get(email=email)
            uid.otp=otp
            uid.save()
            send_mail('Forget password  :',f'OTP :{otp}','jitendradoriya92@gmail.com',[email])
            contaxt={
                'uid':uid
            }
            return render(request,'c_password.html',contaxt)
            
        else:
            contaxt={
                'msg':'Not Register yet '
            }
            return render(request,'forget.html',contaxt)
            
    return render(request,'forget.html')

def c_password(request):
    if request.POST:
        email=request.POST['email']
        otp=request.POST['otp']
        new_pass=request.POST['new_pass']
        con_pass=request.POST['con_pass']
        print(email,otp,new_pass,con_pass)
        uid=User.objects.get(email=email)
        print(type(uid.otp),type(otp))
        if uid.otp==int(otp):
            if new_pass == con_pass:
                uid.password = new_pass
                uid.save()
                return redirect(login)
            else:
                contaxt={
                    "msg":"invalid Password and C_Password",
                    "uid":uid
                    
                }
                return render(request,'c_password.html',contaxt)
        else:
            contaxt={
                    "msg":"invalid Otp",
                    "uid":uid
                }
            return render(request,'c_password.html',contaxt) 
                    
    return render(request,'c_password.html')


def index(request):
    if 'email' not in request.session:
        return redirect(login)
    
    posts=Video.objects.all()
    pagination=Paginator(posts,2)
    page=request.GET.get('page')
    posts=pagination.get_page(page)
    context={
    'posts':posts
    }
    return render(request,"index.html",context)

def video_details(request, id):
    v = get_object_or_404(Video, id=id)
    channle = v.user 
    user = User.objects.get(email=request.session['email'])
    
    vi = LikeDislike.objects.filter(user=user, video=v).exists()
    v.view += 1
    v.save()
    
    l = LikeDislike.objects.filter(user=user, video=v)
    c = Comment.objects.filter(video=v).order_by('-created_at')[:10]
    j = Subscription.objects.filter(subscriber=user, channle=channle).exists()
    b = Subscription.objects.filter(subscriber=user).count()
    
    context = {
        'v': v, 'c': c, 'vi': vi, 'j': j, 'b': b, 'l': l
    }
    
    if request.method == 'POST':
        comment = request.POST['comment']
        rid = User.objects.get(email=request.session.get('email'))
        Comment.objects.create(user=rid, video=v, content=comment)
        return HttpResponseRedirect(reverse('video_details', args=[id]))
    
    return render(request, 'video_details.html', context)

def create_video(request):
    if request.method == "POST":
        title = request.POST['title']
        description = request.POST['description']
        file = request.FILES['file']
        thumbnail = request.FILES['thumbnail']
        
        rid=User.objects.get(email=request.session['email'])
        # uid = Video.objects.filter().exists()
        # if not uid:
        Video.objects.create(
                user=rid,
                title=title,
                description=description,
                file=file,
                thumbnail=thumbnail,
            )
        return redirect(index)  # Redirect to your home page or a success page

    return render(request, 'create_post.html')


def delete_all(request):
    posts=Video.objects.all()
    posts.delete()
    return render(request,'index.html')

def search(request):
    return render(request,'search.html')


def search_function(request):
    if request.POST:
        search=request.POST['query']
        video=Video.objects.filter(title__icontains=search)
        context={
            'video':video
        }
        return render(request,'search.html',context)
        
    return render(request,'search.html')


def like_video(request, id):
    rid = get_object_or_404(User, email=request.session.get('email')) 
    v = get_object_or_404(Video, id=id)  

    liked = LikeDislike.objects.filter(user=rid, video=v).exists()

    if not liked:
        LikeDislike.objects.create(user=rid, video=v)
        v.like += 1
    else:
        LikeDislike.objects.filter(user=rid, video=v).delete()
        v.like -= 1

    v.save()  
    return HttpResponseRedirect(reverse('video_details', args=[id]))


def logout(request):
    del request.session
    return redirect(login)


def profile(request):
    data=User.objects.get(email=request.session['email'])
    u=Subscription.objects.filter(channle=data).count()
    v=Video.objects.filter(user=data).count()
    context={
        'data':data,
        'u':u,
        'v':v
    }
    return render(request,'profile.html',context)   

def subscriber_Details(request):
    user=User.objects.get(email=request.session['email'])
    total=Subscription.objects.filter(channle=user)
    context={
        'total':total
    }
    return render(request,'subscriberlist.html',context)

# def edit(request, id):
#     if request.POST:
#         # New_username = request.POST['name']   
#         email = request.POST['email']
#         # password = request.POST['password']
#         uid = User.objects.filter(email=email).exists()
#         if uid:
#             New_username = request.POST['name']   
#             email = request.POST['email']
#             password = request.POST['password']
#             u = User.objects.get(id=id)
#             u.username = New_username
#             u.email = email
#             u.password = password
#             u.save()
#             # return redirect('profile', id=id)  # Corrected redirect
#         return render(request, 'edit.html', {'u': u})
            
    # return render(request, 'edit.html')


def edit(request):
        if request.POST:
            username=request.POST['username']
            email=request.POST['email']
            password=request.POST['password']
            uid=User.objects.get(email=request.session['email'])
            uid.email=email
            uid.username=username
            uid.password=password
            uid.save()
            return redirect(profile)
        if request.FILES:
            username=request.POST['username']
            email=request.POST['email']
            password=request.POST['password']
            photo=request.FILES['photo']
            uid=User.objects.get(email=request.session['email'])
            uid.photo=photo
            uid.email=email
            uid.username=username
            uid.password=password
            uid.save()
            return redirect(profile)
        data=User.objects.get(email=request.session['email'])
        contaxt={
            'data':data
        }
        return render(request,'edit.html',contaxt)
    
    
def category_list(request):
    cid=category.objects.all()
    context={
        'cid':cid
    }    
    return render(request,'category.html',context)



def display_category(request,id):
    cid=Video.objects.filter(category=id)
    for i in cid:
        print(i.title)
    return render(request,'display_category.html',{'cid':cid})


def watch_letter(request,id):
    # print(id)
    video=Video.objects.get(id=id)
    user=User.objects.get(email=request.session['email'])
    
    uid=watchLetter.objects.filter(user=user,video=video).exists()
    if not uid:
        watchLetter.objects.create(user=user,
                                video=video,
                                title=video.title,
                                    description=video.description,
                                    file=video.file,
                                    thumbnail=video.thumbnail
                                    )
        return redirect(show_watch_letter)
    return redirect(show_watch_letter)
    
    
def show_watch_letter(request):
    user=User.objects.get(email=request.session['email'])
    wl=watchLetter.objects.filter(user=user)
    for i in wl:
        print(i.title)

    context={
        'wl':wl
    }    
    return render(request,'watch_later.html',context)


# def subscriber_channle(request,id):
#     channle=User.objects.get(id=id)
    
#     subscriber=User.objects.get(email=request.session['email'])
#     uid=Subscription.objects.filter(subscriber=subscriber,channle=channle).exists()
#     if not uid:
#         Subscription.objects.create(subscriber=subscriber,channle=channle)
#     else:
#         Subscription.objects.filter(subscriber=subscriber,channle=channle).delete()
        

def subscriber_channle(request, id):
    video = get_object_or_404(Video, id=id)
    channle = video.user 
    
    subscriber = User.objects.get(email=request.session['email'])
    
    subscribed = Subscription.objects.filter(subscriber=subscriber, channle=channle).exists()
    
    if not subscribed:
        Subscription.objects.create(subscriber=subscriber, channle=channle)
    else:
        Subscription.objects.filter(subscriber=subscriber, channle=channle).delete()
    
    return HttpResponseRedirect(reverse('video_details', args=[id]))

def delete_watchlatter(request,id):
    uid=watchLetter.objects.get(id=id)
    uid.delete()
    return redirect(show_watch_letter)

def show_all_post(request):
    user=User.objects.get(email=request.session['email'])
    videos=Video.objects.filter(user=user)
    context={
        'videos':videos
    }
    return render(request,'user_video.html',context)


def trending(request):
    video=Video.objects.all().order_by('-view')
    # print(video)
    for i in video:
        print(i.view)
    context={
        'video':video
    }
    return render(request,'trending.html',context)


def delete_video(request,id):
    uid=Video.objects.get(id=id)
    uid.delete()
    return redirect(show_all_post)

def edit_video(request,id):
    if request.method == "POST":
        title = request.POST['title']
        description = request.POST['description']
        file = request.FILES['file']
        thumbnail = request.FILES['thumbnail']
        
        uid=Video.objects.get(id=id)
        uid.title=title
        uid.description=description
        uid.file=file
        uid.thumbnail=thumbnail
        uid.save()
        return redirect(show_all_post)
    return render(request,'edit_video.html')
    
    
def delete_account(request,id):
    uid=User.objects.get(id=id)
    uid.delete()
    return redirect(register)