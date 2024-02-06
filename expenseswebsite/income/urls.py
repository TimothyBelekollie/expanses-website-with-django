from . import views
from django.urls import path,include
from django.views.decorators.csrf import csrf_exempt, csrf_protect


urlpatterns = [
    path('',views.index, name='income.index'),
    path('add-income',views.add_income,name='income.add'),
    path('edit-income/<int:pk>',views.edit_income,name='income.edit'),
    path('destroy-income/<int:pk>',views.destroy_income,name='income.delete'),

    path('search-income',csrf_exempt(views.search_income), name='search_income'),
]
