from django.shortcuts import get_object_or_404
from services.models import Service

def bag_contents(request):
    total = 0
    product_count = 0
    bag = request.session.get('bag', {})

    bag_items = []

    # unpack bag into individual items
    for object, detail in bag.items():
        service = get_object_or_404(Service, pk=object)
        service_price = service.price
        service_price_type = service.price_type
        for x in detail:
            bag_items.append({
                'service_name': service.name,
                'quantity': x['quantity'],
                'day_selected': x['day_selected'],
                'companion_selected': x['companion_selected'],
                'service_price': service_price,
                'service_price_type': service_price_type,
            })
            # increment the product count and total cost
            product_count += x['quantity']
            total += x['quantity'] * service_price

    context = {
        'bag_items': bag_items,
        'product_count': product_count,
        'total': total,
    }

    return context