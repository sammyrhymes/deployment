from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class MpesaTransaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    merchant_request_id = models.CharField(max_length=255)
    checkout_request_id = models.CharField(max_length=255)
    result_code = models.IntegerField()
    result_desc = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    mpesa_receipt_number = models.CharField(max_length=255)
    transaction_date = models.DateTimeField()
    phone_number = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.mpesa_receipt_number}"


class Competition(models.Model):
    car_model = models.CharField(max_length=100)
    description = models.TextField()
    specifications = models.TextField()
    rules = models.TextField()
    image = models.ImageField(upload_to='cars/')
    ticket_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_tickets = models.PositiveIntegerField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    max_entries_per_user = models.PositiveIntegerField()
    tickets_sold = models.IntegerField(default=0)

    def total_entries_sold(self):
        return self.entries.count()

    def remaining_entries(self):
        return self.total_tickets - self.total_entries_sold()

    def __str__(self):
        return self.car_model
    
class CompetitionImage(models.Model):
    competition = models.ForeignKey(Competition, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='cars/')

    def __str__(self):
        return f"Image for {self.competition.car_model}"

class Entry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    competition = models.ForeignKey(Competition, related_name='entries', on_delete=models.CASCADE)
    purchase_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.competition.car_model}"

class Winner(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
    win_date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='winners/', blank=True, null=True)
    testimonial = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.competition.car_model}"

class ContactInquiry(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    published_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class FAQ(models.Model):
    question = models.CharField(max_length=200)
    answer = models.TextField()

    def __str__(self):
        return self.question

class BasketItem(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
    ticket_count = models.IntegerField()
    added_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.ticket_count} tickets for {self.competition.car_model}"
