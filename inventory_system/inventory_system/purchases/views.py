import json
from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import F
from .models import Purchase, PurchaseDetail
from .forms import PurchaseForm
from products.models import Product
from employees.models import Employee

# ✅ Create form with JS
def purchase_create(request):
    form = PurchaseForm()
    products = Product.objects.all()
    return render(request, 'purchases/purchase_create.html', {
        'purchase_form': form,
        'products': products
    })

# ✅ Submit form (POST) with items_json
def purchase_submit(request):
    if request.method == 'POST':
        form = PurchaseForm(request.POST)
        items = json.loads(request.POST.get('items_json', '[]'))

        if form.is_valid() and items:
            purchase = form.save(commit=False)
            employee = Employee.objects.filter(username=request.user.username).first()
            purchase.employee = employee

            total = sum(
                Decimal(str(i['quantity'])) * Decimal(str(i['price']))
                for i in items
            )
            purchase.total_amount = total
            purchase.total_remain = total - purchase.total_paid
            purchase.save()

            for item in items:
                product = Product.objects.get(id=item['id'])
                PurchaseDetail.objects.create(
                    purchase=purchase,
                    product=product,
                    quantity=item['quantity'],
                    total_price=Decimal(str(item['quantity'])) * Decimal(str(item['price']))
                )

            return redirect('purchase_list')

        # Re-render with error
        return render(request, 'purchases/purchase_create.html', {
            'purchase_form': form,
            'products': Product.objects.all(),
            'form_error': True
        })

    return redirect('purchase_create')

# ✅ Purchase list
def purchase_list(request):
    purchases = Purchase.objects.select_related('supplier', 'employee').all()
    return render(request, 'purchases/purchase_list.html', {
        'purchases': purchases
    })

# ✅ Purchase detail
def purchase_detail(request, pk):
    purchase = get_object_or_404(Purchase.objects.select_related('supplier', 'employee'), pk=pk)
    items = purchase.items.select_related('product').all()
    return render(request, 'purchases/purchase_detail.html', {
        'purchase': purchase,
        'items': items
    })

def purchase_report(request):
    reports = Purchase.objects.select_related('employee', 'supplier').values(
        username=F('employee__username'),
        supplier_name=F('supplier__name'),
        amount=F('total_amount'),         # ✅ Renamed
        paid=F('total_paid'),             # ✅ Renamed
        remain=F('total_remain'),         # ✅ Renamed
    )
    return render(request, 'purchases/purchase_report.html', {
        'reports': reports
    })

