from django.shortcuts import render, get_object_or_404
from .models import *
from .forms import *
from django.views.generic import CreateView
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from datetime import timedelta

def index(request):
    return render(request, 'index.html')



class UserSignupView(CreateView):
    model = User
    form_class = UserSignupForm
    template_name = 'user_signup.html'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('/previous_orders/')

class UserLoginView(LoginView):
    template_name='login.html'


def logout_user(request):
    logout(request)
    return redirect("/")

@login_required(login_url='/accounts/login/')
def order_pizza(request):
    if request.method == 'POST':
        form = PizzaForm(request.POST)
        if form.is_valid():
            pizza = form.save()
            return redirect('order', pizzaid=pizza.id)
        else:
            return render(request, 'pizza.html', {'form': form})
    else:
        form = PizzaForm()
        return render(request, 'pizza.html', {'form': form})



@login_required
def order(request, pizzaid):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():

            order = form.save(commit=False)
            
            data = form.cleaned_data
            order.eircode = format_eircode(data['eircode']) # instance from modelform docs

            user = request.user
            pizza = get_object_or_404(Pizza, id=pizzaid)
            pizzauser = PizzaUser.objects.create(user=user, pizza=pizza)

            order = form.save()

            return redirect('confirmation', orderid=order.id)
        else:
            return render(request, 'order.html', {'form': form})
    else:
        form = OrderForm()
        return render(request, 'order.html', {'form': form})
    
@login_required
def confirmation(request , orderid):
    order = get_object_or_404(Order, id=orderid)
    pizzauser = PizzaUser.objects.filter(user=request.user).latest('time_ordered')
    pizza = pizzauser.pizza

    time_ordered = pizzauser.time_ordered
    delivery_time = time_ordered + timedelta(minutes=30)
    pizzauser.time_ordered = time_ordered.strftime('%d-%m-%Y %H:%M %p')
    delivery_time_no_year = delivery_time.strftime('%H:%M %p')
    delivery_time = delivery_time.strftime('%d-%m-%Y %H:%M %p')

    return render(request, 'details.html', {'pizza': pizza, 'order': order, 'delivery_time': delivery_time, 'pizzauser': pizzauser, 'delivery_time_no_year': delivery_time_no_year})


@login_required
def previous_orders(request):
    user = request.user
    orders = PizzaUser.objects.filter(user=user)

    for order in orders:
        order.time_ordered = order.time_ordered.strftime('%d-%m-%Y %H:%M %p')

    return render(request, 'previous_orders.html', {'orders': orders})
