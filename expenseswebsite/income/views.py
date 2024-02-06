from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Source,Income
from userpreferences.models import UserPreference
from django.contrib import messages
from django.core.paginator import Paginator # this is for pagination.
import json
from django.http import JsonResponse

# Create your views here.




     
@login_required(login_url='/authentication/login')
def search_income(request):
      if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')
        income = Income.objects.filter(
            amount__istartswith=search_str, owner=request.user) | Income.objects.filter(
            date__icontains=search_str, owner=request.user) | Income.objects.filter(
            description__icontains=search_str, owner=request.user) | Income.objects.filter(
            source__icontains=search_str, owner=request.user)
        data = income.values()
        return JsonResponse(list(data), safe=False)
        
        
        
          
@login_required(login_url='/authentication/login')
def index(request):
    sources=Source.objects.all()
    income=Income.objects.filter(owner=request.user).order_by('-date')
    paginator=Paginator(income,10)
    page_Number=request.GET.get('page')
    page_obj=Paginator.get_page(paginator, page_Number)
    currency=UserPreference.objects.get(user=request.user).currency
    context={"sources":sources, 'income':income,'page_obj':page_obj,'currency':currency}
    return render(request, 'income/index.html',context)

@login_required(login_url='/authentication/login')
def add_income(request):
    sources=Source.objects.all()
    data=request.POST
    context={"sources":sources,'data':data}
    if request.method=='GET':
       
        return render(request,'income/add_income.html',context)
    
    if request.method=='POST':
        amount=request.POST['amount']
        if not amount:
            messages.error(request, 'Amount is required ')
            return render(request,'expenses/add_income.html',context)
    
        description=request.POST['description']
        date=request.POST['date']
        source=request.POST['source']
        
        
        if not description:
            messages.error(request, 'Description is required ')
            return render(request,'expenses/add_income.html',context)
        
        Income.objects.create(owner=request.user,amount=amount,date=date,source=source,description=description)
        messages.success(request, 'Income save successfully')
        return redirect('income.index')
    
    
def edit_income(request,pk):
    #income=Income.objects.get(pk=pk)  ---This could also get the job done for me.
    income=get_object_or_404(Income,pk=pk)
    sources=Source.objects.all()
    if request.method=="GET":
        context={'income':income, 'values':income,'sources':sources}
      
        return render(request, 'income/edit_income.html',context)
    
    if request.method=="POST":
            amount=request.POST['amount']
            if not amount:
                messages.error(request, 'Amount is required ')
                return render(request,'income/edit_income.html',context)
        
            description=request.POST['description']
            date=request.POST['date']
            source=request.POST['source']
            
            
            if not description:
                messages.error(request, 'Description is required ')
                return render(request,'expenses/edit_income.html',context)
            
            
            income.owner=request.user
            income.amount=amount
            income.date=date
            income.source=source
            income.description=description
            income.save()
            
            messages.success(request, 'Income updated successfully')
            return redirect('income.index')
        
        
def destroy_income(request, pk):
    income=Income.objects.get(pk=pk)
    income.delete()
    messages.error(request, 'You have successfully deleted an Income')
    return redirect('income.index')
        


