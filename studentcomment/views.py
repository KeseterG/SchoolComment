from django.shortcuts import render,HttpResponseRedirect,HttpResponse
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import permission_required
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.datastructures import MultiValueDictKeyError,MultiValueDict
from django import forms
from django.urls import reverse
from studentcomment.models import MainComment,OtherComments
import logging

logger=logging.getLogger("console")


def get_login_info(request):
    if request.user.is_authenticated:
        msg=request.user.username+", 欢迎"
        return msg
    else:
        return "您还没有登陆..."


def index(request):
    return HttpResponse("index")


def log_in(request):
    ctx={}
    ctx["login_info"] = get_login_info(request)
    if request.POST:
        user_name=request.POST["Username"]
        user_password=request.POST["Password"]
        user=authenticate(username=user_name,password=user_password)

        if user is not None:
            if user.is_active:
                login(request,user)
                ctx["login_info"]=get_login_info(request)
                ctx["error_msg"]="Login success"
                return render(request, "error.html",ctx)

        else:
            ctx["login_info"] = get_login_info(request)
            ctx["state"]="密码或用户名错误，登陆失败"

    return render(request, "login.html", ctx)


def log_out(request):
    if request.user is not None:
        logout(request)
        return render(request, "error.html", {"error_msg": "logout_success",
                                              "login_info":get_login_info(request)})
    else:
        return render(request,"error.html",{"error_msg":"尚未登陆",
                                            "login_info": get_login_info(request)})


@permission_required("studentcomment.change_comment",login_url="/login/")
def edit(request):
    user = request.user
    # main_comment=get_object_or_404(MainComment,author=user)
    # other_comments_write_ny_user=get_object_or_404(OtherComments,author=user)

    if request.POST:
        global main_comment

        try:
            main_comment=MainComment.objects.get(author=user)
            main_comment.main_comment_text = request.POST.get("selfcomment")
            main_comment.latest_change_time_stamp = timezone.now()
            main_comment.author = user
            main_comment.save()

        except MainComment.DoesNotExist:
            new_main_comment = MainComment(main_comment_text=request.POST.get("selfcomment"),
                                           author=user)
            new_main_comment.save()

        other_comments_set=[]
        a=1
        while True:
            try:
                logger.debug(request.POST["select"+str(a)])
                other_comments_set.append({"other_comment_text": request.POST["othercomment"+str(a)],
                                           "to_username":request.POST["select"+str(a)]})
                a+=1

            except MultiValueDictKeyError:
                logger.debug("asd")
                break


        global other_comments

        for i in other_comments_set:
            try:
                logger.debug(User.objects.get(username=i["to_username"]))
                other_comments = OtherComments.objects.get(user_to=User.objects.get(username=i["to_username"]))
                other_comments.other_comment_text = i["other_comment_text"]
                other_comments.latest_change_time_stamp = timezone.now()
                other_comments.author = user
                other_comments.save()

            except OtherComments.DoesNotExist:
                new_other_comment=OtherComments(other_comment_text=i["other_comment_text"],
                                                author=user,
                                                user_to=User.objects.get(username=i["to_username"]))
                new_other_comment.save()



        return render(request,"error.html",{"error_msg":"保存成功！",
                                        "login_info": get_login_info(request)})
    else:
        user=request.user
        users=[]
        for i in User.objects.all():
            users.append(i.username)

        try:
            global old_main_comment_text
            old_main_comment=MainComment.objects.get(author=user)
            old_main_comment_text=old_main_comment.main_comment_text
        except MainComment.DoesNotExist:
            old_main_comment_text=""

        old_other_comments_set=[]
        counter=1

        
        class Entry():
            def __init__(self,number,text,select):
                self.number=number
                self.text=text
                self.select=select
        try:
            old_other_comments=OtherComments.objects.filter(author=user)
            for old_other_comment in old_other_comments:
                old_other_comments_set.append(Entry(counter,
                                                    old_other_comment.other_comment_text,
                                                    old_other_comment.user_to.username))
                counter=counter+1
        except OtherComments.DoesNotExist:
            old_main_comment_text=""



        return render(request,"edit.html",{"login_info": get_login_info(request),
                                           "users":users,
                                           "counter":counter,
                                           "old_other_comments":old_other_comments_set,
                                           "old_main_comment":old_main_comment_text})















def error(request):
    return render(request,"error.html")

def test(request):
    if request.POST:
        while True:
            a=request.POST.get("b")
            logger.debug("a")
    else:
        return render(request,"test.html")

