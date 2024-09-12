from django.shortcuts import render, redirect, get_object_or_404 # type: ignore
from django.urls import reverse # type: ignore
from .forms import SaleForm, AddStockForm, ProcurementForm, CreditSaleForm
from .filters import StockxFilter
from .models import stockx, Sale, Product, CreditSale
from django.contrib.auth.decorators import login_required # type: ignore
from django.contrib.auth import authenticate, login as auth_login, logout # type: ignore
from django.contrib.auth.forms import AuthenticationForm # type: ignore
from django.db.models import Sum # type: ignore
from .models import CreditSale
from django.views import View # type: ignore



# Login view - No login_required decorator
def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('home')  # Redirect to dashboard after login
    else:
        form = AuthenticationForm()
    
    return render(request, 'groceryapp/login.html', {'form': form})

def index(request):
    return render(request, 'groceryapp/index.html')

@login_required
def home(request):
    products = stockx.objects.all().order_by('-id')
    product_filters = StockxFilter(request.GET, queryset=products)
    products = product_filters.qs
    return render(request, 'groceryapp/home.html', {'products': products, 'product_filters': product_filters})

@login_required
@login_required
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'groceryapp/product_detail.html', {'product': product})

    # if request.method == 'POST':
    #     form = AddStockForm(request.POST, instance=product)
    #     if form.is_valid():
    #         updated_product = form.save(commit=False)
    #         updated_product.total_quantity += form.cleaned_data['total_quantity']  
    #         updated_product.save()
    #         return redirect('Astock')
    # else:
    #     form = AddStockForm()
    # return render(request, 'groceryapp/product_detail.html', {'product': product})

@login_required
def issue_item(request, pk):
    issue_item = get_object_or_404(stockx, id=pk)
    sales_form = SaleForm(request.POST or None)

    if request.method == 'POST':
        if sales_form.is_valid():
            new_sale = sales_form.save(commit=False)
            new_sale.item = issue_item
            new_sale.unitcost = issue_item.unit_cost
            new_sale.save()

            issue_quantity = sales_form.cleaned_data['quantity']
            if issue_item.total_quantity >= issue_quantity:
                issue_item.total_quantity -= issue_quantity
                issue_item.save()
            else:
                # Handle case when there's not enough stock
                return render(request, 'groceryapp/issue_item.html', {
                    'sales_form': sales_form,
                    'error': 'Not enough stock available'
                })

            return redirect('receipt')
    
    return render(request, 'groceryapp/issue_item.html', {'sales_form': sales_form})



@login_required
def receipt(request):
    sales = Sale.objects.all().order_by('-id')
    return render(request, 'groceryapp/receipt.html', {'sales': sales})

@login_required
def receipt_detail(request, receipt_id):
    receipt = get_object_or_404(Sale, id=receipt_id)
    return render(request, 'groceryapp/receipt_detail.html', {'receipt': receipt})

@login_required
def user_logout(request):
    logout(request)  # Call the Django logout function
    return render(request, 'groceryapp/logout.html')




@login_required
def total_stock_view(request):
    total_stock = Product.objects.aggregate(total_quantity=Sum('quantity_in_stock'))['total_quantity']
    return render(request, 'groceryapp/total_stock.html', {'total_stock': total_stock})

@login_required
def creditsale(request):
    if request.method == 'POST':
        form = CreditSaleForm(request.POST)
        if form.is_valid():
            form.save()  # Save the form data to the database
            return redirect('success')  # Redirect to success view
    else:
        form = CreditSaleForm()
    
    return render(request, 'groceryapp/creditsale.html', {'form': form})

@login_required
def credit_sales_list(request):
    credit_sales = CreditSale.objects.all()
    return render(request, 'groceryapp/credit_sales_list.html', {'credit_sales': credit_sales})


def success(request):
    credit_sales = CreditSale.objects.all()  # Retrieve all credit sales from the database
    return render(request, 'groceryapp/success.html', {'credit_sales': credit_sales})

def delete_receipt(request, id):
    sale = get_object_or_404(Sale, id=id)
    sale.delete()
    return redirect('receipt') 




@login_required
def Addstock(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        quantity_to_add = int(request.POST.get('quantity', 0))
        if quantity_to_add > 0:
            product.total_quantity += quantity_to_add  # Add to the existing total
            product.save()
            return redirect('product_detail', product_id=product_id)
    else:
        form = AddStockForm(initial={'quantity': 1})  # Initialize with a default value for quantity
    
    return render(request, 'groceryapp/Addstock.html', {'product': product, 'form': form})




# def Astock(request, product_id):
#     product = get_object_or_404(Product, id=product_id)
#     if request.method == 'POST':
#         add_quantity = int(request.POST.get('add_quantity', 0))
#         product.total_quantity += add_quantity
#         product.save()
#         return redirect('product_detail', product_id=product_id) 
    
#     return render(request, 'groceryapp/Astock.html', {'product': product})


@login_required
def total_sales_view(request):
    total_sales = Sale.objects.aggregate(total_amount=Sum('amount_received'))['total_amount']
    total_change = Sale.objects.aggregate(total_change=Sum('amount_received') - Sum('quantity') * Sum('item__unit_price'))['total_change']
    
    return render(request, 'groceryapp/total_sales.html', {
        'total_sales': total_sales,
        'total_change': total_change,
    })

class CreditSaleListView(View):
    def get(self, request):
        branches = Branch.objects.all()
        sales_by_branch = {branch: CreditSale.objects.filter(branch=branch) for branch in branches}
        return render(request, 'credit_sale_list.html', {'sales_by_branch': sales_by_branch})



