from rest_framework import serializers
from .models import User, BuddyProfile
from .validators import validate_strong_password

class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_strong_password])

    class Meta:
        model = User
        fields = ['email', 'password', 'student_id', 'name', 'major']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class BuddyProfileSerializer(serializers.ModelSerializer):
    interest = serializers.ListField(child=serializers.CharField())
    language = serializers.ListField(child=serializers.CharField())
    purpose = serializers.ListField(child=serializers.CharField())
    matching_type = serializers.ChoiceField(choices=["1:1"])
    student_type = serializers.ChoiceField(choices=["Korean", "International"])

    email = serializers.EmailField(read_only=True)  

    class Meta:
        model = BuddyProfile
        fields = ['email', 'interest', 'language', 'purpose', 'matching_type', 'student_type']

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
            student_type=validated_data['student_type']
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
        fields = ['interest', 'language', 'purpose', 'matching_type', 'student_type']


class UserProfileSerializer(serializers.ModelSerializer):
    buddy_profile = BuddyProfileReadSerializer()

    class Meta:
        model = User
        fields = ['email', 'name', 'student_id', 'major', 'buddy_profile', 'profile_image']