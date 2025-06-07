def calculate_match_score(my_profile, candidate_profile):
    score = 0

    # 관심사
    my_interests = set(my_profile.interest.split(','))
    candidate_interests = set(candidate_profile.interest.split(','))
    score += len(my_interests & candidate_interests) * 20

    # 언어
    my_languages = set(my_profile.language.split(','))
    candidate_languages = set(candidate_profile.language.split(','))
    score += len(my_languages & candidate_languages) * 10

    # 교류 목적
    my_purposes = set(my_profile.purpose.split(','))
    candidate_purposes = set(candidate_profile.purpose.split(','))
    score += len(my_purposes & candidate_purposes) * 30

    return score


def get_buddy_status_color(user):
    active_count = BuddyRelation.objects.filter(
        models.Q(user=user) | models.Q(buddy=user),
        status='accepted',
        accepted_at__gte=timezone.now() - timedelta(days=14)
    ).count()

    if active_count >= 2:
        return 'red'
    return 'blue'
