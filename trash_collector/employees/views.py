from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.apps import apps
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from datetime import date
from .models import Employee
from django import forms



@login_required
def index(request):
    Customer = apps.get_model('customers.Customer')
    logged_in_user = request.user
    try:
        logged_in_employee = Employee.objects.get(user=logged_in_user)
        weekday_list = [('monday','Monday'), 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        selected_day = forms.CharField(label='View Day', widget=forms.Select(choices=weekday_list))
        today = date.today()
        weekday = today.strftime('%A')
        customers_in_my_zipcode = Customer.objects.filter(zip_code = logged_in_employee.zip_code)
        pick_up_day = customers_in_my_zipcode.filter(weekly_pickup = weekday) | customers_in_my_zipcode.filter(one_time_pickup = today)
        suspended_or_no = pick_up_day.exclude(suspend_start__lte = today, suspend_end__gte = today)
        trash_picked_up = suspended_or_no.exclude(date_of_last_pickup = today)
        #data_visualization = [item for item in suspended_or_no]
        context = {
            'logged_in_employee': logged_in_employee,
            'today': today,
            'trash_picked_up': trash_picked_up,
            'selected_day': selected_day

        }
        return render(request, 'employees/index.html', context)
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse('employees:create'))


# confirms if the garbage from the customer has been picked up
# when the confirm pickup button is clicked it deleted the cusomer and adds a balance
# to the cusomers account
@login_required
def confirm_pickup(request, item_id):
    Customer = apps.get_model('customers.Customer')
    today = date.today()
    pickup_date = Customer.objects.get(pk=item_id)
    pickup_date.date_of_last_pickup = today
    pickup_date.balance += 20
    pickup_date.save()
    return HttpResponseRedirect(reverse('employees:index'))

# searched the customers weekly pickup day and lists them by day and in order of zipcode
@login_required
def search_daily_pickups(request, weekday):
    weekday = weekday
    logged_in_user = request.user
    logged_in_employee = Employee.objects.get(user=logged_in_user)
    Customer = apps.get_model('customers.Customer')
    pickup_day = Customer.objects.filter(weekly_pickup = weekday).order_by('zip_code')
    #data_visualization = [item for item in pickup_day]
    context = {
        'logged_in_employee': logged_in_employee,
        'pickup_day': pickup_day,
        'day_of_week': weekday
    }
    return render(request, 'employees/search_daily_pickups.html', context)

@login_required
def create(request):
    logged_in_user = request.user
    if request.method == "POST":
        name_from_form = request.POST.get('name')
        address_from_form = request.POST.get('address')
        zip_from_form = request.POST.get('zip_code')
        new_employee = Employee(name=name_from_form, user=logged_in_user, address=address_from_form, zip_code=zip_from_form)
        new_employee.save()
        return HttpResponseRedirect(reverse('employees:index'))
    else:
        return render(request, 'employees/create.html')

# gives the employee the ability to edit their profile info
@login_required
def edit_profile(request):
    logged_in_user = request.user
    logged_in_employee = Employee.objects.get(user=logged_in_user)
    if request.method == "POST":
        name_from_form = request.POST.get('name')
        address_from_form = request.POST.get('address')
        zip_from_form = request.POST.get('zip_code')
        logged_in_employee.name = name_from_form
        logged_in_employee.address = address_from_form
        logged_in_employee.zip_code = zip_from_form
        logged_in_employee.save()
        return HttpResponseRedirect(reverse('employees:index'))
    else:
        context = {
            'logged_in_employee': logged_in_employee
        }
        return render(request, 'employees/edit_profile.html', context)