from django.shortcuts import render
from customers.models import Customer
from products.models import Product
from sales.models import Order
from purchases.models import Purchase
from django.db.models import Sum

def dashboard_home(request):
    total_products = Product.objects.count()
    total_customers = Customer.objects.count()

    total_orders = Order.objects.count()
    order_amount = Order.objects.aggregate(Sum('total_amount'))['total_amount__sum'] or 0

    total_purchases = Purchase.objects.count()
    purchase_amount = Purchase.objects.aggregate(Sum('total_amount'))['total_amount__sum'] or 0

    context = {
        'total_products': total_products,
        'total_customers': total_customers,
        'total_orders': total_orders,
        'order_amount': order_amount,
        'total_purchases': total_purchases,
        'purchase_amount': purchase_amount,
    }
    return render(request, 'dashboard/home.html', context)