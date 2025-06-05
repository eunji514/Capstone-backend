from django.db import models

class CalendarEvent(models.Model):
    post = models.OneToOneField('board.BoardPost', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    start = models.DateTimeField()
    end = models.DateTimeField()

    def __str__(self):
        return f"{self.title} : {self.start} - {self.end}"