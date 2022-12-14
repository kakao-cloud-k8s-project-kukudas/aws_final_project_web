from django import forms
from .models import User_info, User
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
    company_initial = forms.CharField(
        label='이니셜',
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'company_initial',
                'placeholder': '이니셜'
            }
        ),
        error_messages={'required': '이니셜을 입력해주세요'}
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
        'company_initial',
        'password',
        'password_confirm'
    ]
    class Meta:
        model=User_info
        fields=[ # DB 입력받을 field
            'company_name',
            'company_initial',
            'password'
        ]
    # is valid 실행시 호출되는 메소드
    def clean(self):
        cleaned_data=super().clean()
        company_name=cleaned_data.get('company_name','')
        company_initial=cleaned_data.get('company_initial','')
        password=cleaned_data.get('password','')
        password_confirm=cleaned_data.get('password_confirm','')
        # 비밀번호 검사/ 아이디 중복 검사
        # if User_info.objects.filter(company_name=company_name).exists():
        if User.objects.filter(username=company_name).exists():
            return self.add_error('company_name','이미 있는 아이디 입니다.')
        if User_info.objects.filter(company_initial=company_initial).exists():
            return self.add_error('company_initial','이미 있는 이니셜 입니다.')
        elif 4<len(company_initial):
            return self.add_error('company_initial','이니셜은 3자 이하로 적어주세요')
        if password!=password_confirm:
            return self.add_error('password_confirm','비밀번호가 다릅니다.')
        elif 8>len(password):
            return self.add_error('password','비밀번호는 8자 이상으로 적어주세요')
        else:
            self.company_name=company_name
            self.company_initial=company_initial
            # 비밀번호 암호화, DB에는 문자열로 저장되어야 함으로 decode을 이용해 string으로 바꿔준다.
            # self.password=bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            self.password_confirm=password_confirm
            
# 왜 modelorm을 사용하지 않는지? model과 연동하지 않음으로
class SigninForm(forms.Form):
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
    field_order=[
        'company_name',
        'password',
    ]
    # is valid 실행시 호출되는 메소드
    def clean(self):
        cleaned_data=super().clean()
        company_name=cleaned_data.get('company_name','')
        password=cleaned_data.get('password','')
        # 빈칸인지 확인, db와 비교
        if company_name=='':
            return self.add_error('company_name','회사이름을 다시 입력해주세요')
        elif password=='':
            return self.add_error('password','비밀번호를 다시 입력해주세요')
        else:
            try:
                user=User.objects.get(username=company_name)
            except User.DoesNotExist:
                return self.add_error('company_name', '회사가 존재하지 않습니다.')
            # 아래의 암호화 방식 사용하지 않음
            # if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            #     return self.add_error('password','비밀번호가 다릅니다.')
            self.login_session=user.username