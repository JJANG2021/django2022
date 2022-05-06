from django.shortcuts import redirect, render
from .models import Topic, Choice
from django.utils import timezone
from django.contrib import messages

# Create your views here.
def delete(req, tpk):
    t = Topic.objects.get(id=tpk)
    # c = t.choice_set.all()
    if req.user == t.maker:
        t.delete()
        # c.pic.delete()
    else:
        messages.warning(req, "투표글삭제에 고의적 접근으로 인한 해킹일 경우 법적처벌을 받을 수 있습니다.")
    return redirect("vote:index")


def create(req):
    if req.method == "POST":
        s = req.POST.get("sub")
        c = req.POST.get("con")
        cn = req.POST.getlist("chn")
        cf = req.FILES.getlist("chf")   # INPUT TYPE FILE 일때!!
        cc = req.POST.getlist("chc")
        # print(s,c,cn,cf,cc)
        t = Topic(subject=s, maker=req.user, content=c, pubdate=timezone.now())
        t.save()
        for name, pic, con in zip(cn, cf, cc):
            Choice(topic=t, name=name, pic=pic, con=con).save()
        return redirect("vote:index")
    return render(req, "vote/create.html")


def cancel(req, tpk):
    t = Topic.objects.get(id=tpk)
    t.voter.remove(req.user)
    # 사용자 기준 투표한 모든값 중 현재 토픽에 대한 투표값
    req.user.choice_set.get(topic=t).choicer.remove(req.user)
    return redirect("vote:detail", tpk)


def vote(req, tpk):
    t = Topic.objects.get(id=tpk)
    if not req.user in t.voter.all():   # 다중투표 불가
        t.voter.add(req.user)
        cpk = req.POST.get("cho")
        c = Choice.objects.get(id=cpk)
        c.choicer.add(req.user)
    return redirect("vote:detail", tpk)


def detail(req, tpk):
    t = Topic.objects.get(id=tpk)
    c = t.choice_set.all()
    context = {
        "t" : t,
        "cset" : c
    }
    return render(req, "vote/detail.html", context)


def index(req):
    t = Topic.objects.all()
    context ={
        "tset" : t,
    }
    return render(req, "vote/index.html", context)