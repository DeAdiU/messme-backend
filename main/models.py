from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator



class Mess(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    contact_no = models.CharField(
        max_length=10,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^\d{10}$',
                message='Contact number must be exactly 10 digits.'
            ),
        ]
    )
    password = models.CharField(max_length=255)
    address = models.CharField(max_length=255, null=True)
    rating = models.IntegerField(
        default=0, 
        validators=[
            MinValueValidator(0),
            MaxValueValidator(10)
        ], null=True
    )
    delivery = models.BooleanField(null=True)  # Corrected spelling here
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class User(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=255)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255, null=True)
    college = models.CharField(max_length=255, null=True)
    contact_no = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1000000000),
            MaxValueValidator(9999999999),
        ],
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

class Menu(models.Model):
    id = models.AutoField(primary_key=True)
    mess=models.ForeignKey(Mess,  on_delete=models.CASCADE)
    main_course=models.CharField(max_length=255)
    dessert=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    limited=models.BooleanField(default=False)
    price=models.IntegerField()
    updated_at=models.DateTimeField()

    def __str__(self):
        return self.main_course


class Orders(models.Model):
    id = models.AutoField(primary_key=True)
    menu=models.ForeignKey(Menu,  on_delete=models.CASCADE)
    user=models.ForeignKey(User,  on_delete=models.CASCADE)  # Corrected spelling here
    quantity=models.IntegerField(default=1)
    del_instructions=models.CharField(max_length=255)
    status=models.CharField(max_length=100)
    mode=models.CharField(max_length=100)
    created_at=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.id)  # Converted id to string for return
