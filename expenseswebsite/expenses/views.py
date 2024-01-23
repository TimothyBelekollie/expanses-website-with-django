from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Category,Expense
from django.contrib import messages

# Create your views here.
@login_required(login_url='/authentication/login')
def index(request):
    categories=Category.objects.all()
    expenses=Expense.objects.filter(owner=request.user).order_by('-date')
    context={"categories":categories, 'expenses':expenses}
    return render(request, 'expenses/index.html',context)

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
    
    
def edit_expense(request,pk):
    #expense=Expense.objects.get(pk=pk)  ---This could also get the job done for me.
    expense=get_object_or_404(Expense,pk=pk)
    categories=Category.objects.all()
    if request.method=="GET":
        context={'expense':expense, 'values':expense,'categories':categories}
      
        return render(request, 'expenses/edit_expense.html',context)
    
    if request.method=="POST":
            amount=request.POST['amount']
            if not amount:
                messages.error(request, 'Amount is required ')
                return render(request,'expenses/edit_expense.html',context)
        
            description=request.POST['description']
            date=request.POST['date']
            category=request.POST['category']
            
            
            if not description:
                messages.error(request, 'Description is required ')
                return render(request,'expenses/edit_expense.html',context)
            
            
            expense.owner=request.user
            expense.amount=amount
            expense.date=date
            expense.category=category
            expense.description=description
            expense.save()
            
            messages.success(request, 'Expense updated successfully')
            return redirect('expenses.index')
        
    
        
        
        
 
        
        
       
        

    