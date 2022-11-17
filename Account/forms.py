from django import forms
from .models import User
import bcrypt, json, re


class SignupForm(forms.ModelForm):
    company_name=forms.CharField(
        label='회사 이름',
        required=True,
        widget=forms.TextInput(
            attrs={
                'class':'company_name',
                'placeholder':'회사 이름'
            }
        ),
        error_messages={'required': '회사 이름을 입력해주세요'}
    )
    password=forms.CharField(
        label='비밀번호',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'class':'password',
                'placeholder':'비밀번호'
            }
        ),
        error_messages={'required': '비밀번호를 입력해주세요'}
    )
    password_confirm=forms.CharField(
        label='비밀번호 확인',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'class':'password-confirm',
                'placeholder':'비밀번호 확인'
            }
        ),
        error_messages={'required':'비밀번호가 일치하지 않습니다.'}
    )
    # 입력받을 순서 정하기
    field_order=[
        'company_name',
        'password',
        'password_confirm'
    ]
    class Meta:
        model=User
        fields=[ # DB 입력받을 field
            'company_name',
            'password'
        ]
    # is valid 실행시 호출되는 메소드
    def clean(self):
        cleaned_data=super().clean()
        company_name=cleaned_data.get('company_name','')
        password=cleaned_data.get('password','')
        password_confirm=cleaned_data.get('password_confirm','')
        # 비밀번호 검사
        # 1. 같게 썼는지 확인
        if password!=password_confirm:
            return self.add_error('password_confirm','비밀번호가 다릅니다.')
        elif 8>len(password):
            return self.add_error('password','비밀번호는 8자 이상으로 적어주세요')
        else:
            self.company_name=company_name
            # 비밀번호 암호화
            self.password=bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            self.password_confirm=password_confirm
            
        # 2. 비밀번호 8자 이상