from django.db import models


class CurriculumPlan(models.Model):
    topic = models.CharField(max_length=255)
    timeframe = models.PositiveIntegerField()
    level = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self) -> str:
        return f"{self.topic} ({self.level}) - {self.timeframe} weeks"
