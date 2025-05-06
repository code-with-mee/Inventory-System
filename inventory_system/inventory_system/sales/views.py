import json
from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import F
from .models import Order, OrderDetail, Product
from .forms import OrderForm
from employees.models import Employee


# ✅ 1. Render the Create Order Form (uses JS)
def order_create(request):
    form = OrderForm()
    products = Product.objects.all()
    return render(request, 'sales/order_create.html', {
        'order_form': form,
        'products': products
    })


# ✅ 2. Handle POST Submission from JS with Decimal Fix
def order_submit(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        items_json = request.POST.get('items_json')

        try:
            items = json.loads(items_json)
        except json.JSONDecodeError:
            items = []

        if form.is_valid() and items:
            order = form.save(commit=False)

            # 🔐 Link Employee
            employee = Employee.objects.filter(username=request.user.username).first()
            order.employee = employee

            # 💰 Decimal-safe total calculation
            total = sum(
                Decimal(str(i['quantity'])) * Decimal(str(i['price']))
                for i in items
            )
            order.total_amount = total
            order.total_remain = total - order.total_paid
            order.save()

            # 💾 Save each item
            for item in items:
                product = Product.objects.get(id=item['id'])
                OrderDetail.objects.create(
                    order=order,
                    product=product,
                    quantity=int(item['quantity']),
                    total_price=Decimal(str(item['quantity'])) * Decimal(str(item['price']))
                )

            return redirect('order_list')

        # Re-render if error
        return render(request, 'sales/order_create.html', {
            'order_form': form,
            'products': Product.objects.all(),
            'form_error': True
        })

    return redirect('order_create')


# ✅ 3. List All Orders
def order_list(request):
    orders = Order.objects.select_related('customer', 'employee').all()
    return render(request, 'sales/order_list.html', {'orders': orders})


# ✅ 4. View Order Details
def order_detail(request, pk):
    order = get_object_or_404(Order.objects.select_related('customer', 'employee'), pk=pk)
    items = order.items.select_related('product').all()
    return render(request, 'sales/order_detail.html', {'order': order, 'items': items})


# ✅ 5. Order Summary Report
def order_report(request):
    reports = Order.objects.select_related('employee', 'customer').values(
        username=F('employee__username'),
        customer_name=F('customer__name'),
        total_amount=F('total_amount'),
        total_paid=F('total_paid'),
        total_remain=F('total_remain'),
    )
    return render(request, 'sales/order_report.html', {'reports': reports})
