from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views, templates

app_name='common'

urlpatterns = [ #함수는 그냥 호출 / 클래스는 클래스명.as_view() 처리
    path('login/', auth_views.LoginView.as_view(template_name='common/login.html'), name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # path('record/', views.user_purchase, name='user_purchase'),
    # path('record/', views.PurchaseList.as_view(), name='PurchaseList'),
    #테스트용
    # path('signup2/', views.UserCreate.as_view()),
    # path('api-auth/', include('rest_framework.urls')),
]
