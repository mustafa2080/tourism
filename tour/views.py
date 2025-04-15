from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
import json # Import json
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.db.models import Q, Avg, F, Count # Import Count
from django.urls import reverse_lazy
from users.models import WishlistItem # Import WishlistItem

from .models import (
    Destination, Category, Tour, Promotion
)
from reviews.models import Review
from .forms import TourSearchForm
from reviews.forms import ReviewForm # Import ReviewForm from reviews app

# Constants
TOURS_PER_PAGE = 9


class TourListView(ListView):
    """View to display all tours"""
    model = Tour
    template_name = 'tour/tour_list.html'
    context_object_name = 'tours'
    paginate_by = TOURS_PER_PAGE
    
    def get_queryset(self):
        queryset = Tour.objects.filter(is_active=True)
        
        # Apply filters if provided
        filters = {}
        
        # Destination filter
        destination = self.request.GET.get('destination')
        if destination:
            filters['destination__slug'] = destination
        
        # Category filter
        category = self.request.GET.get('category')
        if category:
            filters['categories__slug'] = category
        
        # Price range filter
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')
        if min_price:
            filters['price__gte'] = min_price
        if max_price:
            filters['price__lte'] = max_price
        
        # Duration filter
        duration = self.request.GET.get('duration')
        if duration:
            filters['duration_days__lte'] = duration
        
        # Apply filters
        if filters:
            queryset = queryset.filter(**filters).distinct()
        
        # Sorting
        sort_by = self.request.GET.get('sort', 'created_at')
        if sort_by == 'price_low':
            queryset = queryset.order_by('price')
        elif sort_by == 'price_high':
            queryset = queryset.order_by('-price')
        elif sort_by == 'name':
            queryset = queryset.order_by('name')
        elif sort_by == 'popularity':
            # Corrected related name for reviews
            queryset = queryset.annotate(avg_rating=Avg('tour_reviews__rating')).order_by('-avg_rating')
        else:
            queryset = queryset.order_by('-created_at')
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['destinations'] = Destination.objects.filter(is_active=True)
        context['categories'] = Category.objects.filter(is_active=True)
        
        # Add filter parameters to context for the template
        context['selected_destination'] = self.request.GET.get('destination', '')
        context['selected_category'] = self.request.GET.get('category', '')
        context['selected_min_price'] = self.request.GET.get('min_price', '')
        context['selected_max_price'] = self.request.GET.get('max_price', '')
        context['selected_duration'] = self.request.GET.get('duration', '')
        context['selected_sort'] = self.request.GET.get('sort', 'created_at')
        
        return context


class TourDetailView(DetailView):
    """View to display details of a specific tour"""
    model = Tour
    template_name = 'tour/tour_detail.html'
    context_object_name = 'tour'
    
    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        # Increment view count
        self.object.increment_view_count()
        return response
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tour = self.get_object()
        
        # Get related tours (same destination or categories)
        related_tours = Tour.objects.filter(
            Q(destination=tour.destination) | Q(categories__in=tour.categories.all())
        ).exclude(id=tour.id).distinct()[:3]
        
        # Get tour reviews - Corrected related name
        reviews = tour.tour_reviews.filter(is_approved=True).order_by('-created_at')
        
        # Get tour dates
        tour_dates = tour.dates.filter(is_active=True, available_seats__gt=0).order_by('start_date')
        
        # Check if user has already reviewed this tour - Corrected related name
        user_reviewed = False
        # Check if the tour is in the user's wishlist
        is_in_wishlist = False
        if self.request.user.is_authenticated:
            user_reviewed = tour.tour_reviews.filter(user=self.request.user).exists()
            is_in_wishlist = WishlistItem.objects.filter(user=self.request.user, tour=tour).exists()
        
        # Add to context
        context['related_tours'] = related_tours
        context['reviews'] = reviews
        context['tour_dates'] = tour_dates
        context['user_reviewed'] = user_reviewed
        context['is_in_wishlist'] = is_in_wishlist # Add wishlist status to context
        context['review_form'] = ReviewForm() # Use ReviewForm from reviews.forms

        # Calculate rating percentages
        total_reviews = reviews.count()
        rating_counts = reviews.values('rating').annotate(count=Count('id')).order_by('-rating')
        
        rating_percentages_dict = {i: 0 for i in range(1, 6)}
        if total_reviews > 0:
            for item in rating_counts:
                rating = item['rating']
                count = item['count']
                rating_percentages_dict[rating] = round((count / total_reviews) * 100)
        
        # Convert to list of tuples for easier template iteration [(5, perc), (4, perc), ...]
        context['rating_percentages'] = sorted(rating_percentages_dict.items(), reverse=True)
        
        # Calculate average rating (can also be done via model method)
        context['avg_rating'] = tour.get_average_rating() # Use model method if available

        # Prepare available dates for Flatpickr
        available_dates_list = []
        for date_obj in tour_dates:
            available_dates_list.append({
                'id': date_obj.id,
                'date': date_obj.start_date.strftime('%Y-%m-%d'), # Format needed by flatpickr
                'display': date_obj.start_date.strftime('%d %b %Y'), # Optional display format
                'seats': date_obj.available_seats
            })
        context['available_dates_json'] = json.dumps(available_dates_list)


        return context


class DestinationListView(ListView):
    """View to display all destinations"""
    model = Destination
    template_name = 'tour/destination_list.html'
    context_object_name = 'destinations'
    paginate_by = TOURS_PER_PAGE
    queryset = Destination.objects.filter(is_active=True)


class DestinationDetailView(DetailView):
    """View to display details of a specific destination"""
    model = Destination
    template_name = 'tour/destination_detail.html'
    context_object_name = 'destination'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        destination = self.get_object()
        
        # Get tours for this destination
        tours = destination.tours.filter(is_active=True)
        
        # Get categories for filter
        categories = Category.objects.filter(tours__destination=destination).distinct()
        
        # Add to context
        context['tours'] = tours
        context['categories'] = categories
        
        return context


class CategoryListView(ListView):
    """View to display all categories"""
    model = Category
    template_name = 'tour/category_list.html'
    context_object_name = 'categories'
    queryset = Category.objects.filter(is_active=True)


class CategoryDetailView(DetailView):
    """View to display details of a specific category"""
    model = Category
    template_name = 'tour/category_detail.html'
    context_object_name = 'category'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.get_object()
        
        # Get tours in this category
        tours = category.tours.filter(is_active=True)
        
        # Get destinations for filter
        destinations = Destination.objects.filter(tours__categories=category).distinct()
        
        # Add to context
        context['tours'] = tours
        context['destinations'] = destinations
        
        return context


# Add this to your existing imports if not already there
from django.views.generic import ListView
from django.db.models import Q
from .forms import TourSearchForm

# Add this class to your views.py file
class TourSearchView(ListView):
    """View for searching tours"""
    model = Tour
    template_name = 'tour/tour_search.html'
    context_object_name = 'tours'
    paginate_by = 9  # Adjust as needed
    
    def get_queryset(self):
        queryset = Tour.objects.filter(is_active=True)
        
        # Get the keyword from the request
        keyword = self.request.GET.get('keyword', '')
        
        # If keyword exists, filter the queryset
        if keyword:
            queryset = queryset.filter(
                Q(name__icontains=keyword) |
                Q(description__icontains=keyword) |
                Q(short_description__icontains=keyword) |
                Q(destination__name__icontains=keyword) |
                Q(destination__country__icontains=keyword) |
                Q(destination__city__icontains=keyword)
            )
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add the search keyword to the context
        context['search_keyword'] = self.request.GET.get('keyword', '')
        return context


class TourFilterView(TemplateView):
    """View to filter tours with AJAX"""
    template_name = 'tour/tour_filter.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get filters
        destination_slug = self.request.GET.get('destination')
        category_slug = self.request.GET.get('category')
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')
        duration = self.request.GET.get('duration')
        sort_by = self.request.GET.get('sort', 'created_at')
        
        # Start with all active tours
        tours = Tour.objects.filter(is_active=True)
        
        # Apply filters
        if destination_slug:
            tours = tours.filter(destination__slug=destination_slug)
        
        if category_slug:
            tours = tours.filter(categories__slug=category_slug)
        
        if min_price:
            tours = tours.filter(price__gte=min_price)
        
        if max_price:
            tours = tours.filter(price__lte=max_price)
        
        if duration:
            tours = tours.filter(duration_days__lte=duration)
        
        # Apply sorting
        if sort_by == 'price_low':
            tours = tours.order_by('price')
        elif sort_by == 'price_high':
            tours = tours.order_by('-price')
        elif sort_by == 'name':
            tours = tours.order_by('name')
        elif sort_by == 'popularity':
            # Corrected related name for reviews
            tours = tours.annotate(avg_rating=Avg('tour_reviews__rating')).order_by('-avg_rating')
        else:
            tours = tours.order_by('-created_at')
        
        context['tours'] = tours.distinct()
        return context


class FeaturedToursView(ListView):
    """View to display featured tours"""
    model = Tour
    template_name = 'tour/featured_tours.html'
    context_object_name = 'tours'
    paginate_by = TOURS_PER_PAGE
    queryset = Tour.objects.filter(is_active=True, is_featured=True)


class PromotionsView(ListView):
    """View to display current promotions"""
    model = Promotion
    template_name = 'tour/promotions.html'
    context_object_name = 'promotions'
    
    def get_queryset(self):
        from django.utils import timezone
        today = timezone.now().date()
        return Promotion.objects.filter(
            is_active=True,
            start_date__lte=today,
            end_date__gte=today
        )
