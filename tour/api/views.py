from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from tour.models import Tour, Destination, Category, Activity
from .serializers import (
    TourSerializer, DestinationSerializer, CategorySerializer, 
    ActivitySerializer
)


class TourViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for viewing Tours."""
    queryset = Tour.objects.filter(is_active=True)
    serializer_class = TourSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'slug'


class DestinationViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for viewing Destinations."""
    queryset = Destination.objects.filter(is_active=True)
    serializer_class = DestinationSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'slug'


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for viewing Tour Categories."""
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'slug'


class ActivityViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for viewing Tour Activities."""
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    permission_classes = [permissions.AllowAny]