import base64
import json
import requests
from django.core.files.base import ContentFile
from .models import Check

def generate_pdf(check_id):
    check = Check.objects.get(id=check_id)
    order_id = check.order.get('id', 0)
    
    html_content = f"<h1>Заказ {order_id}</h1><p>Тип: {check.type}</p><p>Детали: {json.dumps(check.order)}</p>"
    
    # Строго 127.0.0.1 для Windows + Docker
    wkhtmltopdf_url = 'http://127.0.0.1:8005/'
    data = {'contents': base64.b64encode(html_content.encode('utf-8')).decode('utf-8')}
    
    try:
        print(f"Отправка запроса на {wkhtmltopdf_url} для чека {check_id}...")
        response = requests.post(wkhtmltopdf_url, json=data, timeout=10)
        response.raise_for_status() # Бросит ошибку, если ответ не 200 OK
        
        filename = f"{order_id}_{check.type}.pdf"
        check.pdf_file.save(filename, ContentFile(response.content))
        check.status = 'rendered'
        check.save()
        print(f"Успех! Файл {filename} сохранен.")
        
    except Exception as e:
        print(f"ОШИБКА генерации PDF: {e}")
        raise  # Заставляем воркер показать статус Failed