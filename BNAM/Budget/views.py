from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, generics
from .models import Budget
from .serializers import BudgetSerializer

class BudgetCreateAPIView(generics.CreateAPIView):
    queryset = Budget.objects.all()
    serializer_class = BudgetSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    

class GetBugetAPIView(APIView):
    def retrieve(self, request, budget_id):
        try:
            budget = Budget.objects.get(budget_id=budget_id)
        except Budget.DoesNotExist:
            return Response({'error': 'Budget Not Found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = BudgetSerializer(budget)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def get_list(self, request):
        budgets = Budget.objects.all()
        serializer = BudgetSerializer(budgets, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def get(self, request, budget_id=None):
        if budget_id is not None:
            return self.retrieve(request, budget_id)
        else:
            return self.get_list(request)