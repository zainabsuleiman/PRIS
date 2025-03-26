from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.files import File
from PIL import Image
import datetime
# Create your models here.
STAGE = (('review','review'), ('reevaluate','reevaluate'),  ('Approval','Approval')
 
    )
STATUS = (('pending','pending'), ('rejected','rejected'),  ('complete','complete')
 
    )
def wrapper(instance, filename):
    new_filename = str(datetime.datetime.now()).split(
        '.')[0]+'_'+str(instance.id).split('-')[0]+'__'+filename
    return 'profilePictures/'+new_filename
class Role(models.Model):
    type_name = models.CharField(max_length=200)
    def __str__(self):
        return self.type_name
    class Meta:
     db_table = 'Role'
class Permission(models.Model):
      perm_name = models.CharField(max_length=200)
      def __str__(self):
        return self.perm_name
      class Meta:
        db_table = 'Permission'
class User(AbstractUser):
  username = models.CharField(max_length=200,unique=True)
  email = models.EmailField(
      verbose_name='Email',
      max_length=255
  )
  names = models.CharField(max_length=200)
  password = models.CharField(max_length=200)
  phone = models.CharField(max_length=200)
  industry_id = models.CharField(max_length=200)
  is_defaultPassword = models.BooleanField(default=False)
  isindustry_user = models.BooleanField(default=False)
  is_active = models.BooleanField(default=True)
  is_admin = models.BooleanField(default=False)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  role = models.ForeignKey(Role,null=True,on_delete=models.CASCADE)


  USERNAME_FIELD = 'username'
 
  class Meta:
     db_table = 'Users'

  def __str__(self):
      return self.username


class Industry(models.Model):
    owner_name = models.CharField(max_length=200,unique=True)
    Brand_name = models.CharField(max_length=200,unique=True)
    physical_address = models.CharField(max_length=200)
    Phone = models.CharField(max_length=20)
    email =models.CharField(max_length=20)
    created_At = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.owner_name
    class Meta:
     db_table = 'Industry'

class Application(models.Model):
    Brand_name = models.CharField(max_length=200)
    product_form = models.CharField(max_length=200)
    intended_use = models.CharField(max_length=200)
    target_user = models.CharField(max_length=200,null=True)
    shelf_life = models.CharField(max_length=200,null=True)
    storage_condition = models.CharField(max_length=200,null=True)
    food_ingredient = models.CharField(max_length=200,null=True)
    food_additive = models.CharField(max_length=200,null=True)
    packaging_material = models.CharField(max_length=200,null=True)
    nutritional_info = models.CharField(max_length=200,null=True)
    stage = models.CharField(max_length=200,null=True, choices=STAGE)
    status = models.CharField(max_length=200,null=True, choices=STATUS)
    date_submitted = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)
    Industry = models.ForeignKey(Industry,null=True,on_delete=models.CASCADE)
    def __str__(self):
        return self.product_form
    class Meta:
        db_table = 'Application'

class Plan(models.Model):
    names = models.CharField(max_length=200)
    email= models.EmailField(max_length=200)
    phone = models.CharField(max_length=20)
    amount = models.FloatField()
    application = models.ForeignKey(Application,null=True,on_delete=models.CASCADE)
    date_of_payment = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name
    class Meta:
        db_table ='Plan'
    
    
class ApplicationFeedback(models.Model):
    applicant_name = models.CharField(max_length=200,null=True)
    applicant_address = models.CharField(max_length=200,null=True)
    brand_name =models.CharField(max_length=200,null=True)
    phone = models.CharField(max_length=200,null=True)
    common_name = models.CharField(max_length=200,null=True)
    food_category = models.CharField(max_length=200,null=True)
    screening_date =models.DateTimeField(auto_now_add=False,null=True)
    product_image = models.ImageField(
        upload_to=wrapper, null=True, default=None)
    food_ingredient_image =  models.ImageField(
        upload_to=wrapper, null=True, default=None)
    lab_result = models.FileField(upload_to='static/media/')
    food_additive = models.CharField(max_length=200,null=True)
    laboratory_analysis = models.CharField(max_length=200,null=True)
    standards = models.CharField(max_length=200,null=True)
    recommendation = models.CharField(max_length=200,null=True)
    query = models.CharField(max_length=200,null=True)
    comments = models.CharField(max_length=200,null=True)
    evaluation_date = models.DateTimeField(auto_now_add=True)
    application = models.ForeignKey(Application,null=True,on_delete=models.CASCADE)
    user = models.ForeignKey(User,null=True,on_delete=models.CASCADE)
    def __str__(self):
        return self.applicant_address
    
           
    class Meta:
        db_table = 'ApplicationFeedback'