from django.shortcuts import render, redirect

from product.models import Product, Payment
from users.models import User


# Create your views here.
def read_all_products(request):
    if not request.session.get('user'):
        return redirect('login')
    else:
        try:
            id = request.session.get('user')
            technicien = User.objects.get(id=id)
            one_product = Product.objects.all().order_by('-id')[:1]
            if technicien.role == 'admin':
                return redirect('dashboard')
            elif technicien.role == 'technicien':
                products = Product.objects.filter(technicien=technicien)
                context = {'admin': technicien, 'products': products, 'one_product': one_product}
                return render(request, 'technicien/product-list.html', context, status=200)
            else:
                products = Product.objects.all()
                context = {'admin': technicien, 'products': products, 'one_product': one_product}
                return render(request, 'fournisseur/shop-list.html', context, status=200)
        except User.DoesNotExist:
            return render(request, 'technicien/product-list.html')


def read_four_products(request):
    products = Product.objects.all().order_by('-id')[:4]
    one_product = Product.objects.all().order_by('-id')[:1]
    context = {'products': products, 'one_product': one_product}
    return render(request, 'home/shop.html', context, status=200)


def read_one_products(request, id):
    if not request.session.get('user'):
        if id:
            product = Product.objects.get(id=id)
            products = Product.objects.all().order_by('-id')[:4]
            context = {'one_product': product, 'products': products}
            return render(request, 'home/shop.html', context, status=200)
        else:
            product = Product.objects.all().order_by('-id')[:1]
            products = Product.objects.all().order_by('-id')[:4]
            context = {'one_product': product, 'products': products}
            return render(request, 'home/shop.html', context, status=200)
    else:
        user_id = request.session.get('user')
        technicien = User.objects.get(id=user_id)
        product = Product.objects.get(id=id)
        context = {'admin': technicien, 'product': product}
        if technicien.role == 'technicien':
            return render(request, 'technicien/edit_product.html', context, status=200)
        else:
            return redirect('dashboard')


def show_story(request):
    if not request.session.get('user'):
        return redirect('login')
    else:
        id = request.session.get('user')
        user = User.objects.get(id=id)
        if user.role == 'fournisseur':
            products = Product.objects.all().order_by('-id')
            payment = Payment.objects.all().order_by('-id').exclude(is_accepted=True)
            context = {'admin': user, 'products': products, 'payment': payment}
            return render(request, 'fournisseur/historique.html', context, status=200)
        elif user.role == 'technicien':
            products = Product.objects.all().order_by('-id')
            payment = Payment.objects.all().order_by('-id').exclude(is_accepted=True)
            context = {'admin': user, 'products': products, 'payment': payment}
            return render(request, 'technicien/historique.html', context, status=200)
        else:
            return redirect('dashboard')


def commander_products(request):
    if not request.session.get('user'):
        return redirect('login')
    else:
        id = request.session.get('user')
        fornisseur = User.objects.get(id=id)
        if fornisseur.role == 'fournisseur':
            if request.method == 'POST':
                prod_id = request.POST.get('prod_id')
                product = Product.objects.get(id=prod_id)
                reference = request.POST.get('reference')
                date = request.POST.get('date')
                nom_compte = request.POST.get('nom_compte')
                payment = Payment(product=product, user=fornisseur, reference=reference, date_envoyer=date,
                                  nom_compte=nom_compte)
                payment.save()
                return redirect('dashboard')
            else:
                return redirect('show_story')
        return redirect('dashboard')


def accept_payment(request, id):
    if not request.session.get('user'):
        return redirect('login')
    else:
        user_id = request.session.get('user')
        user = User.objects.get(id=user_id)
        if user.role == 'technicien':
            payment = Payment.objects.get(pk=id)
            payment.is_accepted = True
            payment.save()
            return redirect('show_story')
        else:
            return redirect('dashboard')


def createProduct(request):
    if not request.session.get('user'):
        return redirect('login')
    else:
        id = request.session.get('user')
        user = User.objects.get(pk=id)
        if user.role == 'technicien':
            if request.method == "POST":
                name = request.POST.get('name')
                price = request.POST.get('price')
                description = request.POST.get('description')
                if len(request.FILES) != 0:
                    image = request.FILES.get('image')
                    product = Product(name=name, price=price, description=description, image=image, technicien=user)
                    product.save()
                    return redirect('list_product')
                else:
                    return redirect('dashboard')
        else:
            return redirect('dashboard')


def editProduct(request, id):
    if not request.session.get('user'):
        return redirect('login')
    else:
        product = Product.objects.get(pk=id)
        if request.method == "POST":
            name = request.POST.get('name')
            price = request.POST.get('price')
            description = request.POST.get('description')
            if len(request.FILES) != 0:
                image = request.FILES.get('image')
                product.name = name
                product.price = price
                product.description = description
                product.image = image
                product.save()
                return redirect('list_product')
            else:
                image = request.FILES.get('image')
                product.name = name
                product.price = price
                product.description = description
                product.save()
                return redirect('list_product')


def deleteProduct(request, id):
    if not request.session.get('user'):
        return redirect('login')
    else:
        product = Product.objects.get(pk=id)
        product.delete()
        return redirect('list_product')
