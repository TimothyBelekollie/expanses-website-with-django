from django.shortcuts import render,redirect
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from validate_email import validate_email # this was install using pip install validate-messages
from django.contrib import messages
from django.core.mail import EmailMessage

from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
# from .utils import account_activation_token
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib import auth



from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.template.loader import render_to_string



#calling a self made class by Dev. Timothy Belekollie
from .utils import tokenGenerator

# Create your views here.

class UsernameValidationView(View):
    def post(self, request):
        data=json.loads(request.body)
        username=data['username']
        if not str(username).isalnum():
            return JsonResponse({'username_error':'Username should only contain alphanumeric characters'},status=400)
        
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error':'Oh sorry, username is in use, choose another one'},status=409)
        
        return JsonResponse({'username_valid':True})
    
class EmailValidationView(View):
    def post(self, request):
        data=json.loads(request.body)
        email=data['email']
        if not validate_email(email):
            return JsonResponse({'email_error':'Email is invalid'},status=400)
        
        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error':'Oh sorry, email is in use, choose another one'},status=409)
        
        return JsonResponse({'email_valid':True})
        
    
  
class RegistrationView(View):
    def get(self, request):
        return render(request,'authentication/register.html')
    
    def post(self, request):
       #Get user data
       username=request.POST['username']
       email=request.POST['email']
       password=request.POST['password']
       context={'fieldValues':request.POST}
       if not User.objects.filter(username=username).exists():
           if not User.objects.filter(email=email).exists():
               if len(password)<6:
                   messages.error(request, 'Your password is too short')
                   return render(request,'authentication/register.html', context)
               else:
                user = User.objects.create_user(username=username, email=email)
                user.set_password(password)
                user.is_active=False
                user.save()
                
                
                #path_to_the_view
                #- getting the domain we are on
                # -relative url to verification
                # - encode ui 
                # - get token
                uidb64=urlsafe_base64_encode(force_bytes(user.pk))
                
                domain=get_current_site(request).domain
                link=reverse('activate',kwargs={'uidb64':uidb64,'token':tokenGenerator.make_token(user)})
                email_subject="Activate Your Account"
                activate_url='http://'+domain+link
                email_body='Hi Dear '+user.username +', Please use this link to verify your account\n'+ activate_url
                email = EmailMessage(
                email_subject,
                email_body,
                "no_reply@gmail.com",
                [email,],
                
                
                )
                email.send(fail_silently=False)
                messages.success(request, 'Your account has been created successfully')
                return render(request, 'authentication/register.html')
           else:
                messages.error(request, 'Email already exist, choose another one')
                return render(request, 'authentication/register.html')
        
       else:
          messages.error(request, 'Username already exist, choose another one')
          return render(request, 'authentication/register.html')
                
                
       
       #Validate user data
       #Create User Account
       return render(request,'authentication/register.html')
   
   
class VerificationView(View):
    def get(self,request,uidb64,token):
        try:
            id=force_str(urlsafe_base64_decode(uidb64))
            user=User.objects.get(pk=id)
            if not tokenGenerator.check_token(user, token):
                return redirect('login'+'?message'+'User already activated')
            if user.is_active:
                return redirect('login')
            user.is_active=True
            user.save()
            messages.success(request, 'Account activated successfully')
            return redirect('login')
        except Exception as ex:
            pass
        
        return redirect('login')
        

class LoginView(View):
    def get(self,request):
        return render(request,'authentication/login.html')  
    
    def post(self,request):
        username=request.POST['username']
        password=request.POST['password']   
        if username and password:
            user=auth.authenticate(username=username,password=password)
            if user:
                if user.is_active:
                    auth.login(request,user)
                    messages.success(request, 'Welcome '+user.username+', You are now logged in')
                    return redirect('expenses.index')
                    
                messages.error(request,'Your account is not activated, please check your email that you register with or trying using an official email becuase you will get a notification in my mail')
                return render(request, 'authentication/login.html')
            messages.error(request,'Invalid Crendentials, try again')
            return render(request, 'authentication/login.html')
        
        messages.error(request,'Please fill all fields')
        return render(request, 'authentication/login.html')
        
        
            

class LogoutView(View):
    def post(self, request):
        auth.logout(request)
        messages.success(request, 'You have logout Successfully')
        return redirect('login')
    
    
    
# class RequestPasswordResetEmail(View):
#     def get(self, request):
#         return render(request, 'authentication/reset-password.html')
    
#     def post(self, request):
#         email=request.POST['email']
#         value=request.POST
#         if not validate_email(email):
#             messages.error(request, 'Invalid Email, Please try gain')
#             context={'value':value}
#             return render(request, 'Authentication/reset-password.html',context) 
        
        
       
            
#         domain=get_current_site(request).domain
#         user=User.objects.get(email=email)
#         uidb64=urlsafe_base64_encode(force_bytes(user[0].pk))
#         if user.exists():
#             email_Contents={
#                 'user': user[0],
#                 'domain': domain,
#                 'uidb64': urlsafe_base64_encode(force_bytes(user[0].pk)),
#                 'token':PasswordResetTokenGenerator().make_token(user[0]),
                
#             }
        
            
#             link=reverse('reset-user-password',kwargs={'uidb64':email_Contents['uidb64'],'token':email_Contents['token']})
#             email_subject="Password Reset Instructions"
#             passwordReset_url='http://'+domain+link
#             email_body='Hi Dear '+user.username +', Please use this link to reset your password \n'+ passwordReset_url
            
#             email = EmailMessage(
#             email_subject,
#             email_body,
#             "no_reply@gmail.com",
#             [email,],
            
            
#             )
#             email.send(fail_silently=False)
            
#         messages.success(request, 'We have send you an email to reset your password')
        
#         messages.success(request, 'Your account has been created successfully')
        
#         return render(request, 'authentication/reset-password.html')
    
class RequestPasswordResetEmail(View):
    def get(self, request):
        return render(request, 'authentication/reset-password.html')
    
    def post(self, request):
        email = request.POST.get('email')  # Using get() method to avoid raising KeyError
        value = request.POST
        
        if not validate_email(email):
            messages.error(request, 'Invalid Email, Please try again')
            context = {'value': value}
            return render(request, 'authentication/reset-password.html', context) 
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, 'User does not exist with this email')
            return render(request, 'authentication/reset-password.html', {'value': value})
        
        domain = get_current_site(request).domain
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        token = PasswordResetTokenGenerator().make_token(user)
        
        email_Contents = {
            'user': user,
            'domain': domain,
            'uidb64': uidb64,
            'token': token,
        }
        
       # link = reverse('reset-user-password', kwargs={'uidb64': uidb64.decode(), 'token': token})
        link=reverse('reset-user-password',kwargs={'uidb64':email_Contents['uidb64'],'token':email_Contents['token']})
        password_reset_url = 'http://' + domain + link
        email_subject = "Password Reset Instructions"
        email_body = f"Hi {user.username}, Please use this link to reset your password:\n{password_reset_url}"
        
        email = EmailMessage(
            email_subject,
            email_body,
            "no_reply@gmail.com",
            [email],
        )
        email.send(fail_silently=False)
        
        messages.success(request, 'We have sent you an email to reset your password')
        return render(request, 'authentication/reset-password.html')
    
    
    
class CompletePasswordReset(View):
        def get(self, request, uidb64,token):
            
            context={'uidb64':uidb64,'token':token}
            
            try:
                user_id=force_str(urlsafe_base64_decode(uidb64))
                user=User.objects.get(pk=user_id)
                
                if not PasswordResetTokenGenerator().check_token(user, token):
                    
                
                    messages.info(request, 'This link is invalid, please request a new one')
                    return render(request, 'authentication/set-newpassword.html',context)
            
            except Exception as identifier:
                pass
            return render(request, 'authentication/set-newpassword.html',context)
        
        def post(self, request, uidb64,token):
            context={'uidb64':uidb64,'token':token}
            
            password=request.POST['password']
            password2=request.POST['password2']
            if password != password2:
                messages.error(request,'Your Passwords do not match')
                return render(request, 'authentication/set-newpassword.html',context)
            
            if len(password)<6:
                messages.error(request,'Password too short')
                return render(request, 'authentication/set-newpassword.html',context)
            try:
                user_id=force_str(urlsafe_base64_decode(uidb64))
                user=User.objects.get(pk=user_id)
                
                user.set_password(password)
                user.save()
                messages.success(request, 'Password reset successfully. You can login now')
                return redirect('login')
            
            except Exception as identifier:
                 messages.info(request, 'Something went wrong, try again')
                 return render(request, 'authentication/set-newpassword.html',context)
          
            
                
                
                
            # return render(request, 'authentication/set-newpassword.html',context)
        