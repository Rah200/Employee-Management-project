from django.shortcuts import render, HttpResponse
from .models import Employee, Role, Department
from datetime import datetime
from django.db.models import Q
from django.contrib import messages


def index(request):
    return render(request, 'index.html')


def all_emp(request):
    emps = Employee.objects.all()
    context = {
        'emps': emps
    }
    print(context)

    return render(request, 'view_all_emp.html', context)


def add_emp(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        dept = int(request.POST['dept'])
        salary = int(request.POST['salary'])
        bonus = int(request.POST['bonus'])
        role = int(request.POST['role'])
        phone = int(request.POST['phone'])
        new_emp = Employee(first_name=first_name, last_name=last_name, dept_id=dept,
                           salary=salary, bonus=bonus, role_id=role, phone=phone, hire_date=datetime.now())
        new_emp.save()
        messages.success(request, 'Details submitted!')
        return HttpResponse('Employee added Successfully')
    elif request.method == 'GET':
        return render(request, 'add_emp.html')
    else:
        return HttpResponse("Exception Occured !!")


def remove_emp(request, emp_id=0):
    if emp_id:
        try:
            emp_to_be_removed = Employee.objects.get(id=emp_id)
            emp_to_be_removed.delete()
            return HttpResponse("Employee removed Successfully")
        except:
            return HttpResponse("Please give valid employee Id")
    emps = Employee.objects.all()
    context = {
        'emps': emps
    }
    return render(request, 'remove_emp.html', context)
    messages.success(request, 'Removed!')


def update_emp(request):
    if request.method == 'POST':
        name = request.POST['name']
        dept = request.POST['dept']
        role = request.POST['role']
        phone = request.POST['phone']
        emps = Employee.objects.all()
        if name:
            emps = emps.filter(
                Q(first_name__icontains=name) | Q(last_name__icontains=name))
        if dept:
            emps = emps.filter(dept__name__icontains=dept)
        if role:
            emps = emps.filter(role__name__icontains=role)
        if phone:
            emps = emps.filter(phone__name__icontains=phone)

        context = {
            'emps': emps
        }
        messages.success(request, 'Details submitted!')
        return render(request, 'view_all_emp.html', context)

    elif request.method == 'GET':
        return render(request, 'update_emp.html')
    else:
        return HttpResponse('Error ocurred!')
