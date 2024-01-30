from django.urls import path,include
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from . import views
urlpatterns = [
   path('',views.index, name='expenses.index'),
   path('add-expense',views.add_expense,name='expenses.add'),
   path('edit-expense/<int:pk>',views.edit_expense,name='expenses.edit'),
   path('destroy-expense/<int:pk>',views.destroy_expense,name='expenses.delete'),
   
   path('search-expenses',csrf_exempt(views.search_expenses), name='search_expenses'),
]
