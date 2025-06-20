from rest_framework.views import APIView
from rest_framework.response import Response
from .models import CalendarEvent
from .serializers import CalendarEventSerializer
from datetime import datetime

class MonthlyCalendarView(APIView):
    def get(self, request):
        year = request.query_params.get("year")
        month = request.query_params.get("month")
        events = CalendarEvent.objects.filter(
            start__year=year,
            start__month=month
        )

        return Response(CalendarEventSerializer(events, many=True).data)

class EventsByDateView(APIView):
    def get(self, request):
        date_str = request.query_params.get("date")  # 'YYYY-MM-DD'
        try:
            date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except (TypeError, ValueError):
            return Response({"error": "날짜 형식이 올바르지 않습니다."}, status=400)

        events = CalendarEvent.objects.filter(start__date=date)
        serializer = CalendarEventSerializer(events, many=True)
        return Response(serializer.data)