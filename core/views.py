from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils import timezone
import random
from .forms import RegistrationForm, VehicleForm
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Customer, Vehicle, Driver, Delivery, DriverWaitingList
from django.utils.crypto import get_random_string
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from .utils import link_callback
from django.conf import settings
from django.utils.crypto import get_random_string
# Create your views here.


def alert_users(deliveries,  request):
    for delivery in deliveries:
        remaining_time = ((delivery.departure_date_time - timezone.now()).total_seconds() / (60 * 60 * 24))
        print(remaining_time)
        if remaining_time <= 1:
            messages.warning(request, f'Umuzigo N0: {delivery.number} wenda kurnza cg warengeje italiki!!')


def profile_page(request):
    user = request.user
    drivers = Driver.objects.filter(account=user)
    customers = Customer.objects.filter(account=user)
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        profile = request.FILES.get('profile')

        user.first_name = first_name if first_name is not None else user.first_name
        user.last_name = last_name if last_name is not None else user.last_name
        user.save()
        if customers.exists():
            customer = customers.first()
            customer.phone = phone if phone is not None else customer.phone
            customer.profile_picture = profile if profile is not None else customer.profile_picture
            customer.save()
        elif drivers.exists():
            driver = drivers.first()
            driver.phone = phone if phone is not None else driver.phone
            driver.has_profile = True if profile is not None else False
            driver.profile_picture = profile if profile is not None else driver.profile_picture
            driver.save()
        messages.success(request, 'Profile edited')
        return redirect('profile_page')

    else:
        if customers.exists():
            return render(request, 'customer-profile.html', {"customer": customers.first()})
        elif drivers.exists():
            driver = drivers.first()
            vehicles = Vehicle.objects.filter(driver=driver)
            return render(request, 'driver-profile.html', {"driver": driver, "vehicles": vehicles})


def home_page(request):
    drivers = [element for element in Driver.objects.all()]
    random_drivers = random.sample(drivers, min(len(drivers), 3))
    return render(request, 'home-page.html', {"drivers": random_drivers})


def login_page(request):
    return render(request, 'login-page.html')


def customer_auth(request):
    return render(request, 'customer-auth.html')


def driver_auth(request):
    return render(request, 'driver-auth.html')


def register_page(request):
    return render(request, 'register_page.html')


@login_required
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')


@login_required
def customer_dashboard(request):
    user = request.user
    clients = Customer.objects.filter(account=user)
    print(clients.exists())
    if clients.exists() is False:

        messages.error(request, 'Not a client account')
        return redirect('home')
    else:
        client = clients.first()
        deliveries = Delivery.objects.filter(owner=client).order_by('-departure_date_time')
        print(deliveries)
        return render(request, 'customer-dashboard.html', {"deliveries": deliveries})


@login_required()
def accept_request(request, delivery_id, driver_id):
    user = request.user
    client = Customer.objects.get(account=user)
    if client is None:
        messages.error(request, 'Not a client account')
        return redirect('home')
    else:
        delivery = Delivery.objects.get(id=delivery_id)
        driver = Driver.objects.get(id=driver_id)
        DriverWaitingList.objects.filter(delivery=delivery).delete()
        delivery.driver = driver
        delivery.status = 'I'
        delivery.save()
        return redirect('delivery-edit', pk=delivery_id)


@login_required()
def driver_profile(request, reason, driver_id, delivery_id):
    user = request.user
    driver = Driver.objects.get(pk=driver_id)
    if Customer.objects.filter(account=user).exists():
        delivery = Delivery.objects.get(pk=delivery_id)
        if reason == 'ASSIGN':
            alert_users([delivery], request)
            messages.warning(request, "Waba koko wifuza gutanga ikiraka? Ohereza iyi form. Niba utabyifuza subira inyuma.")
            return render(request, 'driver_profile.html', {"reason": "ASSIGN", "driver": driver, "delivery": delivery})
        else:
            return render(request, 'driver_profile.html', {"reason": "VIEW", "driver": driver})
    elif Driver.objects.filter(account=user).exists():
        if reason == 'Edit':
            return render(request, 'driver_profile.html', {"reason": "EDIT", "driver": driver})
        else:
            return render(request, 'driver_profile.html', {"reason": "VIEW", "driver": driver})


@login_required()
def delivery_edit(request, pk):
    user = request.user
    client = Customer.objects.get(account=user)
    if client is None:
        messages.error(request, 'Not a client account')
        return redirect('home')
    else:
        if request.method == "GET":
            delivery = Delivery.objects.get(pk=pk)
            driver_list = DriverWaitingList.objects.filter(delivery=delivery)
            list_of_drivers = [list_row.driver for list_row in driver_list]
            return render(request, 'delivery-edit.html', {"delivery": delivery, "list_of_drivers": list_of_drivers})
        else:
            delivery = Delivery.objects.get(pk=pk)
            delivery.departure_date_time = request.POST.get('departure_date_time')
            delivery.arrival_date_time = request.POST.get('arrival_date_time')
            delivery.kilograms = request.POST.get('kilograms')
            delivery.destination = request.POST.get('destination')
            delivery.origin = request.POST.get('origin')
            delivery.price = request.POST.get('price')
            if request.POST.get('status1') :
                delivery.status = 'D'
            if request.POST.get('status2'):
                delivery.status = 'W'

            delivery.save()

            return redirect('customer_dashboard')


@login_required
def record_new_carriage(request):
    user = request.user
    client = Customer.objects.get(account=user)
    if client is None:
        messages.error(request, 'Not a client account')
        return redirect('home')
    else:
        if request.method == 'GET':
            # deliveries = Delivery.objects.filter(owner=client)
            return render(request, 'new-carriage.html')
        else:

            departure_date_time = request.POST.get('departure_date_time')
            arrival_date_time = request.POST.get('arrival_date_time')
            kilograms = request.POST.get('kilograms')
            destination = request.POST.get('destination')
            origin = request.POST.get('origin')
            price = request.POST.get('price')

            Delivery.objects.create(owner=client,
                                    departure_date_time=departure_date_time,
                                    arrival_date_time=arrival_date_time,
                                    kilograms=kilograms,
                                    destination=destination,
                                    origin=origin,
                                    price=price)
            return redirect('customer_dashboard')


@login_required()
def ask_to_deliver(request, delivery_id):
    if request.method == 'POST':
        user = request.user
        driver = Driver.objects.filter(account=user).first()
        if driver is None:
            messages.error(request, 'Not a driver account')
            return redirect('home')
        else:

            delivery = Delivery.objects.get(id=delivery_id)
            in_the_list = DriverWaitingList.objects.filter(delivery=delivery, driver=driver).exists()
            if in_the_list:
                messages.info(request, 'Musanze muri kuri list!')
                return redirect('driver_dashboard')
            else:
                DriverWaitingList.objects.create(driver=driver, delivery=delivery)
                messages.success(request, 'Ibyo wasbye bya tambukijwe, mutegereze igisubizo.')
                return redirect('driver_dashboard')


@login_required
def driver_dashboard(request):
    user = request.user
    driver = Driver.objects.filter(account=user).first()
    if driver is None:
        messages.error(request, 'Not a driver account')
        return redirect('home')
    else:

        deliveries = Delivery.objects.filter(status='W').order_by('-departure_date_time')
        # alert_users(deliveries, request)
        return render(request, 'driver-dashboard.html', {"deliveries": deliveries})


@login_required
def print_bill(request, delivery_id):
    user = request.user
    driver = Driver.objects.get(account=user)
    if driver is None:
        messages.error(request, 'Not a driver account')
        return redirect('home')
    else:
        delivery = Delivery.objects.get(pk=delivery_id)
        template_path = settings.BASE_DIR/'core/templates/bill.html'
        context = {'delivery': delivery, 'test': 'Test here!'}
        # Create a Django response object, and specify content_type a6s pdf
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="bill.pdf"'
        # find the template and render it.
        template = get_template(template_path)
        html = template.render(context)

        # create a pdf
        pisa_status = pisa.CreatePDF(
            html, dest=response, link_callback=link_callback)
        # if error then show some funy view
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')
        return response


@login_required
def mission_details(request, delivery_id):
    user = request.user
    driver = Driver.objects.get(account=user)
    if driver is None:
        messages.error(request, 'Not a driver account')
        return redirect('home')
    else:
        delivery = Delivery.objects.get(id=delivery_id)
        return render(request, 'assigned-mission.html', {"delivery": delivery})


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
        # deliveries = Delivery.objects.filter(driver=driver)
        deliveries = driver.get_assigned_deliveries()
        alert_users(deliveries, request)
        return render(request, 'driver-missions.html', {"deliveries": deliveries})


def delivery_details(request, pk):
    user = request.user
    driver = Driver.objects.get(account=user)
    if driver is None:
        messages.error(request, 'Not a driver account. \n Login first!')
        return redirect('home')
    else:
        delivery = Delivery.objects.get(pk=pk)
        is_on_the_list = DriverWaitingList.objects.filter(driver=driver, delivery=delivery).exists()
        return render(request, 'delivery-details.html', {"delivery": delivery, "is_on_the_list": is_on_the_list})


def register_account(request):

    if request.method == 'POST':
        reg_form = RegistrationForm(request.POST)

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
        return render(request, 'home-page.html', {"reg_form": reg_form, "vehicle_form": vehicle_form})


def login_client(request):
    if request.method == 'POST':
        username = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            customers = Customer.objects.filter(account=user)
            if customers.exists() is False:
                messages.error(request, 'Not a client account.')
                return redirect('login_page')
            else:
                login(request, user)
                request.session["is_who"] = "CUSTOMER"
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
            drivers = Driver.objects.filter(account=user)
            if drivers.exists() is False:
                messages.error(request, 'Not a driver account.')
                return redirect('login_page')
            else:
                login(request, user)
                request.session["is_who"] = "DRIVER"
                messages.success(request, f' Welcome {user.first_name}.')
                return redirect('driver_dashboard')
        else:
            messages.error(request, 'Credentials provided are not correct.')
            return redirect('login_page')

    else:
        return redirect('home')


@login_required()
def add_vehicle_or_delete(request):
    user = request.user
    driver = Driver.objects.filter(account=user).first()
    if driver is None:
        messages.error(request, 'Not a driver account')
        return redirect('home')
    else:

        if request.method == 'POST':
            plate = request.POST.get('plate')
            capacity = request.POST.get('capacity')
            model = request.POST.get('model')
            Vehicle.objects.create(driver=driver, plate=plate, capacity=capacity, model=model)
            messages.success(request, 'Ikinyabiziga cyandukuwe.')
            return redirect('profile_page')
        else:
            plate = request.GET.get('plate_delete')
            capacity = request.GET.get('capacity_delete')
            model = request.GET.get('model_delete')
            vehicles = Vehicle.objects.filter(driver=driver, plate=plate, model=model, capacity=capacity)
            print(plate, capacity, model)
            vehicles.delete()
            messages.success(request, 'Ikinyabiziga cya sibwe kurubuga.')
            return redirect('profile_page')


