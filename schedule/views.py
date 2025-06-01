from rest_framework.views import APIView
from rest_framework.response import Response
from .models import CalendarEvent
from .serializers import CalendarEventSerializer

class MonthlyCalendarView(APIView):
    def get(self, request):
        year = int(request.query_params.get("year"))
        month = int(request.query_params.get("month"))
        council_id = request.query_params.get("council_id") 
        events = CalendarEvent.objects.filter(
            start__year=year,
            start__month=month
        )
        if council_id:
            events = events.filter(student_council_id=council_id)

        return Response(CalendarEventSerializer(events, many=True).data)
