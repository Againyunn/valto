"""Capstone URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from . import views
from .views import*
from django.views import View

app_name='kapchikachi'


urlpatterns = [ #함수는 그냥 호출 / 클래스는 클래스명.as_view() 처리
    # path('main/',views.main_html, name='main'),
    ###메인 페이지 노출& 그래프, 댓글 노출###
    path('',views.GetChart, name='main'),

    ###운영진 소개###
    path('aboutus/', views.About_us, name='aboutus'),

    ###결제 유형 선택 페이지###
    path('SelectPayOption/', views.SelectPayOption, name='SelectPayOption'), #추가할 url페이지

    ###구매 페이지 시스템###
    path('purchase/', views.CommentCreate, name='CommentCreate'),
    path('pastinfo/', views.Find_past_info, name='FindPastInfo'), #기존 구매 이력창으로 넘기는 url
    path('check/', views.CheckBeforeSell, name='check'),
    path('checkbill/', views.Deposit, name="check_bill"),

    ####결제 시스템####
    # path('pay/', views.pay, name="pay"),
    ####아엠포트####
    path('charge/', views.purchase_order, name='purchase_order'),
    path('checkout/', views.OrderCheckoutAjaxView, name='order_checkout'),
    path('validation/', views.OrderImpAjaxView, name='order_validation'),

    path('payment/', views.real_sell, name="real_sell"),
    # path('checkbill/', views.check_bill, name="check_bill"),

    ####구매이력확인####
    path('personal/', views.Check_personal_buy, name='Check_personal_buy'),
    path('notfound_buy/', views.notfound_buy, name='notfound_buy'),

    ####사업자정보고지용####
    path('noticeinfo/', views.Notice_info, name='Notice_info'),
    path('qna/', views.Qna, name='Qna'),#고동현이 추가
    ####관리자용 페이지####
    path('download/', views.GetData, name='GetData'),
    path('delete/', views.DeleteData, name='DeleteData'),

    #상품목록
    path('dogairpod1/',views.Airpoddog1, name='DogAirpod12'),
    path('dogairpod2/', views.Airpoddog2, name='DogAirpodpro'),
    path('catairpod1/', views.Airpodcat1, name='CatAirpod12'),
    path('catairpod2/', views.Airpodcat2, name='CatAirpodpro'),
    path('dogkeyring/', views.KeyringDog, name='DogKeyring'),
    path('catkeyring/', views.KeyringCat, name='CatKeyring'),
     path('products/', views.Products, name='Products'),
]
