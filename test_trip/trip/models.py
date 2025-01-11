from django.db import models
import uuid

class Location(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    latitude = models.FloatField()
    longitude = models.FloatField()
    address = models.TextField()

    def __str__(self):
        return self.address

class Trip(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.UUIDField()
    order_id = models.UUIDField()
    pickup_location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="pickup_trips")
    dropoff_location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="dropoff_trips")
    status = models.CharField(max_length=20, choices=[("pending", "Pending"), ("active", "Active"), ("completed", "Completed")])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Trip {self.id} for Order {self.order_id}"
