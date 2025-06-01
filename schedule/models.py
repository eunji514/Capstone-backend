from django.db import models

class CalendarEvent(models.Model):

    post = models.OneToOneField('board.BoardPost', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    start = models.DateTimeField()
    end = models.DateTimeField()
    student_council = models.ForeignKey('schedule.StudentCouncil', on_delete=models.CASCADE)  

    def __str__(self):
        return f"{self.title} : {self.start} - {self.end}"

class StudentCouncil(models.Model):
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=7)  # ex: "#FF5733"

    def __str__(self):
        return self.name
