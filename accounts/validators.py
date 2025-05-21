import re
from django.core.exceptions import ValidationError

def validate_strong_password(password):
    if len(password) < 8:
        raise ValidationError("비밀번호는 최소 8자 이상이어야 합니다.")
    if not re.search(r'[A-Z]', password):
        raise ValidationError("비밀번호에 대문자가 포함되어야 합니다.")
    if not re.search(r'[a-z]', password):
        raise ValidationError("비밀번호에 소문자가 포함되어야 합니다.")
    if not re.search(r'[!@#$%^&*(),.?\":{}|<>]', password):
        raise ValidationError("비밀번호에 특수문자가 포함되어야 합니다.")
