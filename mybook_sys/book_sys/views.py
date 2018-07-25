from django.shortcuts import render,redirect,HttpResponse
from book_sys.models import *
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage  # 分页器类
from django.contrib.auth.models import User  # 导入django的user表
from django.db import connection
from django import forms
import json
# Create your views here.


class Myform(forms.Form):
    user = forms.CharField(min_length=6)
    pwd = forms.IntegerField()
    agent_pwd = forms.IntegerField()
    email = forms.CharField()


def login(request):
    if request.method == 'POST':
        user = request.POST.get('user')
        pwd = request.POST.get('pwd')
        users = auth.authenticate(username=user, password=pwd)
        if users:
            auth.login(request,users)
            return redirect('/index/')
        else:
            error_msg = '用户名或密码错误'
    return render(request, 'login.html',locals())


# 判断是否登录过用户
@login_required()
def index(request):
    user_msg = request.user
    cursor = connection.cursor()
    cursor.execute("select a.id,a.title,a.price,b.pname,d.aname from book_sys_book as a,book_sys_publish as b,book_sys_book_authors as c,book_sys_author as d where a.publish_id = b.id and a.id = c.book_id and c.author_id = d.id order by id asc;")
    book_list = cursor.fetchall()
    book_list_obj = Book.objects.all()
    publish_list = Publish.objects.all()
    author_list = Author.objects.all()
    return render(request,'index.html',locals(),{"user_msg":user_msg,})


def register(request):
    form_obj = Myform()
    error_msg = ''
    if request.method == 'POST':
        form_post = Myform(request.POST)
        if form_post.is_valid:
            pwd = request.POST.get('pwd')
            agent_pwd = request.POST.get('agent_pwd')
            user_exists = User.objects.filter(username=request.POST.get('user'))
            if pwd == agent_pwd and not user_exists:
                User.objects.create_user(
                    username=request.POST.get('user'),
                    password=pwd,
                    email=request.POST.get('email')
                )
                return redirect('/login/')
            else:
                error_msg = '密码输入不相符|或用户已存在'
        else:
            error_msg = form_post.errors
    return render(request, 'register.html',{"form_obj":form_obj,"error_msg":error_msg})


def login_out(request):
    auth.logout(request)
    return redirect('/login/')


def edit_book(request):
    user_msg = request.user
    # edit_id = request.GET.get('edit')
    book_list = Book.objects.all()
    publish_list = Publish.objects.all()
    author_list = Author.objects.all()
    return render(request, 'edit_book.html', locals())


def edit_book_in(request):
    user_msg = request.user
    edit_id = request.GET.get('edit')
    edit_data = Book.objects.filter(id=edit_id)
    publish_list = Publish.objects.all()
    show_aut_data = Author.objects.all()
    if request.method == 'POST':
        edit_id = request.POST.get('id')  # book_id
        aut_data = []  # 存放修改的用户名
        obj = []       # 存放修改的对象
        not_aut_data = []   # 存放不修改的用户名
        not_aut_obj = []   # 存放不修改的用户名对象
        book_obj = Book.objects.get(id=edit_id)
        author_data = Author.objects.all()

        for i in author_data:
            aname = request.POST.get(i.aname) # 前端传递的是每个obj对应的aname
            if aname:
                aut_data.append(aname)
            else:
                not_aut_data.append(i.aname)
        for i in aut_data:
            obj.append(Author.objects.get(aname=i))
        for ii in obj:
            book_obj.authors.add(ii)
        for j in not_aut_data:
            not_aut_obj.append(Author.objects.get(aname=j))
        for jj in not_aut_obj:
            book_obj.authors.remove(jj)
        title = request.POST.get('title')
        price = request.POST.get('price')
        pub_pname = request.POST.get('publish_name')
        pub_id = Publish.objects.get(pname=pub_pname).id
        # Book.objects.filter(id=edit_id).update(title=title,price=price)
        cursor = connection.cursor()
        cursor.execute("update book_sys_book set publish_id = %s where id = %s;" %(pub_id, edit_id))
        return redirect('/index/')
    return render(request,'edit_book_in.html',locals())


def edit_publish(request):
    '''
    显示对应的出版社出版的书
    :param request:
    :return: edit_publish.html
    '''
    user_msg = request.user
    pname = request.GET.get('name')
    book_list = Book.objects.all()
    publish_list = Publish.objects.all()
    author_list = Author.objects.all()
    pub = Publish.objects.get(pname=pname)
    if not pub:
        return redirect('/index/')
    else:
        book_list_new = pub.book_set.all()
    return render(request,'edit_publish.html',locals())


def edit_publish_in(request):
    user_msg = request.user
    edit_id = request.GET.get('edit')
    edit_data = Publish.objects.filter(book__title=edit_id)
    if request.method == 'POST':
        edit_ids = request.POST.get('id')
        pname = request.POST.get('pname')
        addr = request.POST.get('addr')
        Publish.objects.filter(id=edit_ids).update(pname=pname,addr=addr)
        return redirect('/index/')
    return render(request, 'edit_publish_in.html',locals())


def edit_author(request):
    user_msg = request.user
    aname = request.GET.get('name')
    book_list = Book.objects.all()
    publish_list = Publish.objects.all()
    author_list = Author.objects.all()
    aut = Author.objects.get(aname=aname)
    book_list_new = aut.book_set.all()
    return render(request,'edit_author.html',locals())


def edit_author_in(request):
    user_msg = request.user
    edit_id = request.GET.get('edit')
    edit_data = Author.objects.filter(book__title=edit_id)
    if request.method == 'POST':
        edit_id = request.POST.get('id')
        aname = request.POST.get('aname')
        Author.objects.filter(id=edit_id).update(aname=aname)
        return redirect('/index/')
    return render(request, 'edit_author_in.html',locals())


def del_book(request):
    if request.method == 'POST':
        del_id = request.POST.get('del')
        Book.objects.filter(id=del_id).delete()
        return render(request, 'edit_book.html')


def del_publish(request):
    if request.method == 'POST':
        del_id = request.POST.get('del')
        Publish.objects.filter(book__title=del_id).delete()
        return render(request, 'index.html')


def del_publish_list(request):
    data = request.GET.get('name')
    Publish.objects.filter(pname=data).delete()
    return redirect('/index/')


def del_author(request):
    if request.method == 'POST':
        del_id = request.POST.get('del')
        book_id_name = Book.objects.filter(id=del_id).values('authors__aname').first()['authors__aname']
        Author.objects.filter(aname=book_id_name).delete()
        return render(request, 'index.html')


def del_author_list(request):
    data = request.GET.get('name')
    Author.objects.filter(aname=data).delete()
    return redirect('/index/')


def add_book(request):
    user_msg = request.user
    error_msg = ''
    msg1 = 'title'
    msg2 = 'price'
    msg3 = ''
    show_pub_data = Publish.objects.all()
    show_aut_data = Author.objects.all()
    if not show_aut_data or not show_pub_data:
        error_msg = '请完善相关信息（出版社、作者）'
        return render(request, 'add_book.html',{"error_msg":error_msg})

    if request.method == 'POST':
        title = request.POST.get('title')
        price = request.POST.get('price')
        publish_id = request.POST.get('publish_id') # 前端POST提交之后传递的{name = publish_id}
        title_old = []
        # 获取现在已经有的title
        for i in Book.objects.all():
            title_old.append(i.title)

        _publish_id = Publish.objects.get(pname=publish_id).id
        aut_data = []
        author_data = Author.objects.all()
        for i in author_data:
            aname = request.POST.get(i.aname)  # 前端传递的是每个obj对应的aname
            if aname:
                aut_data.append(aname)
        if not aut_data:
            msg3 = '请选择作者'
            return render(request, 'add_book.html', locals())
        elif title == msg1 or title == '请输入书名' or title in title_old:
            msg1 = '请输入书名'
            return render(request, 'add_book.html', locals())
        elif price == msg2 or price == '请输入价格':
            msg2 = '请输入价格'
            return render(request, 'add_book.html', locals())
        else:
            book = Book(title=title, price=price, publish_id=_publish_id)
            book.save()
            book_obj = Book.objects.get(title=title)
            obj = []
            for i in aut_data:
                obj.append(Author.objects.get(aname=i))

            for ii in obj:
                book_obj.authors.add(ii)

    return render(request, 'add_book.html',locals())


def add_publish(request):
    user_msg = request.user
    msg1 = 'pname'
    msg2 = 'addr'
    msg3 = ''
    if request.method == 'POST':
        old_data = []
        pname = request.POST.get('pname')  # 前端传递的key=pname
        addr = request.POST.get('addr')   # 前端传递的key=addr
        # 取出所有出版社的pname
        for i in Publish.objects.all():
            old_data.append(i.pname)

        if pname == msg1 or addr == msg2:
            msg3 = '请填写完整信息(或信息有误)'
            return render(request, 'add_publish.html', locals())
        elif pname in old_data:
            msg3 = '请填写完整信息(或信息有误)'
            return render(request, 'add_publish.html', locals())
        else:
            p = Publish(pname=pname,addr=addr)
            p.save()
    return render(request, 'add_publish.html', locals())


def add_author(request):
    user_msg = request.user
    msg1 = 'aname'
    if request.method == 'POST':
        aname = request.POST.get('aname')
        if aname == msg1 or aname == '请填写完整信息':
            msg1 = '请填写完整信息'
            return render(request, 'add_author.html', locals())
        else:
            a = Author(aname=aname)
            a.save()
    return render(request, 'add_author.html', locals())