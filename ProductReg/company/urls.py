from django.urls import path
# from accounts.views import RegisterAPI
from . import views


urlpatterns = [
    # path('userlist/', views.UserList, name="userlist"),
     path('create_company/', views.Createcompany, name="login"),
    # path('industrycreate/', views.IndustryCreate, name="industrycreate"),#creation of industry
    # path('Apply/', views.Apply, name="Apply"),#applicaton for license
    # path('profile/', UserProfileView.as_view(), name='profile'),#userprofile
    # path('payment/<str:pk>', views.CreatePlan, name='payment'),#userprofile
    # path('usercreation/', views.Usercreation, name='usercreation'),# creating account for users
    # path('Appid/<str:pk>', views.Appid, name='appid'),# creating account for users
    # path('IndustryList/', views.IndustryList, name='IndustryList'),# viewing list of industry
    # path('userList/', views.UsersList, name='userList'),# viewing list of users
    # path('roleList/', views.RoleList, name='roleList'),# viewing list of roles
    # path('Listofapp/', views.AppList, name='Listofapp'),#for listing application according to roles
    # path('Listoffeed/<str:pk>', views.AppfeedList, name='Listofapp'),#for listing application according to roles
    # path('Userdetails/<str:pk>/', views.Userdetails, name='Userdetails'),#for viewing user details
    # path('Appdetail/<str:pk>', views.Appdetails, name='Appdetail'),#for viewing user details
    # path('Appfeeddetail/<str:pk>', views.Appfeeddetails, name='Appdetail'),#for viewing user details
    # path('deleteuser/<str:pk>/', views.UserDelete, name='deleteuser'),#for deleting user 
    # path('ApproveApp/<str:pk>', views.ApproveApp, name='ApproveApp'),#for Approve  Application  
    # path('FeedApp/<str:pk>', views.FeedApp, name='FeedApp'),#for Approve  Application  
    # path('FeedUpApp/<str:pk>', views.FeedUpApp, name='FeedUpApp'),#for Approve  Application  
    # path('RejectApp/<str:pk>/', views.RejectApp, name='RejectApp'),#for rejection of Application  
    # path('rolecreate/', views.Rolecreation, name='rolecreate'),#for role creation
    # path('roledelete/<str:pk>/', views.RoleDelete, name='roledelete'),#for role delete
    # path('countusers/', views.Usercount, name='countusers'),#for counting users
    # path('countindustry/', views.Industrycount, name='countindustry'),#for rcounting industry
    # path('countpending/', views.Pendingcount, name='countpending'),#for rcounting pending
    # path('countcomplete/', views.Completecount, name='countcomplete'),#for rcounting complete
    # path('countrejected/', views.Rejectedcount, name='countrejected'),#for rcounting rejected
    # path('countrejectedev/', views.Rejectedevcount, name='countrejected'),#for rcounting rejected
    # path('countcompleteev/', views.Completeevcount, name='countrejected'),#for rcounting rejected
    # path('countpendingev/', views.Pendingevcount, name='countrejected'),#for rcounting rejected
    # path('password/', views.ChangePassword, name='passwordchange'),#for changing password
    # path('callback', views.payment_response, name='payment_response'),
    # path('industry_report/',views.industryReport, name='industryReport'),
    # path('app_report',views.ApplicationReport, name='AppReport'),
    # path('license/<str:pk>',views.licenseReport,name='license'),
    # path('generate/',views.generateqr,name='license'),
    # path('approval/<str:pk>',views.Approval,name='license'),



]