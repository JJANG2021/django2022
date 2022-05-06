from django.shortcuts import render, redirect
from .models import Board, Reply
from django.utils import timezone
from django.core.paginator import Paginator
from django.contrib import messages

# Create your views here.
def rlikey(req, bpk):
    b = Board.objects.get(id=bpk)
    b.likey.remove(req.user)
    return redirect("board:detail", bpk)


def likey(req, bpk):
    b = Board.objects.get(id=bpk)
    b.likey.add(req.user)
    return redirect("board:detail", bpk)


def dreply(req, bpk, rpk):
    r = Reply.objects.get(id=rpk)
    if r.replyer == req.user:
        r.delete()
    else:
        messages.warning(req, "답변삭제에 고의적 접근으로 인한 해킹일 경우 법적처벌을 받을 수 있습니다.")
    return redirect("board:detail", bpk)


def creply(req, bpk):
    b = Board.objects.get(id=bpk)
    r = req.POST.get("rcom")
    Reply(board=b, replyer=req.user, comment=r).save()
    return redirect("board:detail", bpk)


def update(req, bpk):
    b = Board.objects.get(id=bpk)
    if b.writer != req.user:
        return redirect(req, "board:index")
    if req.method == "POST":
        s = req.POST.get("bsub")
        c = req.POST.get("bcon")
        b.subject = s
        b.content = c
        b.save()
        return redirect("board:detail", bpk)
    context = {
        "b" : b
    }
    return render(req, "board/update.html", context)


def create(req):
    if req.method == "POST":
        s = req.POST.get("bsub")
        c = req.POST.get("bcon")
        Board(subject=s, writer=req.user, content=c, pubdate=timezone.now()).save()
        return redirect("board:index")
    return render(req, "board/create.html")


def delete(req, bpk):
    b = Board.objects.get(id=bpk)
    if b.writer == req.user:
        messages.info(req, "글삭제가 정상적으로 완료되었습니다.")
        b.delete()
    else:   # HACKING
        messages.warning(req, "글삭제에 고의적 접근으로 인한 해킹일 경우 법적처벌을 받을 수 있습니다.")
    return redirect("board:index")


def detail(req, bpk):
    b = Board.objects.get(id=bpk)
    r = b.reply_set.all()
    context = {
        "b" : b,
        "rset" : r
    }
    return render(req, "board/detail.html", context)


def index(req):
    pg = req.GET.get("page",1)
    cate = req.GET.get("cate", "")
    kw = req.GET.get("kw", "")

    if kw:
        if cate == "sub":
            b = Board.objects.filter(subject__startswith=kw)
        elif cate == "wri":
            try:
                from acc.models import User
                u = User.objects.get(username=kw)
                b = Board.objects.filter(writer=u)  # 작성자를 회원으로 검색
            except:
                b = Board.objects.none()    # 아무것도 없는 레코드 설정
        elif cate == "con":
            b = Board.objects.filter(content__contains=kw)
        else:
            pass
    else:
        b = Board.objects.all()
    
    b = b.order_by('-pubdate')   # 최신글 위로
    
    pag = Paginator(b, 5)
    obj = pag.get_page(pg)
    context = {
        "bset" : obj,
        "cate" : cate,
        "kw" : kw,
    }
    return render(req, "board/index.html", context)