from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password
from .models import User
from django.contrib import messages

# Create your views here.
def delete(req):
    pw = req.POST.get("pwck")
    if check_password(pw, req.user.password):
        req.user.delete()
        return redirect("acc:index")
    else:
        messages.error(req, "패스워드가 틀렸습니다.")
        return redirect("acc:profile")

def update(req):
    if req.method == "POST":
        u = req.user
        up = req.POST.get("upass")
        uc = req.POST.get("ucomm")
        pi = req.FILES.get("upic")
        ue = req.POST.get("umail")
        if up:
            u.set_password(up)  # 비번 암호화 수정
        if pi:
            u.pic = pi
        u.comment = uc
        u.email = ue
        u.save()
        login(req,u)
        return redirect("acc:profile")
    return render(req, "acc/update.html")


def signup(req):
    if req.method == "POST":
        un = req.POST.get("uname")
        up = req.POST.get("upass")
        uc = req.POST.get("ucomm")
        pi = req.FILES.get("upic")
        User.objects.create_user(username=un,password=up,comment=uc,pic=pi)
        return redirect("acc:login")
    return render(req, "acc/signup.html")


def profile(req):
    return render(req, "acc/profile.html")


def logout_user(req):
    logout(req) # request 에 실린 user 빼냄
    return redirect("acc:index")


def login_user(req):
    if req.method == "POST":
        un = req.POST.get("uname")
        up = req.POST.get("upass")

        # authenticate 는 사용자의 username, password 통해 인증
        u = authenticate(username=un, password=up)
        if u:   # 로그인 성공했을 떄
            login(req, u)
            messages.success(req, f"{u}! WELCOME~")
            return redirect("acc:index")
        else:
            messages.error(req, "계정정보가 일치하지 않습니다.")
    return render(req, "acc/login.html")


def index(req):
    return render(req, "acc/index.html")