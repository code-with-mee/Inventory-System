from django.shortcuts import render, redirect
from .models import Employee
from .forms import EmployeeForm

def employee_list(request):
    employees = Employee.objects.all()
    return render(request, 'employee/employee_list.html', {'employees': employees})

def employee_add(request):
    form = EmployeeForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('employee_list')
    return render(request, 'employee/employee_form.html', {'form': form})

def employee_edit(request, pk):
    employee = Employee.objects.filter(pk=pk).first()
    form = EmployeeForm(request.POST or None, instance=employee)
    if form.is_valid():
        form.save()
        return redirect('employee_list')
    return render(request, 'employee/employee_form.html', {'form': form})

def employee_delete(request, pk):
    employee = Employee.objects.filter(pk=pk).first()
    if request.method == 'POST':
        employee.delete()
        return redirect('employee_list')
    return render(request, 'employee/employee_delete.html', {'employee': employee})