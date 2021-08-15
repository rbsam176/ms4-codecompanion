from django.shortcuts import get_object_or_404
from services.models import Service
import datetime


def bag_contents(request):
    bag = request.session.get('bag', {})
    total = 0

    bag_items = []

    # unpack bag into individual items
    for object, detail in bag.items():
        service = get_object_or_404(Service, pk=object)
        service_price = service.price
        service_price_type = service.price_type
        service_duration = service.duration
        for x in detail:
            start_dt = datetime.datetime.strptime(x['start_datetime'], "%Y-%m-%d %H:%M:%S")
            print(start_dt)
            bag_items.append({
                'service_name': service.name,
                # 'start_datetime': x['start_datetime'],
                'start_datetime': start_dt,
                'companion_selected': x['companion_selected'],
                'service_price': service_price,
                'service_price_type': service_price_type,
                'service_duration': service_duration,
            })
            total += service_price

    context = {
        'bag_items': bag_items,
        'product_count': len(bag_items),
        'total': total,
    }

    return context