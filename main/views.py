from django.shortcuts import render
from django.contrib import messages
import uuid
import hashlib
from datetime import date
from .models import SiteUsers, Product, Categories, CategoriesOfProduct, Trashbox, Saeles
from django.http import HttpResponse, HttpResponseRedirect
from django.core.files.storage import FileSystemStorage
userlogin = ""

def homep(request):
    # POST - обязательный метод
    if request.method == 'POST' and request.FILES:
        # получаем загруженный файл
        file = request.FILES['myfile1']
        fs = FileSystemStorage()
        # сохраняем на файловой системе
        filename = fs.save(file.name, file)
        # получение адреса по которому лежит файл
        file_url = fs.url(filename)
        return render(request, 'main/homep.html', {'file_url': file_url})
    return render(request, 'main/homep.html')

def hash_password(password):
    # uuid используется для генерации случайного числа
    salt = uuid.uuid4().hex
    return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt


def check_password(hashed_password, user_password):
    password, salt = hashed_password.split(':')
    return password == hashlib.sha256(salt.encode() + user_password.encode()).hexdigest()

def test(request):
    return render(request, 'main/test.html')

def lk(request):
    global userlogin
    user = SiteUsers.objects.get(login=userlogin)
    users = SiteUsers.objects.all()
    usertrash = Trashbox.objects.filter(id_user=user.id)
    sales = Saeles.objects.filter(id_users=SiteUsers.objects.get(login=userlogin))
    allsales = Saeles.objects.all()
    vigoda = 0
    for el in allsales:
        vigoda += (el.id_product.cost_on_sell - el.id_product.cost_on_buy)
    if user.role == "User" or user.role == "Manager":
        return render(request, 'main/lk.html', {'userlogin': userlogin, 'user': user, 'all': len(usertrash), 'sales': sales})
    elif user.role == "Owners":
        return render(request, 'main/lkpr.html', {'userlogin': userlogin, 'user': user, 'users': users, 'all': len(usertrash), 'sales': sales, 'vigoda': vigoda})
    else:
        return HttpResponse('Some Problem')


def loggout(request):
        global userlogin
        userlogin = ""
        return render(request, 'main/Main.html')


def tovar(request, prod_id):
    global userlogin
    user = SiteUsers.objects.get(login=userlogin)
    usertrash = Trashbox.objects.filter(id_user=user.id)
    tovar = Product.objects.get(id=prod_id)
    return render(request, 'main/tovar.html', {'userlogin': userlogin, 'all': len(usertrash), 'tovar': tovar})

def previos(request, prod_id):
    global userlogin
    user = SiteUsers.objects.get(login=userlogin)
    usertrash = Trashbox.objects.filter(id_user=user.id)
    tovarlen = len(Product.objects.all())
    prod_id = prod_id - 1 + tovarlen
    if prod_id > tovarlen:
        tovar = Product.objects.get(id=(prod_id % tovarlen))
    elif prod_id == 0:
        tovar = Product.objects.get(id=1)
    else:
        tovar = Product.objects.get(id=prod_id)
    return render(request, 'main/tovar.html', {'userlogin': userlogin, 'all': len(usertrash), 'tovar': tovar})

def next(request, prod_id):
    global userlogin
    user = SiteUsers.objects.get(login=userlogin)
    usertrash = Trashbox.objects.filter(id_user=user.id)
    tovarlen = len(Product.objects.all())
    prod_id = prod_id + 1 + tovarlen
    if prod_id % tovarlen == 0:
        tovar = Product.objects.get(id=tovarlen)
    else:
        tovar = Product.objects.get(id=(prod_id % tovarlen))
    return render(request, 'main/tovar.html', {'userlogin': userlogin, 'all': len(usertrash), 'tovar': tovar})



def postuserentry(request):
    # получаем из данных запроса POST отправленные через форму данные
    email = request.POST.get("email", "none")
    pasword = request.POST.get("pasword", "")

    user = SiteUsers.objects.all()
    spis = []
    for person in user:
        spis.append(person.email)
    if email in spis:
        useremail = SiteUsers.objects.get(email=email)
        if check_password(useremail.pasword, pasword):
            global userlogin
            userlogin = useremail.login
            return render(request, 'main/Main.html', {'userlogin': userlogin})
        else:
            return HttpResponseRedirect('entry' + "#wrongpassword")
    else:
        return HttpResponseRedirect('entry' + "#wronguser")

def deltovar(request, prod_id):
    global userlogin
    user = SiteUsers.objects.get(login=userlogin)
    usertrash = Trashbox.objects.filter(id_user=user.id)
    deltovar = Product.objects.get(id=prod_id)
    deltovar.delete()
    dictionaty = []
    products = Product.objects.all()
    return render(request, 'main/shoppr.html', {'products': products, 'userlogin': userlogin, 'massa': dictionaty, 'all': len(usertrash)})

def deltovartrash(request, prod_id):
    global userlogin
    user = SiteUsers.objects.get(login=userlogin)
    deltovar = Trashbox.objects.get(id=prod_id)
    deltovar.delete()
    usertrash = Trashbox.objects.filter(id_user=user.id)
    productsin = Trashbox.objects.all()
    return render(request, 'main/trashbox.html', {'productsin': productsin, 'userlogin': userlogin, 'all': len(usertrash)})

def makesell(request):
    global userlogin
    user = SiteUsers.objects.get(login=userlogin)
    users = SiteUsers.objects.all()
    usertrash = Trashbox.objects.filter(id_user=user.id)
    if usertrash:
        for i in usertrash:
            current_date = date.today()
            id_product = i.id_product.id
            sell = Saeles.objects.create(id_users=SiteUsers.objects.get(login=userlogin),
                                         id_product=Product.objects.get(id=id_product), date=current_date,
                                         price=i.id_product.cost_on_sell)
            i.delete()
    else:
        print(usertrash)
    usertrash = Trashbox.objects.filter(id_user=user.id)
    products = Product.objects.all()
    if user.role == "Owners" or user.role == "Manager":
        return render(request, 'main/shoppr.html',
                      {'products': products, 'userlogin': userlogin, 'all': len(usertrash)})
    else:
        return render(request, 'main/shop.html',
                      {'products': products, 'userlogin': userlogin, 'all': len(usertrash)})

def trashbox(request):
    global userlogin
    user = SiteUsers.objects.get(login=userlogin)
    usertrash = Trashbox.objects.filter(id_user=user.id)
    productsin = Trashbox.objects.all()
    return render(request, 'main/trashbox.html', {'productsin': productsin, 'userlogin': userlogin, 'all': len(usertrash)})


def vkorzinu(request, prod_id):
    global userlogin
    trash = Trashbox.objects.create(id_user=SiteUsers.objects.get(login=userlogin), id_product=Product.objects.get(id=prod_id))
    user = SiteUsers.objects.get(login=userlogin)
    usertrash = Trashbox.objects.filter(id_user=user.id)
    products = Product.objects.all()
    dictionaty = {}
    if user.role == "Owners" or user.role == "Manager":
        return render(request, 'main/shoppr.html',
                      {'products': products, 'userlogin': userlogin, 'massa': dictionaty, 'all': len(usertrash)})
    else:
        return render(request, 'main/shop.html',
                      {'products': products, 'userlogin': userlogin, 'massa': dictionaty, 'all': len(usertrash)})

def changerole(request):
    login = request.POST.get("user")
    role = request.POST.get("role")
    newuser = SiteUsers.objects.get(login=login)
    newuser.role = role
    newuser.save()
    global userlogin
    user = SiteUsers.objects.get(login=userlogin)
    users = SiteUsers.objects.all()
    return render(request, 'main/lkpr.html', {'userlogin': userlogin, 'user': user, 'users': users})

def newtovar(request):
    global userlogin
    cost_on_sell = request.POST.get("cost_on_sell", "none")
    cost_on_buy = request.POST.get("cost_on_buy", "none")
    name = request.POST.get("name", "none")
    quantity_on_stock = request.POST.get("quantity_on_stock", "none")
    if request.method == 'POST' and request.FILES:
        # получаем загруженный файл
        picture = request.FILES.get('picture')
        fs = FileSystemStorage()
        # сохраняем на файловой системе
        filename = fs.save(picture.name, picture)
        file_url = "img/" + picture.name
        Product.objects.create(cost_on_sell=cost_on_sell, cost_on_buy=cost_on_buy, name=name,
                               quantity_on_stock=quantity_on_stock, picture=file_url)
    else:
        Product.objects.create(cost_on_sell=cost_on_sell, cost_on_buy=cost_on_buy, name=name,
                               quantity_on_stock=quantity_on_stock, picture="main/img/awaysocks24-25.png")
    products = Product.objects.all()
    catofprod = CategoriesOfProduct.objects.all()
    dictionaty = {}
    user = SiteUsers.objects.get(login=userlogin)
    usertrash = Trashbox.objects.filter(id_user=user.id)
    return render(request, 'main/shoppr.html', {'products': products, 'userlogin': userlogin, 'massa': dictionaty, 'all': len(usertrash)})



def postuser(request):
    # получаем из данных запроса POST отправленные через форму данные
    login = request.POST.get("login", "none")
    pasword = request.POST.get("pasword", "")
    pasword1 = request.POST.get("pasword1", "")
    email = request.POST.get("email", "def@def")
    if len(login) == 0 or len(pasword) == 0 or len(email) == 0 or len(pasword1) == 0:
        return HttpResponseRedirect('registration'+"#emptydata")
    else:
        if pasword == pasword1:
            user = SiteUsers.objects.all()
            spis = []
            for person in user:
                spis.append(person.email)
            if email in spis:
                return HttpResponseRedirect('registration'+"#sameemail")
            else:
                global userlogin
                userlogin = login
                hashed_password = hash_password(pasword)
                SiteUsers.objects.create(login=login, pasword=hashed_password, email=email, role="User")
                return render(request, 'main/Main.html', {'userlogin': userlogin})
        else:
            return HttpResponseRedirect('registration'+"#incorrectpassword")


def index(request):
    global userlogin
    if userlogin:
        user = SiteUsers.objects.get(login=userlogin)
        usertrash = Trashbox.objects.filter(id_user=user.id)
        return render(request, 'main/Main.html', {'userlogin': userlogin, 'all': len(usertrash)})
    else:
        return render(request, 'main/Main.html')



def history(request):
    global userlogin
    if userlogin:
        user = SiteUsers.objects.get(login=userlogin)
        usertrash = Trashbox.objects.filter(id_user=user.id)
        return render(request, 'main/History.html', {'userlogin': userlogin, 'all': len(usertrash)})
    else:
        return render(request, 'main/History.html')

def entry(request):
    return render(request, 'main/Entry.html')

def team(request):
    global userlogin
    if userlogin:
        user = SiteUsers.objects.get(login=userlogin)
        usertrash = Trashbox.objects.filter(id_user=user.id)
        return render(request, 'main/Team.html', {'userlogin': userlogin, 'all': len(usertrash)})
    else:
        return render(request, 'main/Team.html')

def registration(request):
    return render(request, 'main/Registration.html')

def shop(request):
    global userlogin
    try:
        user = SiteUsers.objects.get(login=userlogin)
        usertrash = Trashbox.objects.filter(id_user=user.id)
        products = Product.objects.all()
        catofprod = CategoriesOfProduct.objects.all()
        if user.role == "Owners" or user.role == "Manager":
            return render(request, 'main/shoppr.html',
                          {'products': products, 'userlogin': userlogin, 'catofprod': catofprod, 'all': len(usertrash)})
        else:
            return render(request, 'main/shop.html',
                          {'products': products, 'userlogin': userlogin, 'catofprod': catofprod, 'all': len(usertrash)})
    except SiteUsers.DoesNotExist:
        return HttpResponse('You do not have permission to visit this page')


