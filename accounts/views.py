import random, re
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.core.mail import send_mail
from django.core.exceptions import ValidationError
from .serializers import SignupSerializer, BuddyProfileSerializer, UserProfileSerializer
from .models import EmailVerification, User

class SignupUserInfoView(APIView):
    def post(self, request):
        email = request.data.get("email")

        if User.objects.filter(email=email).exists():
            return Response({"error": "이미 가입된 이메일입니다."}, status=400)

        record = EmailVerification.objects.filter(email=email, is_verified=True).first()
        if not record:
            return Response({"error": "이메일 인증이 필요합니다."}, status=400)
        

        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {
                    "message": "기본 정보 저장 완료",
                    "email": user.email  # buddyinfo 단계로 넘길 때 필요
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SignupBuddyInfoView(APIView):
    def post(self, request):
        email = request.data.get("email")
        if not email:
            return Response({"error": "이메일은 필수입니다."}, status=400)

        serializer = BuddyProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(email=email)
            return Response(
                {"message": "버디 정보 저장 완료. 회원가입이 완료되었습니다."},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmailVerificationRequestView(APIView):
    def generate_code(self):
        return ''.join(random.choices('0123456789', k=6))

    def validate_email(self, email):
        if not re.fullmatch(r'^[\w\.-]+@dankook\.ac\.kr$', email):
            raise ValidationError("단국대학교 이메일만 사용 가능합니다.")

    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({"error": "이메일을 입력하세요."}, status=400)

        try:
            self.validate_email(email)
        except ValidationError as e:
            return Response({"error": str(e)}, status=400)

        code = self.generate_code()

        EmailVerification.objects.update_or_create(
            email=email,
            defaults={'code': code, 'is_verified': False}
        )

        send_mail(
            subject="[단국대] 이메일 인증 코드",
            message=f"인증 코드: {code}",
            from_email=None,
            recipient_list=[email]
        )

        return Response({"message": "인증 코드가 이메일로 전송되었습니다."}, status=200)


class EmailVerificationConfirmView(APIView):
    def post(self, request):
        email = request.data.get('email')
        code = request.data.get('code')

        if not email or not code:
            return Response({"error": "이메일과 인증 코드를 모두 입력하세요."}, status=400)

        try:
            record = EmailVerification.objects.get(email=email)
        except EmailVerification.DoesNotExist:
            return Response({"error": "해당 이메일에 대한 인증 요청이 없습니다."}, status=404)

        if record.code != code:
            return Response({"error": "인증 코드가 일치하지 않습니다."}, status=400)

        record.is_verified = True
        record.code = None
        record.save()

        return Response({"message": "이메일 인증이 완료되었습니다."}, status=200)


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserProfileSerializer(user)
        return Response(serializer.data, status=200)


class ProfileImageView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        image = request.FILES.get('profile_image')
        if not image:
            return Response(
                {'detail': 'profile_image 파일을 함께 전송하세요.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = request.user
        # 기존 이미지 삭제
        if user.profile_image:
            user.profile_image.delete(save=False)

        user.profile_image = image
        user.save()

        serializer = UserProfileSerializer(user, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request):
        user = request.user
        # 파일 스토리지에서 삭제
        if user.profile_image:
            user.profile_image.delete(save=False)
        # default 값으로 되돌리기
        user.profile_image = 'profile_images/default.png'
        user.save()

        serializer = UserProfileSerializer(user, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class BuddyProfileEditView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        buddy = request.user.buddy_profile
        serializer = BuddyProfileSerializer(
            buddy,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # 변경된 전체 프로필 반환
        user_serializer = UserProfileSerializer(request.user, context={'request': request})
        return Response(user_serializer.data, status=status.HTTP_200_OK)
