from django.http import JsonResponse
from rest_framework.views import APIView
from redisManager import RedisManager
from users.serializers import UserSerializer

from utils.Frontend import FRONTEND_DOMAIN
from utils.UserSlugManager import UserSlugManager
from .models import User
from django.contrib.auth.hashers import make_password, check_password
from utils.httpResponse import HttpResponse
from utils.JWTTokenManager import UserTokenManager
from utils.SendMail import SendEmail
from utils.RandomStrings import GenerateRandomString
from threading import Thread
from django.core.validators import EmailValidator
from .serializers import CompanySerializer
from knox.models import AuthToken





class TestApi(APIView):
    def get(self, request):
        CACHE_KEY ="CACHE_KEY"
        cached_data = RedisManager().get(CACHE_KEY)
        if not cached_data:
            users = list(User.object.values())
            RedisManager().set(CACHE_KEY, data)
            return JsonResponse(users, safe=False)
        else:
            return JsonResponse(cached_data, safe=False)



class RegisterCompany(APIView):
    
    def post(self, request):
        company_name = request.data.get("company_name")
        company_address = request.data.get("company_address")
        company_current_plan = request.data.get("company_current_plan")
        company_description = request.data.get("company_description")
        company_area_of_interest = request.data.get("company_area_of_interest")
        company_mobile_contact = request.data.get("company_mobile_contact")
        company_email_address = request.data.get("company_email_address")
        company_password = request.data.get("company_password")

        
        if not company_name:
            return HttpResponse.error("Please enter the company name")
        if not company_address:
            return HttpResponse.error("Please enter the company address")
        if not company_current_plan:
            return HttpResponse.error("Please enter the company current plan")
        
        if not company_area_of_interest:
            return HttpResponse.error("Please enter the company area of interest")
        if not company_mobile_contact:
            return HttpResponse.error("Please enter the company mobile contact")
        if not company_email_address:
            return HttpResponse.error("Please enter company email address")
        if not company_password:
            return HttpResponse.error("Please enter company password")

        try:
            EmailValidator()(company_email_address)
        except Exception as e:
            return HttpResponse.error("Sorry, your email is not valid")

        

        try:
            u = User.object.get(email=company_email_address)
            return HttpResponse.error("Email already registered")
        except User.DoesNotExist as e:
            pass

            
        slug = UserSlugManager().generateUserSlug()

        dataUser = {"email":company_email_address, "full_name":company_name,"slug":slug, "password": make_password(company_password)}




        

        serializerUser = UserSerializer(data=dataUser)
        
        

        if serializerUser.is_valid():
            u = serializerUser.save()

            # START REGISTERING COMPANY
            dataCompany = { "company_name":company_name, "company_address":company_address,"company_current_plan":company_current_plan,"company_description":company_description, "company_area_of_interest":company_area_of_interest,"company_mobile_contact":company_mobile_contact,"company_email_address":company_email_address, "company_password":company_password, "registered_by":u.id}

            serializerCompany = CompanySerializer(data = dataCompany )
            if serializerCompany.is_valid():
                c= serializerCompany.save()
                sendUserAcctEmail = Thread(target=sendUserAccountActivationEmail, args=(request,u))
                sendUserAcctEmail.start()
                data = {"company": CompanySerializer(c).data}
                return HttpResponse.success("Company created successfully, please check your email to active company  account", data)
            else:
                User.object.get(id=u.id).delete()
                if not serializerCompany.is_valid():
                    print(serializerCompany.errors)
                return JsonResponse({"companyError": serializerCompany.error_messages}, status=400)
            
            
        else:
            if not serializerUser.is_valid():
                print(serializerUser.errors)
            return JsonResponse({ "userError": serializerUser.error_messages}, status=400)
        



class LoginCompany(APIView):
    def post(self, request):
        company_email = request.data.get("company_email_address")
        company_password = request.data.get("company_password")
        if not company_email:
            return HttpResponse.error("Please enter  company email")
        if not company_password:
            return HttpResponse.error("Please enter  company password")

        try:
            u = User.object.get(email=company_email)
            if u.email == company_email:
                if check_password(company_password, u.password):
                    token = AuthToken.objects.create(u)
                    data ={
                        "user": UserSerializer(u).data,
                        "token":token[1],
                    }
                    if u.is_active:
                        try:
                            company = u.company
                        except Exception as e:
                            return HttpResponse.error("A company is not registered here")
                        if company.company_is_active:
                            return HttpResponse.success("User LoggedIn Successfully", data)
                        else:
                            return HttpResponse.error("Company has not yet paid for a plan  account not activated")



                    else:
                        return HttpResponse.error("Company Email not yet activated")
                else:
                    return HttpResponse.error("Please check  company password")

            else:
                return HttpResponse.error("Company Email is not correct, try again")


        except User.DoesNotExist as e:
            return HttpResponse.error("Company with this Email does not exist does not exist.")


def sendUserAccountActivationEmail(request, user):
    tokenGen = UserTokenManager()
    tokenGenerated = tokenGen.generateToken(user)
    activationLink = FRONTEND_DOMAIN+"users/user-email-activation/"+GenerateRandomString.randomStringGenerator(40)+"/"+tokenGenerated+"/"+GenerateRandomString.randomStringGenerator(20)
    
    email = SendEmail('emails/UserAccountActivation.html',"User Account Activation",{"activationLink":activationLink, "company_account": True }, user.email)
    email.send()
