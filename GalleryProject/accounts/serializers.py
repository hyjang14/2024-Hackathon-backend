from rest_framework import serializers
from .models import User

from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

# 로그인
from dj_rest_auth.serializers import LoginSerializer
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate

# 커스텀 로그인
class CustomLoginSerializer(LoginSerializer):
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        # 사용자 인증
        self.user = authenticate(username=username, password=password)

        if self.user is None:
            raise serializers.ValidationError(('해당 사용자가 없습니다.'))

        if not self.user.is_active:
            raise serializers.ValidationError(('로그인 중이 아닙니다.'))

        # super().validate 호출 전에 user를 attrs에 설정
        attrs['user'] = self.user

        # 기본 validate 메소드 호출
        data = super().validate(attrs)

        # 토큰 생성 또는 가져오기
        token, created = Token.objects.get_or_create(user=self.user)

        # 사용자 데이터 반환
        data.update({
            'token': token.key,
            'usercode': self.user.id
        })

        return data
    
    
# 회원가입
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password_confirm = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    profile = serializers.ImageField(required=False)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'password_confirm', 'name', 'nickname', 'email', 'birthdate', 'phone', 'profile']
        extra_kwargs = {
            'password': {'write_only': True},
            'password_confirm': {'write_only': True},
        }

    # 비밀번호 유효성 검사
    def validate(self, data):
        password = data.get('password')
        password_confirm = data.get('password_confirm')

        # 비밀번호 확인 검사
        if password != password_confirm:
            raise serializers.ValidationError({'password_confirm': '비밀번호가 일치하지 않습니다.'})

        # 비밀번호 유효성 검사
        try:
            validate_password(password)
        except ValidationError as e:
            raise serializers.ValidationError({'password': e.messages})

        return data

    def create(self, validated_data):
        profile = validated_data.pop('profile', 'accounts_photo/default_profile.png')
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            name=validated_data.get('name', ''),
            nickname=validated_data.get('nickname', ''),
            email=validated_data.get('email', ''),
            birthdate=validated_data.get('birthdate', None),
            phone=validated_data.get('phone', ''),
            profile=validated_data.get('profile', None)
        )
        if profile:
            user.profile = profile
            user.save()

        return user



# 회원정보 수정
class UserUpdateSerializer(serializers.ModelSerializer):
   
   # 닉네임 중복 유효성 검사
    def validate_nickname(self, value):
        if User.objects.filter(nickname=value).exists():
            raise serializers.ValidationError("이미 존재하는 닉네임입니다.")
        return value
    
    def update(self, instance, validated_data):
        instance.profile = validated_data.get('profile', instance.profile)
        instance.nickname = validated_data.get('nickname', instance.nickname)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.birthdate = validated_data.get('birthdate', instance.birthdate)
        instance.save()
        return instance
    
    class Meta:
        model = User
        fields = ['id', 'username', 'name', 'nickname', 'email', 'birthdate', 'phone', 'profile']

# 회원정보 조회
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'name', 'nickname', 'email', 'birthdate', 'phone', 'profile']