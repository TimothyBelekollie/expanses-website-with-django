from django.urls import path,include
from . import views
urlpatterns = [
   path('',views.index, name='expenses.index'),
   path('add-expense',views.add_expense,name='expenses.add'),
]
