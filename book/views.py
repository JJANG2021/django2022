from django.shortcuts import redirect, render
from .models import Book

# Create your views here.
def create(req):
    if req.method == "POST":
        im = req.POST.get("impo")
        sn = req.POST.get("sname")
        su = req.POST.get("surl")
        sc = req.POST.get("scon")
        # print(im, sn, su, sc) # DATA 전송 CHECK
        Book(site_name=sn, site_url=su, site_con=sc, impo=bool(im), maker=req.user).save()
        return redirect("book:index")
    return render(req, "book/create.html")


def index(req):
    b = req.user.book_set.all() # 사용자별 북마크 가져오기
    context = {
        "bset" : b
    }
    return render(req, "book/index.html", context)