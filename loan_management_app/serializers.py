from rest_framework import serializers
from .models import Loan

class LoanApplicationSerializer(serializers.Serializer):
    unique_user_id = serializers.UUIDField()
    loan_type = serializers.ChoiceField(choices=[('Car', 'Car'), ('Home', 'Home'), ('Education', 'Education'), ('Personal', 'Personal')])
    loan_amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    interest_rate = serializers.DecimalField(max_digits=5, decimal_places=2)
    term_period = serializers.IntegerField()
    disbursement_date = serializers.DateField()