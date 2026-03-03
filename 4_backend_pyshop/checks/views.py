import django_rq
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Printer, Check
from .tasks import generate_pdf

@api_view(['POST'])
def create_order(request):
    """Принимает заказ, создает чеки и ставит задачи в очередь."""
    order_data = request.data
    point_id = order_data.get('point_id')
    
    printers = Printer.objects.filter(point_id=point_id)
    if not printers.exists():
        return Response({"error": "Для данной точки не настроено ни одного принтера"}, status=400)
        
    order_id = order_data.get('id')
    if Check.objects.filter(order__id=order_id).exists():
        return Response({"error": "Чеки для данного заказа уже созданы"}, status=400)
        
    created_checks = []
    for printer in printers:
        check = Check.objects.create(
            printer_id=printer,
            type=printer.check_type,
            order=order_data
        )
        created_checks.append(check.id)
        # Ставим задачу в очередь (RQ)
        django_rq.enqueue(generate_pdf, check.id)
        
    return Response({"status": "ok", "created_checks": created_checks})