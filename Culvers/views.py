from django.shortcuts import render
from django.views import View
from .models import MenuItem, Category, Order

# Create your views here.
class Index(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'Culvers/index.html')




class Order(View):
    def get(self, request, *args, **kwargs):
        
        #get item from each category
        BUTTERBURGERS = MenuItem.objects.filter(category__name__contains='BUTTERBURGERS')
        chicken_sandwhich = MenuItem.objects.filter(category__name__contains='Chicken & Sandwhiches')
        seafood_salad = MenuItem.objects.filter(category__name__contains='Seafood & Salads')
        sides = MenuItem.objects.filter(category__name__contains='Sides')
        drinks = MenuItem.objects.filter(category__name__contains='Drinks')
        frozen_custard = MenuItem.objects.filter(category__name__contains='Fresh Frozen Custard')
        #pass into context
        context = {
            'BUTTERBURGERS': BUTTERBURGERS,
            'chicken_sandwhich': chicken_sandwhich,
            'seafood_salad': seafood_salad,
            'sides': sides,
            'drinks': drinks,
            'frozen_custard': frozen_custard,
        }

        #render templates
        return render(request, 'Culvers/order.html', context)
    
    #method to calculate total
    def post(self, request, *args, **kwargs):
        #order item dictionary with a list of items
        order_items = {
            'items': []
        }

        #grab all selected items
        items = request.POST.getlist('items[]')
        #get the item data for each selected item
        for item in items:
            menu_item = MenuItem.objects.get(pk=int(item))
            item_data = {
                'id': menu_item.pk,
                'name':menu_item.name,
                'price': menu_item.price
            }

            #append selected data to a list
            order_items['items'].append(item_data)

            #price and item id variables
            price = 0
            item_ids = []

        #loop through and get the price and id
        for item in order_items['items']:
            price += item['price']
            item_ids.append(item['id'])

        #set price to total price
        order = Order.objects.create(price=price)
        order.items.add(*item_ids)

        context = {
            'items': order_items['items'],
            'price': price
        }
        #go to confirmation page
        return render(request, 'Culvers/order_confirmation.html', context)
