from django.shortcuts import render

from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator
from .choices import bedroom_choices,state_choices,price_choices
from django.shortcuts import get_object_or_404

from .models import Listing

def index(request):
    #getting the data from database
    # getting the object or data and displaying it in tje form of latest addded listing first 
    # and also filtering the object by is published means is is published is true listing will display otherwise not
    listings = Listing.objects.order_by('-list_date').filter(is_published=True)

    paginator = Paginator(listings, 6)
    page = request.GET.get('page')
    paged_listings = paginator.get_page(page)

    context = {
        'listings' : paged_listings
    }

    return render(request,'listings/listings.html',context)

def listing(request, listing_id):
    # check to see that whether the listing page exist or not if not it will return 404 error
    listing = get_object_or_404(Listing, pk=listing_id)

    context = {
        'listing' : listing
    }

    return render(request,'listings/listing.html', context)

def search(request):
    queryset_list = Listing.objects.order_by('-list_date')

    # Search by keywords
    if 'keywords' in request.GET:
        keywords = request.GET['keywords']
        if keywords:
            #check whether the description contains the searched keyword
            queryset_list = queryset_list.filter(description__icontains=keywords)


    # Search by city
    if 'city' in request.GET:
        city = request.GET['city']
        if city:
            #check whether the database contains the searched city
            queryset_list = queryset_list.filter(city__iexact=city)
    
    # Search by state
    if 'state' in request.GET:
        state = request.GET['state']
        if state:
            #check whether the database contains the searched state
            queryset_list = queryset_list.filter(state__iexact=state)

    # Search by bedrooms
    if 'bedrooms' in request.GET:
        bedrooms = request.GET['bedrooms']
        if bedrooms:
            #check whether the database contains the searched bedrooms
            queryset_list = queryset_list.filter(bedrooms__lte=bedrooms)
    
    # Search by price
    if 'price' in request.GET:
        price = request.GET['price']
        if price:
            #check whether the database contains the searched price
            queryset_list = queryset_list.filter(price__lte=price)
    
    

    context = {
        'bedroom_choices' : bedroom_choices,
        'state_choices' : state_choices,
        'price_choices' : price_choices,
        'listings' : queryset_list,
        'values' : request.GET,
    }

    return render(request,'listings/search.html', context)


