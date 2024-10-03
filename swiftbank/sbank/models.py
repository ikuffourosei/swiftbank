from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

# ACCOUNT MODEL
class Account(models.Model):
    """Database model for accounts"""
    account_no = models.BigIntegerField(unique=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    username = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"Account: {self.account_no} \nBalance: {self.balance}"

# TRANSACTION MODEL
class Transaction(models.Model):
    """Transaction model"""
    TRANSACTION = [
        ('CR', 'CREDIT'),
        ('DB', 'DEBIT'),
    ]
    trans_type = models.CharField(choices=TRANSACTION, max_length=2)
    amount = models.DecimalField(max_digits=10, decimal_places=2, 
                                 validators=[MinValueValidator(1.00)])
    date = models.DateTimeField(auto_now_add=True)
    account = models.ForeignKey(Account, on_delete=models.RESTRICT)

    def __str__(self) -> str:
        return f"Date: {self.date}\nTransaction Type: {self.get_trans_type_display()}\nAmount: {self.amount}"

# SECRET PIN
class MyUser(models.Model):
    """Custom User Model that inherits from django User with Secret Pin"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    pin = models.IntegerField(validators=[
        MinValueValidator(1000), MaxValueValidator(9999)]
        )
    account = models.ForeignKey(Account, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"Welcome! {self.user.get_username()} {self.account.account_no}"
