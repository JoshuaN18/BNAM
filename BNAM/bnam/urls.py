from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('authentication.urls')),
    path("api/users/", include("User.urls")),
    path('api/budgets/', include('Budget.urls')),
    path('api/accounts/', include('Account.urls')),
    path('api/payees/', include('Payee.urls')),
    path('api/categorygroups/', include('CategoryGroup.urls')),
    path('api/categories/', include('Category.urls')),
    path('api/monthlycategories/', include('MonthlyCategory.urls')),
    path('api/transactions/', include('Transaction.urls')),
]
