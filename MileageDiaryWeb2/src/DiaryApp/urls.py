'''
Created on 2020/07/14

@author: snowc
'''
from django.urls import path
from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
from . import views

app_name = 'DiaryApp'
urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('<int:log_id>/', views.detail, name='detail'),
    path('<int:log_id>/results/', views.results, name='results'),
    path('<int:log_id>/vote/', views.addLog, name='addLog'),
    path('DiaryApp_list', views.LogListView.as_view(), name='DiaryApp_list'),
    path('create/', views.LogCreateView.as_view(), name='create'),
    path('<int:pk>/update/', views.LogUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.LogDeleteView.as_view(), name='delete'),
    path('log_chart/', views.ChartView, name='chart'),
    path('login/', auth_views.LoginView.as_view(template_name='DiaryApp/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('oauth/', include('social_django.urls', namespace='social')),
]