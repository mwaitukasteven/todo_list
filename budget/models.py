from django.db import models
from django.contrib.auth.models import User

class Income(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.IntegerField()  # Changed to IntegerField
    description = models.CharField(max_length=255, default='no description provided')
    date_added = models.DateTimeField(auto_now_add=True, null=True)
    date = models.DateField(null=True, blank=True)

    def __str__(self):
        display_date = self.date.strftime('%Y-%m-%d') if self.date else self.date_added.strftime('%Y-%m-%d')
        return f"{self.user.username} - {self.amount} - {display_date}"

    class Meta:
        ordering = ['-date_added']
        verbose_name_plural = "Incomes"

class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.IntegerField()  # Changed to IntegerField
    description = models.CharField(max_length=255, default='no description provided')
    date_added = models.DateTimeField(auto_now_add=True, null=True)
    date = models.DateField(null=True, blank=True)

    def __str__(self):
        display_date = self.date.strftime('%Y-%m-%d') if self.date else self.date_added.strftime('%Y-%m-%d')
        return f"{self.user.username} - {self.amount} - {display_date}"

    class Meta:
        ordering = ['-date_added']
        verbose_name_plural = "Expenses"
