from django.shortcuts import get_object_or_404
from services.models import Service

def bag_contents(request):
    bag_items = []
    total = 0
    product_count = 0
    bag = request.session.get('bag', {})

    for service_name, quantity in bag.items():
        service = get_object_or_404(Service, pk=service_name)
        service_price = service.price
        service_price_type = service.price_type
        total += quantity * service.price
        product_count += quantity
        bag_items.append({
            'service_name': service_name,
            'service_price': service_price,
            'service_price_type': service_price_type,
            'quantity': quantity,
        })

    context = {
        'bag_items': bag_items,
        'product_count': product_count,
        'total': total,
    }

    return context