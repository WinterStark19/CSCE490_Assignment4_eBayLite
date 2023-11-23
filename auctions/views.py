from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required


from .models import User, Auction, Category, Comment, Bid


def index(request):
    active = Auction.objects.filter(closed=False)
    allSorted = Category.objects.all()
    return render(request, "auctions/index.html", {
        "listings": active,
        "categories":allSorted
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
    

@login_required(login_url = "login")    
def create(request):
    if request.method == 'POST':
        title = request.POST["title"]
        description = request.POST["description"]
        price = request.POST["price"]
        imageurl = request.POST["imageurl"]
        category = request.POST["category"]
        seller = request.user

        categoryInfo = Category.objects.get(title = category)

        newListing = Auction(
            title = title,
            description = description,
            price = price,
            imageUrl = imageurl,
            category = categoryInfo,
            seller = seller
            )
        newListing.save()

        return HttpResponseRedirect(reverse(index))
    else:
        allCategories = Category.objects.all()
        return render(request, "auctions/create.html", {
            "categories": allCategories
        })

def showCategory(request):
    if request.method == "POST":
        getCategory = request.POST['category']
        newCategory = Category.objects.get(title = getCategory)
        active = Auction.objects.filter(closed=False, category = newCategory)
        allSorted = Category.objects.all()
        return render(request, "auctions/index.html", {
            "listings": active,
            "categories": allSorted
        })


def listings(request, id):
 listingData = Auction.objects.get(pk=id)
 isListingInWatchList = request.user in listingData.watchlist.all()
 comments = Comment.objects.filter(listing=listingData)
 isSeller = request.user.username == listingData.seller.username
 return render(request, "auctions/listing.html", {
        "listing": listingData,
        "isListingInWatchList" : isListingInWatchList,
        "comments": comments,
        "isSeller": isSeller
    })

def addBid(request, id):
    newBid = request.POST['newBid']
    listingData = Auction.objects.get(pk=id)
    isListingInWatchList = request.user in listingData.watchlist.all()
    comments = Comment.objects.filter(listing=listingData)
    isSeller = request.user.username == listingData.seller.username
    if float(newBid) > float(listingData.price.bid):
        updateBid = Bid(user=request.user, bid=float(newBid))
        updateBid.save()
        listingData.price = updateBid
        listingData.save()
        return render(request, "auctions/listing.html", {
            "listing": listingData,
            "message": "Successful bid",
            "update": True,
            "isListingInWatchList" : isListingInWatchList,
            "comments": comments,
            "isSeller": isSeller, 
        })
    else:
        return render(request, "auctions/listing.html", {
            "listing": listingData,
            "message": "Unsuccessful bid",
            "update": False,
            "isListingInWatchList" : isListingInWatchList,
            "comments": comments,
            "isSeller": isSeller, 
        })
    
def displayWatchList(request):
    currentUser = request.user
    listings = currentUser.WatchList.all()
    print(listings)
    return render(request, "auctions/watchlist.html", {
        "listings": listings
    })

def removeWatchList(request, id):
    listingData = Auction.objects.get(pk=id)
    currentUser = request.user
    listingData.watchlist.remove(currentUser)
    return HttpResponseRedirect(reverse("listing", args=(id, )))

def addWatchList(request, id):
    listingData = Auction.objects.get(pk=id)
    currentUser = request.user
    listingData.watchlist.add(currentUser)
    return HttpResponseRedirect(reverse("listing", args=(id, )))    

def closeAuction(request, id):
    listingData = Auction.objects.get(pk=id)
    listingData.isActive = False
    listingData.save()
    isListingInWatchList = request.user in listingData.watchlist.all()
    comments = Comment.objects.filter(listing=listingData)
    isSeller = request.user.username == listingData.seller.username
    return render(request, "auctions/listing.html", {
        "listing": listingData,
        "isListingInWatchList" : isListingInWatchList,
        "comments": comments,
        "isSeller": isSeller, 
        "update": True,
        "message": "Auction closed"
    })

def categories(request):
    categories = Category.objects.values_list('title', flat=True).distinct()
    categories = list(categories)

    return render(request, "auctions/categories.html", {
        "categories": categories
    })

def categoryList(request, category):
    listings = Auction.objects.filter(category=category)

    return render(request, "auctions/categoryList.html", {
        "category": category,
        "listings": listings
    })

def addComment(request, id):
    currentUser = request.user
    listingData = Auction.objects.get(pk=id)
    message = request.POST['comment']
    newComment = Comment(
        author=currentUser,
        listing=listingData,
        message=message
    )
    newComment.save()
    return HttpResponseRedirect(reverse("listing", args=(id, )))