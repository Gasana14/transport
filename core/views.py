from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import RegistrationForm, VehicleForm
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Customer, Vehicle, Driver, Delivery
from django.utils.crypto import get_random_string
# Create your views here.


def home_page(request):
    return render(request, 'home_page.html')


def login_page(request):
    return render(request, 'login_page.html')


def register_page(request):
    return render(request, 'register_page.html')


@login_required
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')


@login_required
def customer_dashboard(request):
    user = request.user
    client = Customer.objects.get(account=user)
    if client is None:
        messages.error(request, 'Not a client account')
        return redirect('home')
    else:
        deliveries = Delivery.objects.filter(owner=client)
        print(deliveries)
    return render(request, 'customer_dashboard.html', {"deliveries": deliveries})


@login_required
def record_new_carriage(request):
    user = request.user

    if request.method == 'GET':
        client = Customer.objects.get(account=user)
        if client is None:
            messages.error(request, 'Not a client account')
            return redirect('home')
        else:
            # deliveries = Delivery.objects.filter(owner=client)
            return render(request, 'new_carriage.html')
    else:
        user = request.user
        owners = Customer.objects.filter(account=user)
        if owners.exists():
            departure_date_time = request.POST.get('departure_date_time')
            arrival_date_time = request.POST.get('arrival_date_time')
            kilograms = request.POST.get('kilograms')
            destination = request.POST.get('destination')
            origin = request.POST.get('origin')
            price = request.POST.get('price')

            Delivery.objects.create(owner=owners[0],
                                    departure_date_time=departure_date_time,
                                    arrival_date_time=arrival_date_time,
                                    kilograms=kilograms,
                                    destination=destination,
                                    origin=origin,
                                    price=price)
            return redirect('customer_dashboard')
        else:
            messages.error(request, 'You do not have a customer account.')
            return redirect('record_new_carriage')


@login_required
def driver_dashboard(request):
    user = request.user
    driver = Driver.objects.get(account=user)
    if driver is None:
        messages.error(request, 'Not a driver account')
        return redirect('home')
    else:

        deliveries = Delivery.objects.filter(status='W').order_by('departure_date_time')

    return render(request, 'driver_dashboard.html', {"deliveries": deliveries})


@login_required
def driver_missions(request):
    # this cods are repeated
    # can make a function!
    user = request.user
    driver = Driver.objects.get(account=user)
    if driver is None:
        messages.error(request, 'Not a driver account')
        return redirect('home')
    else:
        deliveries = Delivery.objects.filter(driver=driver)

    return render(request, 'driver_missions.html', {"deliveries": deliveries})


def register_account(request):

    if request.method == 'POST':
        reg_form = RegistrationForm(request.POST)
        vehicle_form = VehicleForm(request.POST)

        if reg_form.is_valid():
            email = reg_form.cleaned_data.get('email')

            try:
                user = User.objects.create_user(username=email,
                                                email=email,
                                                password=reg_form.cleaned_data.get('password'),
                                                first_name=str(email).split('@')[0],
                                                last_name='Last name')
            except Exception as e:
                messages.error(request, f"Could not create the account with user name {reg_form.cleaned_data.get('email')}")
                return redirect('home')

            is_admin = reg_form.cleaned_data.get('is_admin')
            if is_admin == 'is_admin':
                user.is_staff = True
                user.save()
                login(request, user=user)
            else:
                is_customer = reg_form.cleaned_data.get('is_customer')
                print(is_customer)
                if is_customer == 'is_customer':
                    try:
                        Customer.objects.create(account=user, phone=reg_form.cleaned_data.get('phone'))
                        login(request, user=user)
                        return redirect('customer_dashboard')
                    except Exception as e:
                        messages.error(request, 'The account was not created, try again latter.')
                else:
                    try:

                        driver = Driver.objects.create(account=user, phone=reg_form.cleaned_data.get('phone'))
                        for i in range(0, int(request.POST.get('vehicles'))):
                            Vehicle.objects.create(plate=get_random_string(8, ['1', '2', '3', '4', '5', '6', '7', '8', '9']),
                                                   model="DEFAULT MODEL (MOTO, TOYOTA E, BUS...)",
                                                   capacity=1,
                                                   driver=driver)
                        login(request, user=user)
                        return redirect('driver_dashboard')
                    except Exception as e:
                        print(str(e))
                        messages.error(request, 'Something went wrong, try again latter.')

                        # messages.error(request, 'Provide the required information please!')
        else:
            messages.error(request, 'Provide the required information please!')

        # return render(request, 'home_page.html', {"reg_form": reg_form, "vehicle_form": vehicle_form})
        return redirect('register')
    else:
        reg_form = RegistrationForm()
        vehicle_form = VehicleForm()
        return render(request, 'home_page.html', {"reg_form": reg_form, "vehicle_form": vehicle_form})


def login_client(request):
    if request.method == 'POST':
        username = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            customer = Customer.objects.get(account=user)
            if customer is None:
                messages.error(request, 'Not a client account.')
                return redirect('login_page')
            else:
                login(request, user)
                messages.success(request, f' Welcome {user.first_name}.')
                return redirect('customer_dashboard')
        else:
            messages.error(request, 'Credentials provided are not correct.')
            return redirect('login_page')

    else:
        return redirect('login_page')


def login_driver(request):
    if request.method == 'POST':
        username = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            driver = Driver.objects.get(account=user)
            if driver is None:
                messages.error(request, 'Not a driver account.')
                return redirect('home')
            else:
                login(request, user)
                messages.success(request, f' Welcome {user.first_name}.')
                return redirect('driver_dashboard')
        else:
            messages.error(request, 'Credentials provided are not correct.')
            return redirect('home')

    else:
        return redirect('home')