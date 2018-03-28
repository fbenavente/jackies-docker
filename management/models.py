from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin, Permission
from django.contrib import auth
from django.conf import settings
from jackies.settings import MEDIA_URL
from django.utils import timezone
from django.utils.encoding import smart_str
from _constants.choices import PRODUCT_STATUS_CODES, ORDER_SOURCE, ORDER_STATUS_CODES, DECORATION_OPTIONS


class Category(models.Model):
    name = models.CharField(max_length=200, blank=False, null=False, unique=True)
    short_name = models.CharField(max_length=30, blank=False, unique=True)
    order = models.IntegerField(unique=True, blank=True, null=True)
    image = models.ImageField(upload_to="uploads/categories/", blank=True, null=True)

    def __str__(self):
        return smart_str(self.name)

    def get_image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        else:
            return MEDIA_URL + 'uploads/categories/default-avatar-category.png'

    class Meta:
        app_label = 'management'
        db_table = 'category'

class Flavor(models.Model):
    category = models.ForeignKey(Category)
    name = models.CharField(max_length=200, blank=False, null=False)
    short_name = models.CharField(max_length=30, blank=True, null=True)
    order = models.IntegerField(blank=True, null=True)
    image = models.ImageField(upload_to="uploads/flavors/", blank=True, null=True)

    def __str__(self):
        return smart_str(self.category) + " " + smart_str(self.name)

    def get_image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        else:
            return MEDIA_URL + 'uploads/flavors/default-avatar-flavor.png'

    class Meta:
        unique_together = (("category", "name"),)
        app_label = 'management'
        db_table = 'flavor'

class Size(models.Model):
    category = models.ForeignKey(Category)
    name = models.CharField(max_length=200, blank=False, null=False)
    short_name = models.CharField(max_length=30, blank=True, null=True)
    order = models.IntegerField(blank=True, null=True)
    image = models.ImageField(upload_to="uploads/sizes/", blank=True, null=True)

    def __str__(self):
        return smart_str(self.category) + " " + smart_str(self.name)

    def get_image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        else:
            return MEDIA_URL + 'uploads/sizes/default-avatar-size.png'

    class Meta:
        unique_together = (("category", "name"),)
        app_label = 'management'
        db_table = 'size'

class Product(models.Model):

    category = models.ForeignKey(Category)
    flavor = models.ForeignKey(Flavor,null=True, blank=True)
    size = models.ForeignKey(Size,null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    price = models.IntegerField()
    image = models.ImageField(upload_to="uploads/products/", blank=True, null=True)
    thumbnail = models.ImageField(upload_to="uploads/products/thumbnails/", blank=True, null=True)
    created_date = models.DateField(null=True, blank=True, default=timezone.now)
    status = models.IntegerField(null=True, blank=True, choices=PRODUCT_STATUS_CODES, default=1)
    discount = models.IntegerField(default=0)
    sold_units = models.IntegerField(default=0)
    new = models.BooleanField(default=False)

    def __str__(self):
        return self.get_full_name() + " " + self.get_size_name()

    def get_full_name(self):
        if self.flavor:
            return smart_str(self.category) + " " + smart_str(self.flavor.name)
        else:
            return smart_str(self.category)

    def get_image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        else:
            return MEDIA_URL + 'uploads/products/default-avatar-product.png'

    def get_thumbnail_url(self):
        if self.thumbnail and hasattr(self.thumbnail, 'url'):
            return self.thumbnail.url
        else:
            return MEDIA_URL + 'uploads/products/default-avatar-product.png'

    def get_size_name(self):
        if self.size:
            return smart_str(self.size.name)
        else:
            return smart_str("único")

    #ToDo dont allow to create product with empty flavor if its category already has flavor(s)

    class Meta:
        unique_together = (("category", "flavor","size"),)
        app_label = 'management'
        db_table = 'product'

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, confirm_password=None, last_name=None, first_name=None):
        """
        Creates and saves a User with the given email, and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(email=self.normalize_email(email),
                          last_name=last_name,
                          first_name=first_name)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        """
        Creates and saves a superuser with the given email, and password.
        """
        user = self.create_user(email, password=password)
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(unique=True, max_length=255)
    first_name = models.CharField(max_length=30, null=True, blank=True)
    last_name = models.CharField(max_length=30, null=True, blank=True)
    profile_image = models.ImageField(upload_to="uploads/users/", blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    phone_number = models.CharField(max_length=30, null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def get_full_name(self):
        if self.first_name:
            if self.last_name:
                return smart_str(self.first_name + " " + self.last_name)
            else:
                return smart_str(self.first_name)
        return self.email.split("@")[0]

    def get_short_name(self):
        if self.first_name:
            return smart_str(self.first_name)
        return self.email.split("@")[0]

    # On Python 3: def __str__(self):
    def __str__(self):
        return self.email.split("@")[0]

    def get_image_url(self):
        if self.profile_image and hasattr(self.profile_image, 'url'):
            return self.profile_image.url
        else:
            return MEDIA_URL + 'uploads/users/default-avatar-user.png'

    @property
    def is_staff(self):
        """Is the user a member of staff?"""
        # Simplest possible answer: All admins are staff
        return self.is_admin

    class Meta:
        app_label = 'management'


class Order(models.Model):

    product = models.ManyToManyField(Product, through='ProductInOrder')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True)
    # Client info (if it is a "live" shopping)
    name = models.CharField(max_length=150, null=True, blank=True)
    phone_number = models.CharField(max_length=30, null=True, blank=True)
    email = models.EmailField(null=True, blank=True, max_length=255)
    # order info
    order_time = models.DateTimeField(default=timezone.now)
    retire_time = models.DateTimeField()
    order_source = models.IntegerField(null=True, blank=True, choices=ORDER_SOURCE, default=1)
    status = models.IntegerField(null=True, blank=True, choices=ORDER_STATUS_CODES, default=1)
    discount = models.IntegerField(default=0)
    total = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        app_label = 'management'
        db_table = 'order'


class ProductInOrder(models.Model):
    order = models.ForeignKey(Order)
    product = models.ForeignKey(Product)
    quantity = models.DecimalField(max_digits=4, decimal_places=1)
    wedding = models.BooleanField(default=False)
    decoration = models.IntegerField(null=True, blank=True, choices=DECORATION_OPTIONS, default=1)
    subtotal = models.IntegerField(null=True, blank=True)
    discount = models.IntegerField(default=0)

    class Meta:
        unique_together = (("order", "product","wedding"),)
        app_label = 'management'
        db_table = 'product_in_order'


class GlobalValues(models.Model):
    key = models.CharField(max_length=100, null=True, blank=True)
    int_value = models.IntegerField(null=True, blank=True)
    char_value = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        app_label = 'management'
        db_table = 'global_values'

    def __str__(self):
        return smart_str(self.key)


class Campaign(models.Model):
    title = models.CharField(max_length=250, null=True, blank=True)
    products = models.ManyToManyField(Product)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    active = models.BooleanField(default=False)

    class Meta:
        app_label = 'management'
        db_table = 'campaign'

class Background(models.Model):
    name = models.CharField(max_length=150, null=True, blank=True)
    image = models.ImageField(upload_to="uploads/backgrounds/", blank=True, null=True)
    available = models.BooleanField(default=True)

    def __str__(self):
        return smart_str(self.name)

    def get_image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        else:
            return MEDIA_URL + 'uploads/backgrounds/default-background.jpg'

    class Meta:
        app_label = 'management'
        db_table = 'background'