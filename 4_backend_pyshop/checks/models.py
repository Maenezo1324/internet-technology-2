from django.db import models

class Printer(models.Model):
    name = models.CharField(max_length=255)
    api_key = models.CharField(max_length=255, unique=True)
    check_type = models.CharField(max_length=20, choices=[('kitchen', 'kitchen'), ('client', 'client')])
    point_id = models.IntegerField()

    def __str__(self):
        return f"{self.name} ({self.check_type})"

class Check(models.Model):
    printer_id = models.ForeignKey(Printer, on_delete=models.CASCADE)
    type = models.CharField(max_length=20, choices=[('kitchen', 'kitchen'), ('client', 'client')])
    order = models.JSONField()
    status = models.CharField(max_length=20, default='new', choices=[('new', 'new'), ('rendered', 'rendered'), ('printed', 'printed')])
    pdf_file = models.FileField(upload_to='pdf/', blank=True, null=True)

    def __str__(self):
        return f"Check {self.id} for Order {self.order.get('id', 'N/A')}"