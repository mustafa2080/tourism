from rest_framework import viewsets, permissions
from payments.models import Payment
from .serializers import PaymentSerializer

class PaymentViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows payments to be viewed.
    (Typically payments are created via gateway interactions, not direct API POST)
    """
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAdminUser] # Or custom permission for user to view own payments

    # Add filtering to show only payments related to the requesting user if needed
    # def get_queryset(self):
    #     user = self.request.user
    #     if user.is_staff:
    #         return Payment.objects.all()
    #     return Payment.objects.filter(booking__user=user)
