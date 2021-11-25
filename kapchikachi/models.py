from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from .iamport import validation_prepare, get_transaction
import hashlib, random, time
from django.db.models.signals import post_save
from markdownx.models import MarkdownxField

# Create your models here.

#구매자에게 입력 받을 코멘트
class Comment(models.Model):
    content = MarkdownxField(help_text='"석수" 관련 멘트를 남겨주시면 후원금을 석수에게 지급합니다!', blank=True) #구매자 코멘트 : 300자 이내로 제한
    created = models.DateTimeField(auto_now_add=True) #작성시간
    
    #유저가 누군지 입력 받게 할 지는 상의 필요
    author = models.ForeignKey(User, on_delete=models.CASCADE) #유저: sns로그인 해야 이용 할 수 있게 하는 경우

    # #현재유저식별을 위한 사용자명
    # username=models.CharField(max_length=50)

    #수취인 이름
    receiver_name = models.CharField(max_length=10, blank=False)

    #수취인 휴대폰 정보 입력 +정수형으로 할시 아마 0은 생략될거같에서 문자열로 수정(고동현)
    receiver_phone = models.CharField(max_length=12,blank=False)

    # #기부 타입(1개 단일 선택으로 만들 경우)
    # type_choice = (
    #     ('DC1', 'dog_case1'), #강아지 에어팟1
    #     ('DC2', 'dog_case2'), #강아지 에어팟2
    #     ('DKR', 'dog_keyring'), #강아지 키링
    #     ('CC1', 'cat_case1'), #고양이 에어팟1
    #     ('CC2', 'cat_case2'), #고양이 에어팟2
    #     ('CKR', 'cat_keyring'), #고양이 키링
    # )
    # donate_type = models.CharField(max_length=3, choices=type_choice)

    #기부 상품(복수 선택으로 만들 경우)

    count_method=(
        (0, '선택(0개)'),
        (1,1),
        (2,2),
        (3,3),
        (4,4),
        (5,5),
        (6,6),
        (7,7),
        (8,8),
        (9,9),
    )
    dog_case1 = models.IntegerField(default=0,choices=count_method, blank=True)
    dog_case2 = models.IntegerField(default=0,choices=count_method, blank=True)
    dog_keyring =models.IntegerField(default=0,choices=count_method, blank=True)
    cat_case1 =models.IntegerField(default=0,choices=count_method, blank=True)
    cat_case2 =models.IntegerField(default=0,choices=count_method, blank=True)
    cat_keyring = models.IntegerField(default=0,choices=count_method, blank=True )
    # dog_case1 = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)], blank=True)
    # dog_case2 = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)], blank=True)
    # dog_keyring = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)], blank=True)
    # cat_case1 = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)], blank=True)
    # cat_case2 = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)], blank=True)
    # cat_keyring= models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)], blank=True)

    #1인당 총 구매 금액  -> 배송비 + 원가는 나중에 빼기
    sell = models.IntegerField() #int형으로 받게 설정 + 음수 불가하도록 설정 필요(재윤)

    #배송방법 선택
    shipping_method = (
        ('0','직접수령(    0원)'),
        ('1','택배배송(2,800원)')
        # ('0','서울'),
        # ('1','부산'),
        # ('2','인천'),
        # ('3','대구'),
        # ('4','대전'),
        # ('5','광주'),
        # ('6','경기'),
        # ('7','강원'),
        # ('8','충남'),
        # ('9','충북'),
        # ('10','전북'),
        # ('11','전남'),
        # ('12','경북'),
        # ('13','경남'),
        # ('14','제주')
    )
    shipping=models.CharField(max_length=1, choices=shipping_method, blank=False, help_text="직접수령 선택시 담당자가 연락드립니다.")

    #배송지 #배송지 100자 이내로 입력가능
    detail_address=MarkdownxField(blank=True, help_text="택배배송 선택시 입력해주세요.")
    #detail_address=models.CharField(max_length=100, help_text="시/도를 포함한 배송받을 주소를 정확히 입력해주세요.", blank=True)

    #외대생 여부 확인
    hufs=models.BooleanField(default=False,blank=True)

    #결제 관련
    #입금자명
    deposit_name=models.CharField(max_length=10, blank=False)
    
    #구매번호(처리가 되었음을 알려주는 방법)
    order_num=models.IntegerField(blank=True,null=True)

    #입금완료여부
    deposit_check=models.IntegerField(blank=True,null=True)

    #실구매여부 확인 (구매 전: 0 , 구매 후:1)
    real_selled = models.IntegerField()  # 실구매여부 확인 (구매 전: 0 , 구매 후:1)

    # #현금영수증
    # cashreceipts_method=(
    #     ('0','발급안함'),
    #     ('1','발급')
    # )
    # cashreceipts=models.CharField(max_length=1,choices=cashreceipts_method, default='0', blank=False)

    # #현금영수증 번호 0생략 방지를 위해 char 지정
    # cashreceipts_num=models.CharField(max_length=12,blank=True,null=True, help_text="현금영수증 요청 시 입력해주세요.")

    #배송상태
    shipping_state_check=(
        ('0','준비중'),
        ('1','배송중'),
        ('2','배송완료')
    )
    shipping_state=models.CharField(max_length=1, choices=shipping_state_check, default='0', blank=True)


    def __str__(self):
        return f'{self.author}'

    def get_donator_pk(self):
        return(self.pk)

class Order(models.Model):
    user_pk = models.IntegerField(blank=False) #사용자 식별 번호
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    order_num = models.IntegerField(blank=False)  # 주문번호
    created = models.DateTimeField(auto_now_add=True, auto_now=False)  # order_created
    real_selled = models.IntegerField()  # 실구매여부 확인 (구매 전: 0 , 구매 후:1)
    order_sell = models.IntegerField() #1인당 총 구매 금액  -> 배송비 + 원가는 나중에 빼기


########주문 DB모델#########
class OrderTransaction(models.Model):
    user_pk = models.IntegerField(blank=False) #사용자 식별 번호
    # user_id = models.CharField(max_length=300,blank=False) #사용자 아이디(식별용)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    # order_created =  models.DateTimeField(auto_now_add=True) #작성시간
    order_num = models.IntegerField(blank=False) #주문번호
    order_sell = models.IntegerField() #1인당 총 구매 금액  -> 배송비 + 원가는 나중에 빼기
    real_selled = models.IntegerField() #실구매여부 확인 (구매 전: 0 , 구매 후:1)

    #######결제 시스템 연동 코드#######
    transaction_id = models.CharField(max_length=120, null=True, blank=True)
    order_id = models.CharField(max_length=120, unique=True) #order_num
    amount = models.PositiveIntegerField(default=0) #order_sell
    success = models.BooleanField(default=False)
    transaction_status = models.CharField(max_length=220, null=True, blank=True)
    type = models.CharField(max_length=120)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)#order_created

    def __str__(self):
        return self.order_id

    class Meta:
        ordering = ['-created']

class OrderTransactionManager(models.Manager):
    # 새로운 트랜젝션 생성
    def create_new(self, user, amount, type, success=None, transaction_status=None):
        if not user:
            raise ValueError("유저가 확인되지 않습니다.")
        short_hash = hashlib.sha1(str(random.random())).hexdigest()[:2]
        time_hash = hashlib.sha1(str(int(time.time()))).hexdigest()[-3:]
        base = str(user.email).split("@")[0]
        key = hashlib.sha1(short_hash + time_hash + base).hexdigest()[:10]
        new_order_id = "%s" % (key)
        # 아임포트 결제 사전 검증 단계
        validation_prepare(new_order_id, amount)
        # 트랜젝션 저장
        new_trans = self.model(
            user=user,
            order_id=new_order_id,
            amount=amount,
            type=type
        )
        if success is not None:
            new_trans.success = success
            new_trans.transaction_status = transaction_status
        new_trans.save(using=self._db)
        return new_trans.order_id

    # 생선된 트랜잭션 검증
    def validation_trans(self, merchant_id):
        result = get_transaction(merchant_id)
        if result['status'] is not 'paid':
            return result
        else:
            return None

    def all_for_user(self, user):
        return super(OrderTransactionManager, self).filter(user=user)

    def get_recent_user(self, user, num):
        return super(OrderTransactionManager, self).filter(user=user)[:num]

def new_point_trans_validation(sender, instance, created, *args, **kwargs):
    if instance.transaction_id:
        # 거래 후 아임포트에서 넘긴 결과
        v_trans = OrderTransaction.objects.validation_trans(
            merchant_id=instance.order_id
        )
        res_merchant_id = v_trans['merchant_id']
        res_imp_id = v_trans['imp_id']
        res_amount = v_trans['amount']
        # 데이터베이스에 실제 결제된 정보가 있는지 체크
        r_trans = OrderTransaction.objects.filter(
            order_id=res_merchant_id,
            transaction_id=res_imp_id,
            amount=res_amount
        ).exists()
        if not v_trans or not r_trans:
            raise ValueError('비정상적인 거래입니다.')
post_save.connect(new_point_trans_validation, sender=OrderTransaction)

# class Purchase(models.Model):

# class Chart(models.Model):