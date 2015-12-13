from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .forms import Login, Registration
from models import Flower, Cart, CartDetail, Order
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse

class Index(View):  # renders initial log/reg screen
    def get(self, request):
        logform = Login()
        regform = Registration()
        return render(request, 'flower/index.html', {'logform': logform, 'regform': regform})

class Log(View): # logs user in
    def post(self, request):
        form = Login(request.POST)
        if form.is_valid():
            user = authenticate(username=request.POST['username'], password=request.POST['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('/main')
                else: 
                    print('The password is valid, the teh user')
                    return redirect('/')
            else:
                print("The username and password were incorrect.")
                return redirect('/')
        else:
            return redirect('/')

class Reg(View): # registers user
    def post(self, request):
        form = Registration(request.POST)
        if form.is_valid():
            form = form.cleaned_data
            if form['password'] != form['confirm']:
                return redirect('/')
            else:
                User.objects.create_user(username = form["username"], email = form["email"], password = form["password"])
                user = authenticate(username=request.POST['username'], password=request.POST['password'])
                login(request, user)
                logged_in_user = User.objects.filter(id = request.user.id)[0]
                Cart.objects.create(user=logged_in_user)
                return redirect('/main')
        else:
            return redirect('/')

class Logout(View): # logs out user
    def get(self,request):
        logout(request)
        return redirect('/')

class Main(View): #renders main flower page and sends flowers to template
    def get(self, request):
        flower = self.paginate(request)
        return render(request, 'flower/main.html', flower)

    def post(self, request):
        flower = self.paginate(request)
        return render(request, 'flower/main.html', flower)

    def paginate(self, request):
        flower_list =  Flower.objects.all()
        paginator = Paginator(flower_list, 16)
        page = request.GET.get('page')
        try: 
            flowers = paginator.page(page)
        except PageNotAnInteger:
            flowers = paginator.page(1)
        except EmptyPage:
            flowers = paginator.page(paginator.num_pages)
        return {'flowers': flowers}

class AddToCart(View): 
    def post(self, request):
        flower_inst = Flower.objects.filter(id = request.POST['flower_id'])[0]
        user_cart = request.user.cart
        cart_item = CartDetail(flower = flower_inst, cart = user_cart)
        print user_cart
        cart_item.save()
        return JsonResponse({'status': True})

class ShowCart(View):
    def post(self, request):
        context = self.show_user_cart(request)
        return render(request, 'flower/order.html', context)

    def get(self, request):
        context = self.show_user_cart(request)
        return render(request, 'flower/order.html', context)

    def show_user_cart(self,request):
        cart = Cart.objects.filter(user_id = request.user.id)[0]
        flowers_in_cart = cart.cart_details.all()
        flowers_counted = self.Count_Flowers(flowers_in_cart)
        context = {
            'flowers' : flowers_counted,
        }
        return {'flowers' : flowers_counted}

    def Count_Flowers(self, arr_of_flower_objects):
        flowers_counted = {}
        flowers_list = []
        for flower_type in arr_of_flower_objects:
            flowers_counted.setdefault(flower_type.flower.name, 0)
            flowers_counted[flower_type.flower.name]+=1
        for i, j in flowers_counted.items():
            flower_quantity = "{}: {}".format(i, j)
            flowers_list.append(flower_quantity)
        return flowers_list

class Checkout(View):
    def post(self, request):
        user_cart = Cart.objects.filter(user_id = request.user.id)[0]
        cart_details = user_cart.cart_details.all()
        user_of_cart = user_cart.user
        Order.objects.create(user = user_of_cart, order = cart_details)
        cart_details.delete()
        return redirect('/main?page=1')
                    