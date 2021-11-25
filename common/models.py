from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class Userinfo(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    # username = models.CharField(max_length=200,blank=True)
    # created = models.DateTimeField(auto_now_add=True)  # 작성시간
    email = models.EmailField(blank=True)
    gender_method=(
        (None,'선택'),
        ('0','남성'),
        ('1','여성')
    )
    gender = models.CharField(max_length=1, choices=gender_method, null=False, blank=False)
    birth = models.DateField(blank=True)



# class UserManager(BaseUserManager):
#     # 일반 user 생성
#     def create_user(self, email, gender, birth, password=None):
#         if not email:
#             raise ValueError('이메일을 입력해주세요.')
#         if not gender:
#             raise ValueError('성별을 선택해주세요.')
#         if not birth:
#             raise ValueError('생년월일을 지정해주세요.')
#         user = self.model(
#             email=self.normalize_email(email),
#
#         )
#         user.set_password(password)
#         user.save(using=self._db)
#         return user
#
#     # 관리자 user 생성
#     def create_superuser(self, email, gender, birth, password=None):
#         user = self.create_user(
#             email,
#             password=password,
#             gedner=gender,
#             birth=birth
#         )
#         user.is_admin = True
#         user.save(using=self._db)
#         return user


# class User(AbstractBaseUser):
#     id = models.AutoField(primary_key=True)
#     email = models.EmailField(default='', max_length=100, null=False, blank=False, unique=True)
#     gender_method=(
#         (None, '선택'),
#         ('0','남성'),
#         ('1','여성')
#     )
#     gender = models.CharField(max_length=1, choices=gender_method, null=False, blank=False)
#     birth = models.DateField(null=False, blank=False)
#
#     # User 모델의 필수 field
#     is_active = models.BooleanField(default=True)
#     is_admin = models.BooleanField(default=False)
#
#     # 헬퍼 클래스 사용
#     objects = UserManager()
#
#     # 사용자의 username field는 id로 설정
#     USERNAME_FIELD = 'id'
#     # 필수로 작성해야하는 field
#     REQUIRED_FIELDS = ['email', 'gender', 'birth']
#
#     def __str__(self):
#         return self.id

