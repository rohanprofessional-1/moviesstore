from django.shortcuts import render

# Create your views here.
from django.shortcuts import get_object_or_404, redirect
from movies.models import Movie
from .utils import calculate_cart_total
from .models import Order, Item
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import UserFeedback

def index(request):
    cart_total = 0
    movies_in_cart = []
    cart = request.session.get('cart', {})
    movie_ids = list(cart.keys())
    if (movie_ids != []):
        movies_in_cart = Movie.objects.filter(id__in=movie_ids)
        cart_total = calculate_cart_total(cart,
            movies_in_cart)
    template_data = {}
    template_data['title'] = 'Cart'
    template_data['movies_in_cart'] = movies_in_cart
    template_data['cart_total'] = cart_total
    return render(request, 'cart/index.html',
        {'template_data': template_data})
def add(request, id):
    get_object_or_404(Movie, id=id)
    cart = request.session.get('cart', {})
    cart[id] = request.POST['quantity']
    request.session['cart'] = cart
    return redirect('home.index')
def add_to_cart(request, id):
    get_object_or_404(Movie, id=id)
    cart = request.session.get('cart', {})
    cart[id] = request.POST['quantity']
    request.session['cart'] = cart
    return redirect('cart:index')
def clear(request):
    request.session['cart'] = {}
    return redirect('cart:index')

@login_required
def purchase(request):
    cart = request.session.get('cart', {})
    movie_ids = list(cart.keys())
    if (movie_ids == []):
        return redirect('cart:index')
    movies_in_cart = Movie.objects.filter(id__in=movie_ids)
    cart_total = calculate_cart_total(cart, movies_in_cart)
    order = Order()
    order.user = request.user
    order.total = cart_total
    order.save()
    for movie in movies_in_cart:
        item = Item()
        item.movie = movie
        item.price = movie.price
        item.order = order
        item.quantity = cart[str(movie.id)]
        item.save()
    request.session['cart'] = {}
    template_data = {}
    template_data['title'] = 'Purchase confirmation'
    template_data['order_id'] = order.id
    # Redirect to a new view that displays the feedback modal
    return redirect('cart.feedback_prompt', order_id=order.id)

@login_required
def feedback_prompt(request, order_id):
    template_data = {}
    template_data['title'] = 'Provide Feedback'
    template_data['order_id'] = order_id
    return render(request, 'cart/feedback_modal.html', {'template_data': template_data})

@login_required
def submit_feedback(request, order_id):
    if request.method == 'POST':
        user_name = request.POST.get('userName')
        user_experience = request.POST.get('userExperience')
        UserFeedback.objects.create(user_name=user_name, experience=user_experience)
        return redirect('cart.purchase_complete', order_id=order_id) # Redirect to the purchase complete page
    return redirect('cart.feedback_prompt', order_id=order_id)

def purchase_complete(request, order_id):
    template_data = {}
    template_data['title'] = 'Purchase Completed'
    template_data['order_id'] = order_id
    return render(request, 'cart/purchase.html', {'template_data': template_data})

@login_required
def view_feedback(request):
    feedbacks = UserFeedback.objects.all().order_by('-created_at')
    template_data = {
        'title': 'User Feedback',
        'feedbacks': feedbacks
    }
    return render(request, 'cart/view_feedback.html', {'template_data': template_data})