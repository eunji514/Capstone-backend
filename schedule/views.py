from rest_framework.views import APIView
from rest_framework.response import Response
from .models import CalendarEvent
from .serializers import CalendarEventSerializer

class MonthlyCalendarView(APIView):
    def get(self, request):
        year = int(request.query_params.get("year"))
        month = int(request.query_params.get("month"))

        events = CalendarEvent.objects.filter(
            start__year=year,
            start__month=month
        )
        serializer = CalendarEventSerializer(events, many=True)
        return Response(serializer.data)
