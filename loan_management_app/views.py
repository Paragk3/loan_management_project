from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Loan, Transaction
from .serializers import LoanApplicationSerializer
from .utils import calculate_emi_schedule
from datetime import date

class MakePaymentAPIView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            loan_id = request.data.get('Loan_id')
            amount_paid = request.data.get('Amount')

            loan = Loan.objects.get(id=loan_id)
            if loan.status == 'CLOSED':
                return Response({"error": "Loan is already closed."}, status=status.HTTP_400_BAD_REQUEST)

            today = date.today()
            next_emi_due_date = loan.next_emi_due_date()
            if today != next_emi_due_date:
                return Response({"error": "Payment can only be made on the 1st of every month."}, status=status.HTTP_400_BAD_REQUEST)

            if amount_paid != loan.emi_amount:
                loan.emi_amount = amount_paid
                loan.save()

            Transaction.objects.create(
                user=loan.user,
                date=today,
                amount=amount_paid,
                transaction_type='CREDIT'
            )

            return Response({"message": "Payment registered successfully"}, status=status.HTTP_200_OK)

        except Loan.DoesNotExist:
            return Response({"error": "Loan with this Loan_id does not exist."}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class GetStatementAPIView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            loan_id = request.query_params.get('Loan_id')

            loan = Loan.objects.get(id=loan_id)
            if loan.status == 'CLOSED':
                return Response({"error": "Loan is already closed."}, status=status.HTTP_400_BAD_REQUEST)

            emi_schedule = calculate_emi_schedule(loan.loan_amount, loan.interest_rate, loan.term_period, loan.disbursement_date)
            past_transactions = Transaction.objects.filter(user=loan.user, date__lt=date.today())

            response_data = {
                "error": None,
                "Past_transactions": [],
                "Upcoming_transactions": emi_schedule
            }

            for transaction in past_transactions:
                response_data["Past_transactions"].append({
                    "Date": transaction.date.strftime("%Y-%m-%d"),
                    "Principal": None,
                    "Interest": None,
                    "Amount_paid": transaction.amount,
                })

            return Response(response_data, status=status.HTTP_200_OK)

        except Loan.DoesNotExist:
            return Response({"error": "Loan with this Loan_id does not exist."}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)