from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User as AuthUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import date, timedelta

class UserProfile(models.Model):
    user = models.OneToOneField(AuthUser, on_delete=models.CASCADE)
    income = models.DecimalField(max_digits=10, decimal_places=2)
    credit_score = models.IntegerField()

class Loan(models.Model):
    user = models.ForeignKey(AuthUser, on_delete=models.CASCADE)
    loan_type = models.CharField(max_length=20, choices=[('Car', 'Car'), ('Home', 'Home'), ('Education', 'Education'), ('Personal', 'Personal')])
    loan_amount = models.DecimalField(max_digits=10, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    term_period = models.IntegerField()
    disbursement_date = models.DateField()
    emi_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=10, default='PENDING')

    def next_emi_due_date(self):
        # Calculate the next EMI due date (1st of the month)
        next_due_date = self.disbursement_date + timedelta(days=30)
        return next_due_date

class Transaction(models.Model):
    user = models.ForeignKey(AuthUser, on_delete=models.CASCADE)
    date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    TRANSACTION_CHOICES = [
        ('DEBIT', 'Debit'),
        ('CREDIT', 'Credit'),
    ]
    transaction_type = models.CharField(max_length=6, choices=TRANSACTION_CHOICES)

@receiver(post_save, sender=AuthUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=AuthUser)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()