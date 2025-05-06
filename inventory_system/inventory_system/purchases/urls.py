from django.urls import path
from . import views

urlpatterns = [
    path('purchases/', views.purchase_list, name='purchase_list'),           # 🧾 View all purchases
    path('purchases/add/', views.purchase_create, name='purchase_create'),   # ➕ Create form page
    path('purchases/submit/', views.purchase_submit, name='purchase_submit'),# ✅ Handle form submission
    path('purchases/<int:pk>/', views.purchase_detail, name='purchase_detail'), # 🔍 View single purchase
    path('purchases/report/', views.purchase_report, name='purchase_report'),  # 📊 Summary report
]