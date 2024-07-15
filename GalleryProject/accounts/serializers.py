from rest_framework import serializers
from .models import User

# 회원가입
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True, label='Confirm password')

    # 비밀번호 일치 유효성 검사
    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("비밀번호가 일치하지 않습니다.")
        return data
    
    # 아이디 중복 유효성 검사
    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("이미 존재하는 아이디입니다.")
        return value
    
    # 닉네임 중복 유효성 검사
    def validate_nickname(self, value):
        if User.objects.filter(nickname=value).exists():
            raise serializers.ValidationError("이미 존재하는 닉네임입니다.")
        return value

    def create(self, validated_data):
        validated_data.pop('password2')  # password2는 DB에 필요없는 칸이므로 삭제
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
        return user

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'password2', 'name', 'nickname', 'email', 'birthdate', 'phone', 'profile']


# 회원정보 수정
class UserUpdateSerializer(serializers.ModelSerializer):
   
   # 닉네임 중복 유효성 검사
    def validate_nickname(self, value):
        if User.objects.filter(nickname=value).exists():
            raise serializers.ValidationError("이미 존재하는 닉네임입니다.")
        return value
    
    def update(self, instance, validated_data):
        instance.profile = validated_data.get('username', instance.profile)
        instance.nickname = validated_data.get('nickname', instance.nickname)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.save()
        return instance
    
    class Meta:
        model = User
        fields = ['id', 'profile', 'nickname', 'phone']  

# 회원정보 조회
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'name', 'nickname', 'email', 'birthdate', 'phone', 'profile']