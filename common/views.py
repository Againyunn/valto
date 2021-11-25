from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .forms import *
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from kapchikachi.models import Comment
from django.views.generic import ListView

#테스트용
# from django.shortcuts import render
# #from .serializers import UserSerializer
# from .models import User
# from rest_framework import generics


# Create your views here.
# class UserCreate(generics.CreateAPIView):
#     queryset = User.objects.all()
    #serializer_class = UserSerializer
#테스트용

# def signup1(request):
#     if request.method=='POST':
#         user_form=UserForm(request.POST)
#         # userinfo_form = UserinfoForm(request.POST)
#         if user_form.is_valid():
#             user_form.save() #회원가입 정보 저장
#             # userinfo_form.save()
#
#             username=user_form.cleaned_data.get('username')
#             raw_password=user_form.cleaned_data.get('password1')
#
#             #회원가입한 유저 로그인 처리
#             user=authenticate(username=username, password=raw_password)
#             login(request, user)
#             return redirect('kapchikachi:CommentCreate')
#             # return redirect('./kapchikachi/purchase/') #회원가입 후 로그인되면, 구매페이지로 이동
#
#         else:
#             # context = {
#             #     'user_form': UserForm(),
#             #     'userinfo_form': UserinfoForm(),
#             # }
#             #user_form=UserForm()
#             # userinfo_form=UserinfoForm()
#             return redirect('kapchikachi:aboutus')
#     user_form = UserForm()
#     return render(request, 'common/signup.html', {'user_form':user_form}) #, 'userinfo_form':userinfo_form})

def signup(request):
    if request.method=='POST':
        form1 = UserForm(request.POST)
        form2 = UserinfoForm(request.POST)
        # if form1.is_valid():# and form2.is_valid():

        if request.POST['password1']==request.POST['password2']:

            user=User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])

            auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')

            #저장된 User 호출
            this_user = request.user.id
            user = User.objects.get(id=this_user)

            tmp_birth_year =request.POST['birth_year']
            tmp_birth_month =request.POST['birth_month']
            tmp_birth_day = request.POST['birth_day']
            user_birth=tmp_birth_year+'-'+tmp_birth_month+'-'+tmp_birth_day

            userinfo = Userinfo.objects.create(username=user, email=request.POST['email'], gender=request.POST['gender'], birth=user_birth )
            userinfo.save()
            # result={'this_user':request.POST['username']}

            return redirect('kapchikachi:CommentCreate')
        #else:
        #    raise ValueError('입력 값을 확인해주세요.')
    else:
        form1 = UserForm()
        form2 = UserinfoForm()
        # 'userinfo_form': UserinfoForm(),
    return render(request, 'common/signup.html', {'user_form':form1, 'userinfo_form':form2})


# 유저 정보
# @login_required(login_url='common:login')
# def user_info(request):
#     all_data=Comment.objects.all()
#     db_num = len(all_data)
#
#     user_num = 0  # 현재 로그인한 유저 식별 번호(전체 데이터 중 현재 유저의 데이터 위치 인덱스 반환)
#     user_purchase_num = 0
#
#     # 현재 로그인 유저의 데이터 식별기능
#     for a in range(db_num):
#         if (str(all_data[a].author) == str(request.user.username)) and (
#                 int(all_data[a].sell) > 0):  # 현재 로그인 유저의 데이터 인덱스 번호 조회
#             user_num +=a
#             user_purchase_num += 1
#
#     user_name = str(all_data[a].author)
#
#     user_product_type = []
#     user_purchase_amount = []
#
#     for b in range(user_purchase_num):
#
#



# 유저 구매내역
@login_required(login_url='common:login')
def user_purchase(request):
    all_data=Comment.objects.all()
    db_num = len(all_data)

    user_data=[[0,0,0,0,0] for col in range(db_num)]
    user_num=[] #현재 로그인한 유저 식별 번호(전체 데이터 중 현재 유저의 데이터 위치 인덱스 반환)
    user_purchase_num=0

    #현재 로그인 유저의 데이터 식별기능
    for a in range(db_num):
        if (str(all_data[a].author) == str(request.user.username)) and (int(all_data[a].sell) >0): #현재 로그인 유저의 데이터 인덱스 번호 조회
            user_num.append(a)
            user_purchase_num+=1
        else:
            return render(request, 'common/user_purchase_none.html')

    #구매내역이 1번이라도 있는 경우
    if user_purchase_num>0:
        check=0
        user_purchase_time=[]
        user_product_type=[]
        user_purchase_amount=[]
        user_receiver_name=[]
        user_receiver_phone=[]
        user_receiver_address=[]
        #각각의 구매내역을 result에 추가
        for b in range(user_purchase_num):
            #구매정보
            # user_name=self.request.user.username#유저이름(식별용)
            this_purchase_time=str(all_data[user_num[b]].created) #구매일자

            this_receiver_name=all_data[user_num[b]].receiver_name #수취인 성함
            this_receiver_phone=all_data[user_num[b]].receiver_phone #수취인 번호
            this_receiver_address = all_data[user_num[b]].detail_address #수취인 주소(상세주소)

            #구매상품
            this_product_type = []  # 구매상품 종류

            if all_data[user_num[b]].dog_strap > 0:
                this_product_type.append(f'강아지 스트랩 {all_data[user_num[b]].dog_strap}개')
            if all_data[user_num[b]].dog_case > 0:
                this_product_type.append(f'강아지 케이스 {all_data[user_num[b]].dog_case}개')
            if all_data[user_num[b]].cat_strap > 0:
                this_product_type.append(f'고양이 스트랩 {all_data[user_num[b]].cat_strap}개')
            if all_data[user_num[b]].cat_case > 0:
                this_product_type.append(f'고양이 케이스 {all_data[user_num[b]].cat_case}개')

            #구매금액
            this_purchase_amount=all_data[user_num[b]].sell

            #반환값
            user_purchase_time.append(this_purchase_time)
            user_product_type.append(this_product_type)
            user_purchase_amount.append(this_purchase_amount)
            user_receiver_name.append(this_receiver_name)
            user_receiver_phone.append(this_receiver_phone)
            user_receiver_address.append(this_receiver_address)

            # result={
            #     'user_name':user_name,
            #     'user_purchase_time':user_purchase_time,
            #     'user_product_type':user_product_type,
            #     'user_purchase_amount':user_purchase_amount,
            #     'user_receiver_name':user_receiver_name,
            #     'user_receiver_phone':user_receiver_phone,
            #     'user_receiver_address':user_receiver_address,
            # }

        # total_num=[]
        # for i in range(user_purchase_num):
        #     total_num.append(str(i))
        total_num=int(user_purchase_num)

        result={
            'user_purchase_time':user_purchase_time,
            'user_product_type':user_product_type,
            'user_purchase_amount':user_purchase_amount,
            'user_receiver_name':user_receiver_name,
            'user_receiver_phone':user_receiver_phone,
            'user_receiver_address':user_receiver_address,
            'total_num':total_num,
        }


        return render(request,'common/user_purchase.html', context=result) #호출 시 for문으로 각 아이템별 호출 필요

    # return render(request,'common/user_purchase_none.html')

# 유저 구매내역
@login_required(login_url='common:login')
class PurchaseList(ListView):
    model=Comment

    def get_queryset(self):
        return Comment.objects.order_by('-created')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PurchaseList, self).get_context_data(**kwargs)
        context['category_list'] = Comment.objects.filter(author=self.user.username)
        return context