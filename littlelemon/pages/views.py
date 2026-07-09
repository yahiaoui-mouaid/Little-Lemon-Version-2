from django.shortcuts import render



def home_page(request):
    return render(request, 'home.html', {})


def signup_page(request):
    # This grabs the HTML file and sends it to the user's screen
    return render(request, 'signup.html')


def login_page(request): 
    return render(request, 'login.html')


def logout_page(request):
    return render(request, 'logout.html')


def about_page(request):
    return render(request, 'about.html')


def book_table_page(request):
    return render(request, 'book_table.html')


def menu_page(request):
    return render(request, 'menu.html')


def menu_item_page(request, pk):
    return render(request, 'menu_item.html')


def menu_item_create(request):
    return render(request, 'create_menu_item.html')


def create_category(request):
    return render(request, 'create_category.html')


def members_page(request):
    return render(request, 'members.html')


def order_confirmation_page(request):
    return render(request, 'order_confirmation.html')


def myorders_page(request):
    return render(request, 'myorders.html')


def dashboard_page(request):
    return render(request, 'dashboard.html')





