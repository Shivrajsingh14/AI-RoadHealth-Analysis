from django.db import models
from django.contrib.auth.models import User


class Assessment(models.Model):
    SEVERITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('analyzing', 'Analyzing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="uploads/")
    crack_percentage = models.FloatField(null=True, blank=True)
    pothole_probability = models.FloatField(null=True, blank=True)
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES, null=True, blank=True)
    condition_score = models.IntegerField(null=True, blank=True)
    analysis_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Assessment {self.id} by {self.user.username} - {self.analysis_status}"
    
    @property
    def condition_description(self):
        """Return a human-readable condition description based on score"""
        if self.condition_score is None:
            return "Not analyzed"
        elif self.condition_score >= 80:
            return "Excellent"
        elif self.condition_score >= 60:
            return "Good"
        elif self.condition_score >= 40:
            return "Fair"
        elif self.condition_score >= 20:
            return "Poor"
        else:
            return "Very Poor"
