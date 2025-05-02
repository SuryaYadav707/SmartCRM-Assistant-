from django.urls import path # type: ignore
from .import views


urlpatterns = [
    path('', views.home,name='home'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('chatquery/',views.chatquery,name='chatquery'),
    path("get_user_room/",views.get_user_room, name="get_user_room"), 
    path('sales/', views.sales_summariser, name='sales'),
    path('sales/download_pdf/', views.download_pdf, name='download_pdf'),  
    path('predictions/', views.run_churn_prediction, name='predictions'),


]

