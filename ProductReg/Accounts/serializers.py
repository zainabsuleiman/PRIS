from django.urls import path, include
from django.contrib.auth.models import User, Group
from django.contrib import admin
admin.autodiscover()
from . models import *
from rest_framework import generics, permissions, serializers
from django.contrib.auth.hashers import make_password, check_password
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope

# first we define the serializers
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', "names","phone","role")
class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'
class UserListSerializer(serializers.ModelSerializer):
  
    class Meta:
        model = User
        fields = ('id','username', 'email', "names","phone","created_at","updated_at")
    
class UserSerializers(serializers.Serializer):
    names = serializers.CharField(max_length=200)
    username = serializers.CharField(max_length=200)
    phone = serializers.CharField(max_length=200)
    email = serializers.EmailField()
    role= serializers.IntegerField()
    def createUser(self):
        from .views import CredentialsNotification
        users = User()
        users.names = self.validated_data.get('names')
        users.username = self.validated_data.get('username')
        users.phone = self.validated_data.get('phone')
        users.email = self.validated_data.get('email')
        users.is_defaultPassword = True
        users.password = make_password('p@ssw@rd')
        users.role = Role.objects.get(pk=self.validated_data.get('role'))
        users.save()
        p= users.phone
        u = users.username
        ps = 'p@ssw@rd'
        CredentialsNotification(p,u,ps)
        return users
class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ("name", )

# Create the API views
# class UserList(generics.ListCreateAPIView):
#     permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

# class UserDetails(generics.RetrieveAPIView):
#     permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

class GroupList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated, TokenHasScope]
    required_scopes = ['groups']
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
class ChangepasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=200)
    new_password1 = serializers.CharField(max_length=200)
    new_password2 = serializers.CharField(max_length=200)

class IndustrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Industry
        fields = ['owner_name','Brand_name','physical_address','Phone','email']
class IndustrySerializerList(serializers.ModelSerializer):
    class Meta:
        model = Industry
        fields = ['id','owner_name','Brand_name','physical_address','Phone','email']
class AppSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = '__all__'
class FeedAppSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationFeedback
        fields = ['id','applicant_name','applicant_address','brand_name','common_name','food_category','screening_date','product_image','food_ingredient_image','food_additive','evaluation_date','application','user','lab_result']
class FeedSerializers(serializers.ModelSerializer):
    class Meta:
        model = ApplicationFeedback
        fields = '__all__'
class AppSerializerList(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ['id','Brand_name','product_form','intended_use','status','stage','Industry']
class UserProfileSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ['id', 'email', 'username','role'] 
class PlanSerializer(serializers.ModelSerializer):
    class Meta:
     model = Plan
     fields = '__all__'
class Create_industrySerializer(serializers.Serializer):
      owner_name = serializers.CharField(max_length=200)
      Brand_name = serializers.CharField(max_length=200)
      physical_address =serializers.CharField(max_length=200)
      Phone =serializers.CharField(max_length=200)
      email = serializers.EmailField()
      names = serializers.CharField(max_length=200)
      username = serializers.CharField(max_length=200)
      phone = serializers.CharField(max_length=200)
      email = serializers.EmailField()
     
    
      def create(self):
        from .views import CredentialsNotification
        industry = Industry()
        industry.owner_name = self.validated_data.get('owner_name')
        industry.Brand_name = self.validated_data.get('Brand_name')
        industry.physical_address = self.validated_data.get('physical_address')
        industry.Phone = self.validated_data.get('Phone')
        industry.email = self.validated_data.get('email')
        industry.save()
        users = User()
        users.names = self.validated_data.get('names')
        users.username = self.validated_data.get('username')
        users.phone = self.validated_data.get('phone')
        users.email = self.validated_data.get('email')
        users.is_defaultPassword = True
        users.password = make_password('p@ssw@rd')
        users.industry_id = industry.pk
        users.isindustry_user = True
        users.role = Role.objects.get(type_name = 'Industry')
        users.save()
        p= users.phone
        u = users.username
        ps = 'p@ssw@rd'
        CredentialsNotification(p,u,ps)
        return industry
#  
class ApplicationSerializer(serializers.Serializer):
    Brand_name = serializers.CharField(max_length=200)
    product_form = serializers.CharField(max_length=200)
    intended_use = serializers.CharField(max_length=200)
    target_user = serializers.CharField(max_length=200)
    shelf_life = serializers.CharField(max_length=200)
    packaging_material = serializers.CharField(max_length=200)
    storage_condition = serializers.CharField(max_length=200)
    food_ingredient = serializers.CharField(max_length=200)
    food_additive = serializers.CharField(max_length=200)
    nutritional_info = serializers.CharField(max_length=200)
    def create(self,user):
     print(user.industry_id)
     print(Industry.objects.get(pk=user.industry_id))
     
    #  print(Industry.objects.filter(pk=user.industry_id).first())
     app = Application()
     app.Brand_name = self.validated_data.get('Brand_name')
     app.product_form = self.validated_data.get('product_form')
     app.intended_use = self.validated_data.get('intended_use')
     app.food_additive = self.validated_data.get('food_additive')
     app.food_ingredient= self.validated_data.get('food_ingredient')
     app.nutritional_info = self.validated_data.get('nutritional_info')
     app.shelf_life = self.validated_data.get('shelf_life')
     app.packaging_material = self.validated_data.get('packaging_material')
     app.storage_condition = self.validated_data.get('storage_condition')
     app.target_user = self.validated_data.get('target_user')
     app.status = 'pending'
     app.stage = 'review'
     app.Industry = Industry.objects.filter(pk=user.industry_id).first()
     app.save()

     return app

class FeedSerializer(serializers.Serializer):
      def createfed(self,application,user):
        from .views import ApprovalNotification
        feed = ApplicationFeedback()
        if user.role.type_name == 'Evaluator1' and application.stage =='reevaluate':
           common_name = serializers.CharField(max_length=200)
           food_category = serializers.CharField(max_length=200)
           feed.applicant_name = application.Industry.Brand_name
           feed.applicant_address = application.Industry.physical_address
           feed.brand_name = application.Brand_name
           feed.common_name = self.validated_data.get('common_name')
           feed.food_category = self.validated_data.get('food_category')
           feed.screening_date = application.date_submitted
           feed.food_additive = application.food_additive
 
           feed.application = Application.objects.get(pk=application.pk)
           feed.user = User.objects.get(pk=user.pk)
           feed.save()
        elif user.role.type_name == 'Evaluator2' and application.stage =='Approval':
            laboratory_analysis = serializers.CharField(max_length=200)
            standards = serializers.CharField(max_length=200)
            recommendation = serializers.CharField(max_length=200)
            query =serializers.CharField(max_length=200)
            comments = serializers.CharField(max_length=200)
            feed.comments = self.validated_data.get('comments')
            feed.applicant_name = application.Industry.Brand_name
            feed.applicant_address = application.Industry.physical_address
            feed.screening_date = application.date_submitted
            feed.food_additive = application.food_additive
            feed.brand_name = application.Brand_name
            feed.laboratory_analysis = self.validated_data.get('laboratory_analysis')
            feed.standards = self.validated_data.get('standards')
            feed.query =self.validated_data.get('query')
            feed.recommendation =self.validated_data.get('recommendation')
            feed.save()
        elif user.role.type_name == 'Evaluator3' and application.stage =='Approval':
            application.status ='complete'
            application.stage = 'Approval'
            application.save()
            feed.save()
            name = application.Industry.owner_name
            date = application.date_submitted
            phone = application.Industry.Phone
            # p = Industry.objects.filter(pk=ide)
            print(phone)
            # print(phone)
            ApprovalNotification(phone, name,date)
        return feed
class FeedupSerializer(serializers.Serializer):
      laboratory_analysis = serializers.CharField(max_length=200)
      standards = serializers.CharField(max_length=200)
      recommendation = serializers.CharField(max_length=200)
      query =serializers.CharField(max_length=200)
      comments = serializers.CharField(max_length=200)
      def updatefed(self,user,feed):
          print(self.validated_data.get('comments'))
          if user.role.type_name == 'Evaluator2':
            feed.comments = self.validated_data.get('comments')
            feed.laboratory_analysis = self.validated_data.get('laboratory_analysis')
            feed.standards = self.validated_data.get('standards')
            feed.query =self.validated_data.get('query')
            feed.recommendation =self.validated_data.get('recommendation')
            feed.save()
             
          return feed

#applicationfeedback
class UpdateAppSerializer(serializers.Serializer):
      def update(self,application,user):
        from .views import ApprovalNotification
        feed = ApplicationFeedback()
        if user.role.type_name == 'Evaluator1' and application.stage =='review':
          
           
           application.stage ='reevaluate'
           application.status ='pending'
           application.save()
           
        elif user.role.type_name == 'Evaluator2' and application.stage =='reevaluate':
            
            
            application.status ='pending'
            application.stage = 'Approval'
            application.save()
            
        elif user.role.type_name == 'Evaluator3' and application.stage =='Approval':
            application.status ='complete'
            application.stage = 'Approval'
            application.save()
            name = application.Industry.owner_name
            date = application.date_submitted
            phone = application.Industry.Phone
            # p = Industry.objects.filter(pk=ide)
            print(phone)
            # print(phone)
            ApprovalNotification(phone, name,date)
        return application
class RejectAppSerializer(serializers.Serializer):
      comments = serializers.CharField(max_length=200)
      def reject(self,application,user):
        from .views import RejectionNotification
        feed = ApplicationFeedback()
        phone = application.Industry.Phone
        feed.comments = self.validated_data.get('comments')
        if user.role.type_name == 'Evaluator1' and application.stage =='review':
            application.status ='rejected'
            application.save()
            feed.save()
            comment = feed.comments
            date = application.date_submitted
            RejectionNotification(phone,date,comment)
        elif user.role.type_name == 'Evaluator2' and application.stage =='reevaluate':
            application.status ='rejected'
            application.save()
            feed.save()
            comment = feed.comments
            date = application.date_submitted
            RejectionNotification(phone,date,comment)
        elif user.role.type_name == 'Evaluator3' and application.stage =='Approval' :
            application.status ='rejected'
            application.save()
            feed.save()
            comment = feed.comments
            date = application.date_submitted
            RejectionNotification(phone,date,comment)
        return application

#payment serializer
class CreatePlanSerializer(serializers.Serializer):
    names = serializers.CharField(max_length=200)
    email= serializers.EmailField(max_length=200)
    phone = serializers.CharField(max_length=200)
    
    def createPlan(self,application):
        from .views import process_payment
        plan = Plan()
        plan.names = self.validated_data.get('names')
        plan.amount = 5000
        plan.email = self.validated_data.get('email')
        plan.phone = self.validated_data.get('phone')
        plan.application = Application.objects.get(pk=application.pk)
        plan.save()
        n = plan.names
        e = plan.email
        p =plan.phone
        a = plan.amount
        process_payment(n,e,p,a)
        return plan


