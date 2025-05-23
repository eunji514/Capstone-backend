from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import SignupSerializer, BuddyProfileSerializer

class SignupUserInfoView(APIView):
    def post(self, request):
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
        serializer = BuddyProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "버디 정보 저장 완료. 회원가입이 완료되었습니다."},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)