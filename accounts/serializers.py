from rest_framework import serializers
from .models import User, BuddyProfile
from .validators import validate_strong_password
from django.conf import settings

class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_strong_password])

    class Meta:
        model = User
        fields = ['email', 'password', 'student_id', 'name', 'major', 'student_type']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class BuddyProfileSerializer(serializers.ModelSerializer):
    interest = serializers.ListField(child=serializers.CharField())
    language = serializers.ListField(child=serializers.CharField())
    purpose = serializers.ListField(child=serializers.CharField())
    matching_type = serializers.CharField()

    email = serializers.EmailField(write_only=True)  

    class Meta:
        model = BuddyProfile
        fields = ['email', 'interest', 'language', 'purpose', 'matching_type']

    def create(self, validated_data):
        email = validated_data.pop('email')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError({"email": "해당 이메일의 사용자가 존재하지 않습니다."})

        interest = ",".join(validated_data.pop('interest'))
        language = ",".join(validated_data.pop('language'))
        purpose = ",".join(validated_data.pop('purpose'))

        return BuddyProfile.objects.create(
            user=user,
            interest=interest,
            language=language,
            purpose=purpose,
            matching_type=validated_data['matching_type'],
        )

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['interest'] = instance.interest.split(',')
        rep['language'] = instance.language.split(',')
        rep['purpose'] = instance.purpose.split(',')
        return rep 


class BuddyProfileReadSerializer(serializers.ModelSerializer):
    interest = serializers.SerializerMethodField()
    language = serializers.SerializerMethodField()
    purpose = serializers.SerializerMethodField()

    def get_interest(self, obj):
        return obj.interest.split(',')

    def get_language(self, obj):
        return obj.language.split(',')

    def get_purpose(self, obj):
        return obj.purpose.split(',')

    class Meta:
        model = BuddyProfile
        fields = ['interest', 'language', 'purpose', 'matching_type']


class UserProfileSerializer(serializers.ModelSerializer):
    buddy_profile = BuddyProfileReadSerializer()
    profile_image = serializers.ImageField(
        required=False,
        allow_null=True,
        use_url=True,           
    )
    profile_image_url = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'email', 'name', 'student_id', 'major', 'student_type',
            'buddy_profile', 'profile_image', 'profile_image_url'
        ]

    def get_profile_image_url(self, obj):
        # profile_image가 없으면 None 반환
        if not obj.profile_image:
            return None
            
        # request context 확인
        request = self.context.get('request')
        if request is not None:
            return request.build_absolute_uri(obj.profile_image.url)
        
        # request가 없는 경우 URL만 반환
        return obj.profile_image.url

    # def update(self, instance, validated_data):
    #     # 프로필 이미지를 포함한 부분 업데이트
    #     image = validated_data.pop('profile_image', None)
    #     if image is not None:
    #         instance.profile_image = image
    #     if image is None:
    #         instance.profile_image = 'profile_images/default.png'
    #     return super().update(instance, validated_data)
