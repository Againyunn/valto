from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model= Comment
        fields=['receiver_name','receiver_phone','content', 'dog_case1', 'dog_case2', 'dog_keyring', 'cat_case1', 'cat_case2', 'cat_keyring', 'shipping', 'detail_address', 'hufs','deposit_name']
        labels= {
            'receiver_name': '수취인 성함', #배송받는 분
            'receiver_phone': '수취인 연락처',
            'content': '남기고 싶은 말',
            'dog_case1': '강아지 에어팟1,2 케이스',
            'dog_case2': '강아지 에어팟프로 케이스',
            'dog_keyring': '강아지 키링',
            'cat_case1': '고양이 에어팟1,2 케이스',
            'cat_case2': '고양이 에어팟프로 케이스',
            'cat_keyring': '고양이 키링',
            'shipping': '수령방법 선택', #배송비 책정용
            'detail_address': '배송지 입력',
            'hufs': '외대생 여부',
            'deposit_name': '예금주', #입금하는 사람 이름
            #'cashreceipts': '현금영수증 발급', #현금영수증 발급 여부 -> 동현 프론트 추가 요청(재윤)
            #'cashreceipts_num': '현금영수증 번호'#현금영수증 번호 발급 여부 -> 동현 프론트 추가 요청(재윤)
        }






