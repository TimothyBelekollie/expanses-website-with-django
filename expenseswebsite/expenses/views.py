from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Category,Expense
from django.contrib import messages

# Create your views here.
@login_required(login_url='/authentication/login')
def index(request):
    categories=Category.objects.all()
    context={"categories":categories}
    return render(request, 'expenses/index.html')

@login_required(login_url='/authentication/login')
def add_expense(request):
    categories=Category.objects.all()
    data=request.POST
    context={"categories":categories,'data':data}
    if request.method=='GET':
       
        return render(request,'expenses/add_expense.html',context)
    
    if request.method=='POST':
        amount=request.POST['amount']
        if not amount:
            messages.error(request, 'Amount is required ')
            return render(request,'expenses/add_expense.html',context)
    
        description=request.POST['description']
        date=request.POST['date']
        category=request.POST['category']
        
        if not description:
            messages.error(request, 'Description is required ')
            return render(request,'expenses/add_expense.html',context)
        
        Expense.objects.create(owner=request.user,amount=amount,date=date,category=category,description=description)
        messages.success(request, 'Expense save successfully')
        return redirect('expenses.index')
        
        
    
        
        
        
 
        
        
       
        

    