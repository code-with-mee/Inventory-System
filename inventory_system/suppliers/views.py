from django.shortcuts import render, redirect, get_object_or_404
from .models import Supplier
from .forms import SupplierForm

# CUSTOMER VIEWS
def supplier_list(request):
    suppliers = Supplier.objects.all()
    return render(request, 'supplier/supplier_list.html', {'suppliers': suppliers})

def supplier_add(request):
    form = SupplierForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("supplier_list")
    return render(request,"supplier/supplier_add.html",{"form":form})

def supplier_edit(request,pk):
    supplier = Supplier.objects.filter(pk=pk).first()
    form = SupplierForm(request.POST or None,instance = supplier)
    if form.is_valid():
        form.save()
        return redirect("supplier_list")
    return render(request,"supplier/supplier_edit.html",{"form":form})

def supplier_delete(request,pk):
    supplier = Supplier.objects.filter(pk=pk).first()
    if request.method == "POST":
        supplier.delete()
        return redirect("supplier_list")
    return render(request,"supplier/supplier_delete.html",{"supplier":supplier})