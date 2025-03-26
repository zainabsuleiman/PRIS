from django.shortcuts import render ,redirect
from django.http import JsonResponse
from django.http import Http404
from rest_framework.decorators import api_view,authentication_classes,permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import authenticate , login
from rest_framework import status
from .serializers import *
from .models import *
from django.contrib.auth.hashers import make_password, check_password
import json
import requests
from  company.models import *
from  company.serializers import *
import math
import random
from rest_framework import generics, permissions
from rest_framework.response import Response
from .serializers import UserSerializer
from django.contrib.auth import login
from rest_framework.permissions import IsAuthenticated,AllowAny,IsAdminUser
from rest_framework import permissions
from oauth2_provider.contrib.rest_framework.authentication import OAuth2Authentication
from Accounts.utils.flutter_wave import CreatePayment
from ProductReg import settings
import environ
import os
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
import datetime
from io import BytesIO
from django.template.loader import get_template
from xhtml2pdf import pisa
import qrcode
import qrcode.image.svg
from qrcode import *
from django.contrib.auth import get_user_model
User = get_user_model()
# Initialise environment variables
env = environ.Env()
environ.Env.read_env()



#callback
@require_http_methods(['GET', 'POST'])
def payment_response(request):
    status=request.GET.get('status', None)
    tx_ref=request.GET.get('tx_ref', None)
    print(status)
    print(tx_ref)
    return HttpResponse('Finished')
#role creation
@api_view(['POST'])
@authentication_classes([OAuth2Authentication])
@permission_classes([IsAdminUser])
def Rolecreation(request):
    serializer = RoleSerializer(data=request.data)

    if serializer.is_valid():
       serializer.save()
       return Response(serializer.data,status=status.HTTP_201_CREATED)
    else:
        return Response({'msg':serializer.errors},status=status.HTTP_400_BAD_REQUEST )
#role list
@api_view(['GET'])
@authentication_classes([OAuth2Authentication])
@permission_classes([IsAdminUser])
def RoleList(request):
    p =Role.objects.all()
    serializer = RoleSerializer(p , many=True)
    return Response(serializer.data) 


#usercreation
@api_view(['POST'])
@authentication_classes([OAuth2Authentication])
@permission_classes([IsAdminUser])
def Usercreation(request):
    serializer = UserSerializers(data=request.data)

    if serializer.is_valid():
       user = serializer.createUser()
       serial = UserSerializer(user)
       return Response(serial.data,status=status.HTTP_201_CREATED)
    else:
        return Response({'msg':serializer.errors},status=status.HTTP_400_BAD_REQUEST )
#user list
@api_view(['GET'])
@authentication_classes([OAuth2Authentication])
@permission_classes([IsAdminUser])
def UsersList(request):
    p = User.objects.all()
    serializer = UserListSerializer(p , many=True)
    return Response(serializer.data) 
#userdetails
@api_view(['GET'])
@authentication_classes([OAuth2Authentication])
@permission_classes([IsAdminUser])
def Userdetails(request,pk):
    p = User.objects.get(id=pk)
    serializer = UserSerializer(p,many=False)
    return Response(serializer.data)
#delete user
@api_view(['DELETE'])
@authentication_classes([OAuth2Authentication])
@permission_classes([IsAdminUser])
def UserDelete(request, pk):
    p = User.objects.get(id=pk)
    p.delete()
    return Response("User is deleted successfully")
#delete role
@api_view(['DELETE'])
@authentication_classes([OAuth2Authentication])
@permission_classes([IsAdminUser])
def RoleDelete(request, pk):
    p = Role.objects.get(id=pk)
    p.delete()
    return Response("Role is deleted successfully")
#userprofile
class UserProfileView(APIView):
  authentication_classes = [OAuth2Authentication]
  permission_classes = [IsAuthenticated]
  def get(self, request, format=None):
    serializer = UserProfileSerializer(request.user)
    return Response(serializer.data, status=status.HTTP_200_OK)
#change password
@api_view(['PUT'])
@authentication_classes([OAuth2Authentication])
@permission_classes([IsAuthenticated])
def ChangePassword(request):
    serialized_data = ChangepasswordSerializer(data=request.data)
    if serialized_data.is_valid():
        user = request.user
        if User.check_password(user,serialized_data.validated_data['old_password']):
            if serialized_data.validated_data['new_password1'] == serialized_data.validated_data['new_password2']:
                user.password = make_password(serialized_data.validated_data['new_password1'])
                user.save()
                return Response(data='password successfully changed', status=status.HTTP_200_OK)
            return Response(data='New password don\'t match', status=status.HTTP_400_BAD_REQUEST)
        return Response(data='Invalid old password ',status=status.HTTP_400_BAD_REQUEST)
    return Response(data=serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)

# industry registration
@api_view(['POST'])
@permission_classes([AllowAny])
def IndustryCreate(request):
    serializer = Create_industrySerializer(data=request.data)
    Industry=None

    # serial=Null
    if serializer.is_valid():
       Industry = serializer.create()
       serial = IndustrySerializer(Industry)
       return Response(serial.data)
    else:
        return Response({'msg':serializer.errors})   

#Allindustries
@api_view(['GET'])
@authentication_classes([OAuth2Authentication])
@permission_classes([IsAdminUser])
def IndustryList(request):
    p = Industry.objects.all()
    serializer = IndustrySerializerList(p , many=True)
    return Response(serializer.data)
#application details
@api_view(['GET'])
@authentication_classes([OAuth2Authentication])
@permission_classes([IsAuthenticated])
def Appdetails(request,pk):
    p = Application.objects.get(id=pk)
    serializer = AppSerializer(p , many=False)
    return Response(serializer.data)
#get feedby id
@api_view(['GET'])
@authentication_classes([OAuth2Authentication])
@permission_classes([IsAuthenticated])
def Appfeeddetails(request,pk):
    p = ApplicationFeedback.objects.get(id=pk)
    serializer = FeedSerializers(p , many=False)
    return Response(serializer.data)
#get app by id
@api_view(['GET'])
@authentication_classes([OAuth2Authentication])
@permission_classes([IsAuthenticated])
def Appid(request,pk):
    p = Application.objects.get(id=pk)
    serializer = AppSerializerList(p , many=False)
    return Response(serializer.data)
#apply
@api_view(['POST'])
@authentication_classes([OAuth2Authentication])
@permission_classes([IsAuthenticated])
def Apply(request):
    serializer = ApplicationSerializer(data=request.data)
    if serializer.is_valid():
       application = serializer.create(request.user)
       serial = AppSerializer(application)
       return Response(serial.data,status=status.HTTP_201_CREATED)
    else:
        return Response({'msg':serializer.errors},status=status.HTTP_400_BAD_REQUEST )  
#list of applications according to evaluators
@api_view(['GET'])
@authentication_classes([OAuth2Authentication])
@permission_classes([IsAuthenticated])
def AppList(request):
    p =[]
    if request.user.role.type_name == 'Evaluator1' :
       p = Application.objects.filter(stage='review')
    elif request.user.role.type_name == 'Evaluator2':
       p = Application.objects.filter(stage='reevaluate')
    elif request.user.role.type_name == 'Evaluator3':
       p = Application.objects.filter(stage='Approval')
    else:
        p = Application.objects.filter(Industry=Industry.objects.get(pk=request.user.industry_id)) 

    serializer = AppSerializer(p , many=True)
    return Response(serializer.data,status=status.HTTP_200_OK)
@api_view(['GET'])
@authentication_classes([OAuth2Authentication])
@permission_classes([IsAuthenticated])
def AppfeedList(request,pk):
    p = ApplicationFeedback.objects.filter(application=pk)
    serializer = FeedSerializers(p , many=True)
    return Response(serializer.data)
#update Application
@api_view(['PUT'])
@authentication_classes([OAuth2Authentication])
@permission_classes([IsAuthenticated])
def ApproveApp(request, pk):
    application = Application.objects.get(id=pk)
    serializer = UpdateAppSerializer(instance=application , data=request.data)
    if serializer.is_valid():
        update_app = serializer.update(application,request.user)
        serial = AppSerializerList(update_app)
        return Response(serial.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
#ffedback creation
@api_view(['POST'])
@authentication_classes([OAuth2Authentication])
@permission_classes([IsAuthenticated])
def FeedApp(request, pk):
    try:
       application = Application.objects.get(id=pk)
       feed = ApplicationFeedback()
       if request.user.role.type_name == 'Evaluator1' and application.stage =='reevaluate':
           feed.applicant_name = application.Industry.Brand_name
           feed.applicant_address = application.Industry.physical_address
           feed.brand_name = application.Brand_name
           feed.common_name = request.data['common_name']
           feed.food_category = request.data['food_category']
           feed.screening_date = application.date_submitted
           feed.food_additive = application.food_additive
           feed.evaluation_date = datetime.datetime.now()
           if bool(request.FILES.get('product_image') and request.FILES.get('food_ingredient_image')):

             feed.product_image=request.FILES.get('product_image')
             feed.food_ingredient_image=request.FILES.get('food_ingredient_image')
           if bool(request.FILES.get('lab_result')):
                feed.lab_result = request.FILES.get('lab_result')
           feed.application = Application.objects.get(pk=application.pk)
           feed.user = User.objects.get(pk=request.user.pk)
           feed.save()
           content = {'code': 200, 'description': 'Feedback added Successfuly'}
           return Response(content, status.HTTP_200_OK)
    except Exception as e:
        print(str(e))
        content = {'code': 500, 'description': 'Error Occurred try again'}
        return Response(content, status.HTTP_200_OK)
@api_view(['PUT'])
@authentication_classes([OAuth2Authentication])
@permission_classes([IsAuthenticated])
def FeedUpApp(request,pk):
    application = ApplicationFeedback.objects.get(id=pk)
    serializer = FeedupSerializer(instance=application , data=request.data)
    if serializer.is_valid():
        update_app = serializer.updatefed(request.user,application)
        serial = FeedSerializers(update_app)
        return Response(serial.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
@api_view(['PUT'])
@authentication_classes([OAuth2Authentication])
@permission_classes([IsAuthenticated])
def RejectApp(request, pk):
    application = Application.objects.get(id=pk)
    serializer = RejectAppSerializer(instance=application , data=request.data)
    if serializer.is_valid():
        update_app = serializer.reject(application,request.user)
        serial = AppSerializerList(update_app)
        return Response(serial.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
#counting users
@api_view(['GET'])
@authentication_classes([OAuth2Authentication])
@permission_classes([IsAdminUser])
def Usercount(request):
    users = User.objects.all()
    list_users = users.count() 
    return Response(list_users)
#counting Industry
@api_view(['GET'])
@authentication_classes([OAuth2Authentication])
@permission_classes([IsAdminUser])
def Industrycount(request):
    users = Industry.objects.all()
    list_industry = users.count() 
    return Response(list_industry)
#counting pending application
@api_view(['GET'])
@authentication_classes([OAuth2Authentication])
@permission_classes([IsAuthenticated])
def Pendingcount(request):
    users = Application.objects.filter(status='pending',Industry=request.user.industry_id).count()
    print(users)
    return Response(users)
#count complete
@api_view(['GET'])
@authentication_classes([OAuth2Authentication])
@permission_classes([IsAuthenticated])
def Completecount(request):
    users = Application.objects.filter(status='complete',Industry=request.user.industry_id).count()
    print(users)
    return Response(users)
#count rejected
@api_view(['GET'])
@authentication_classes([OAuth2Authentication])
@permission_classes([IsAuthenticated])
def Rejectedcount(request):
    users = Application.objects.filter(status='rejected',Industry=request.user.industry_id).count()
    print(users)
    return Response(users)
#reject evaluator
@api_view(['GET'])
@authentication_classes([OAuth2Authentication])
@permission_classes([IsAuthenticated])
def Rejectedevcount(request):
    users = Application.objects.filter(status='rejected').count()
    print(users)
    return Response(users)
#completeevaluator
@api_view(['GET'])
@authentication_classes([OAuth2Authentication])
@permission_classes([IsAuthenticated])
def Completeevcount(request):
    users = Application.objects.filter(status='complete').count()
    print(users)
    return Response(users)
#pending evaluator
@api_view(['GET'])
@authentication_classes([OAuth2Authentication])
@permission_classes([IsAuthenticated])
def Pendingevcount(request):
    users = Application.objects.filter(status='pending').count()
    print(users)
    return Response(users)
#approval notification
def ApprovalNotification(phone , names , date):
    token='eyJhbGciOiJub25lIn0.eyJpZCI6MzczLCJyZXZva2VkX3Rva2VuX2NvdW50IjowfQ.'
    headers = {'Authorization': 'Bearer ' + token}
    s = ' Dear {} your Application  Submitted On {} has been approved Return to the P.R.I.S System to pay for Your License ,Thanks'.format(names,date) 
    data = {'to' : phone, 'text' : s, 'sender' : 'PRIS_RFDA'}

    url = 'https://api.pindo.io/v1/sms/'
    response = requests.post(url, json=data, headers=headers)
    print(response)
    print(response.json())
    return Response(response)

#credentials notification
def CredentialsNotification(phone ,username,password):
    token='eyJhbGciOiJub25lIn0.eyJpZCI6MzczLCJyZXZva2VkX3Rva2VuX2NvdW50IjowfQ.'
    headers = {'Authorization': 'Bearer ' + token}
    s = 'Your account has been created , your credentials for the system username:{} and password {}'.format(username,password)  
    data = {'to' : phone, 'text' : s, 'sender' : 'PRIS_RFDA'}

    url = 'https://api.pindo.io/v1/sms/'
    response = requests.post(url, json=data, headers=headers)
    print(response)
    print(response.json())
    return Response(response)
#rejection notification
def RejectionNotification(phone ,date_submitted,comments):
    token='eyJhbGciOiJub25lIn0.eyJpZCI6MzczLCJyZXZva2VkX3Rva2VuX2NvdW50IjowfQ.'
    headers = {'Authorization': 'Bearer ' + token}
    s = 'Your Application submitted on {} has been Rejected , try again by collecting mistakes Found:{} thanks'.format(date_submitted,comments)  
    data = {'to' : phone, 'text' : s, 'sender' : 'PRIS_RFDA'}

    url = 'https://api.pindo.io/v1/sms/'
    response = requests.post(url, json=data, headers=headers)
    print(response)
    print(response.json())
    return Response(response)
# class MakePayment(APIView):
#     authentication_classes = [OAuth2Authentication]
#     permission_classes = [permissions.IsAuthenticated]

#     def post(self,request,pk):
#         application = Application.objects.get(id=pk)
#         serializer = CreatePlanSerializer(data=request.data,many=True)
#         plan = Plan()
#         if serializer.is_valid():
#             pay_object={
#                 "reference_number":application.pk,
#                 "amount":plan.price,
#                 "customer_name":plan.name,
#                 "customer_phone":application.Industry.Phone,
#                 "customer_email":application.Industry.email,
#                 'redirect_url':settings.FRONTEND_PROJECT_URL+"/payments/"+application.pk+"success" #Will be frontend URL
#             }
#             payment_response=CreatePayment.make_payment(pay_object)
#             return Response(data=payment_response, status=status.HTTP_200_OK)
#         else:
#             return Response(serializer.errors,status=status.HTTP_401_UNAUTHORIZED)
#proccessing payment
@api_view(['POST'])
@authentication_classes([OAuth2Authentication])
@permission_classes([IsAuthenticated])
def RejectionNotificatio(phone ,hour,name):
    token='eyJhbGciOiJub25lIn0.eyJpZCI6MzczLCJyZXZva2VkX3Rva2VuX2NvdW50IjowfQ.'
    headers = {'Authorization': 'Bearer ' + token}
    s = 'Dear {} Remember to take your medicine at {} thanks'.format(hour,name)  
    data = {'to' : phone, 'text' : s, 'sender' : 'We-actx'}

    url = 'https://api.pindo.io/v1/sms/'
    response = requests.post(url, json=data, headers=headers)
    print(response)
    print(response.json())
    return Response(response)
def process_payment(name,email,amount,phone):
     auth_token= env('FLUTTER_WAVE')
     hed = {'Authorization': 'Bearer ' + auth_token,'Content-Type': 'application/json',}
     data = {
                "tx_ref":''+str(math.floor(1000000 + random.random()*9000000)),
                "amount":amount,
                "currency":"RWF",
                "redirect_url":"http://localhost:3000/#/dashboard/industry",
                "payment_options":"mobilemoneyrwanda",
                "customer":{
                    "email":email,
                    "phonenumber":phone,
                    "name":name
                },
                "customizations":{
                    "title":"Product Regulatory & Inspection System",
                    "description":"Pay License certificate",
                    "logo":"media/logo1.png"
                }
                }
     url = 'https://api.flutterwave.com/v3/payments'
     response = requests.post(url, json=data, headers=hed)
     response=response.json()
     print(response)
    #  if response['status'] == "success":
    #            return response
     link=response['data']['link']
     return link

# Application plan creation & payment
@api_view(['POST']) 
@authentication_classes([OAuth2Authentication])
@permission_classes([IsAuthenticated])
def CreatePlan(request, pk):
    application = Application.objects.get(id=pk)
    plan = Plan()
    plan.names = request.data['names']
    plan.email = request.data['email']
    plan.phone = request.data['phone']
    plan.amount=5000
    plan.application = Application.objects.get(id=pk)
    plan.save()
    name =plan.names
    email = plan.email
    amount = plan.amount
    phone = plan.phone
    application.paid = True
    application.save()
    data = process_payment(name,email,amount,phone)
    return Response(data) 
    

#industry list report
def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        # print('hello')
        # response = HttpResponse(result.getvalue(), content_type='application/pdf')
        return result
    else:
        print(pdf.err)
        return None

@api_view(['POST'])
@authentication_classes([OAuth2Authentication])
@permission_classes([IsAdminUser])
def industryReport(request):
    try:
        # data_before = '2023-08-01T09:02:57.074234Z'
        #data_after = datetime.datetime.now()
        order_db = Industry.objects.all()     
    except:
        return HttpResponse("505 Not Found")
         
    data = {
            'order':order_db,
            'imagePath': os.path.abspath("media/logo1.png"),
            'printed_date':datetime.datetime.now()
    }
    pdf = render_to_pdf('Industry.html', data)
    response = HttpResponse(pdf.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=industry.pdf'
    return response
    return Response(pdf, content_type='application/pdf')

#Application report
@api_view(['POST'])
@authentication_classes([OAuth2Authentication])
@permission_classes([IsAuthenticated])
def ApplicationReport(request):   
    order_db = Application.objects.filter(Industry=request.user.industry_id, paid=True,status='complete')
    count = order_db.count()
    p = Application.objects.get(Industry=request.user.industry_id)
    plan = Plan.objects.filter(application=p)
    for p in plan:
        total += p.amount     #you can filter using order_id as well
    # except:
    #     return HttpResponse("505 Not Found")
         
    data = {
            'order':order_db,
            'imagePath': os.path.abspath("media/logo1.png"),
            'printed_date':datetime.datetime.now(),
            'nbr':count,
            'total':total,
            'plan':plan,
            'by':request.user.names
    }
    pdf = render_to_pdf('appReport.html', data)
    response = HttpResponse(pdf.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=appReport.pdf'
    return response
    return Response(pdf, content_type='application/pdf')
#qrcode
@api_view(['POST'])
@authentication_classes([OAuth2Authentication])
@permission_classes([IsAuthenticated])
def generateqr(request):
    datas ='hello world'
    img = make(datas)
    img_name = 'qr' + str(datetime.datetime.now()) + '.png'
    img.save('media/' + img_name)
    return Response({img_name}, status=status.HTTP_201_CREATED)
    # return render(request, 'licenseCertificate.html', {'img_name': img_name})
#License report
@api_view(['POST'])
@authentication_classes([OAuth2Authentication])
@permission_classes([IsAuthenticated])
def licenseReport(request,pk):
    try:
         order_db = Application.objects.get(pk=pk,Industry=request.user.industry_id, paid=True,status='complete') 
         feed = ApplicationFeedback.objects.get(application=pk) 
        #  print(feed.applicant_name)  #you can filter using order_id as well
    except:
        return HttpResponse("505 Not Found")
    datas ='Manufacturer'+':'+feed.applicant_name + ' - ' + 'Product Name'+':'+feed.brand_name
    img = make(datas)
    img_name = 'qr' + str(datetime.datetime.now()) + '.png'
    img.save('media/' + img_name)
    # img = generateqr(HttpRequest)
    print(img)
    data = {
            'order':order_db,
            'o':feed.applicant_name,
            'add':feed.applicant_address,
            'br':feed.brand_name,
            'pk':order_db.packaging_material,
            'tg':order_db.target_user,
            'imagePath': os.path.abspath("media/logo1.png"),
            'img':os.path.abspath("media/log1.png"),
            'im':img_name,
            'ev_date':datetime.datetime.now(),
    }
    pdf = render_to_pdf('licenseCertificate.html', data)
    response = HttpResponse(pdf.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=licenseLicense.pdf'
    return response
    return Response(pdf, content_type='application/pdf')
#qrcode


#    factory = qrcode.image.svg.SvgPathImage
#    svg_img = qrcode.make("hello world",image_factory=factory)
#    data = svg_img.save('myqr.svg')
#    return render(request, 'licenseCertificate.html',{'img':data})

#reject application
@api_view(['POST'])
@authentication_classes([OAuth2Authentication])
@permission_classes([IsAuthenticated])
def Reject(request,pk):
    app = ApplicationFeedback.objects.get(application=pk)
    ap = Application.objects.all()
    app.application.status = 'rejected'
    app.save()
    ap.save()

@api_view(['POST'])
@authentication_classes([OAuth2Authentication])
@permission_classes([IsAuthenticated])
def Approval(request,pk):
   app = ApplicationFeedback.objects.filter(id=pk)
   phone = app.phone
   return Response(phone)
# @api_view(['POST'])
# @authentication_classes([OAuth2Authentication])
# @permission_classes([IsAuthenticated])
# def Industry_check(request):
#     industry = Industry()
#     c = Rdb.objects.all()
#     b=RdbSerializer(c , many=True)
#     print(b)
#     industry.owner_name = request.data['owner_name']
#     industry.Brand_name = request.data['Brand_name']
#     industry.physical_address = request.data['physical_address']
#     industry.Phone = request.data['Phone']
#     industry.email = request.data['email']
#     if b.data.company_name !=industry.Brand_name:
#        return Response({"msg":"not in databse"})
#     # return Response(b.data)




