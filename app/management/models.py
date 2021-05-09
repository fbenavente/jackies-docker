from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.conf import settings
from jackies.settings import MEDIA_URL
from django.utils import timezone
from django.template.defaultfilters import slugify
from django.utils.encoding import smart_str
from _constants.choices import (
    PRODUCT_STATUS_CODES,
    ORDER_SOURCE,
    ORDER_STATUS_CODES,
    DECORATION_OPTIONS,
    ORDER_STATUS_CODES_DESC
)


class Category(models.Model):
    name = models.CharField(max_length=200, blank=False, null=False, unique=True)
    image = models.ImageField(upload_to="uploads/categories/", blank=True, null=True)

    def __str__(self):
        return smart_str(self.name)

    @property
    def normalized_name(self):
        return slugify(self.name).replace("-", "_")

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
    image = models.ImageField(upload_to="uploads/flavors/", blank=True, null=True)

    def __str__(self):
        return smart_str(self.category) + " " + smart_str(self.name)

    @property
    def normalized_name(self):
        return slugify(self.name).replace("-", "_")

    def get_normalized_name(self):
        return slugify(self.name).replace("-", "_")

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
    image = models.ImageField(upload_to="uploads/sizes/", blank=True, null=True)

    def __str__(self):
        return smart_str(self.category) + " " + smart_str(self.name)

    @property
    def normalized_name(self):
        return slugify(self.name).replace("-", "_")

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
    flavor = models.ForeignKey(Flavor, null=True, blank=True)
    size = models.ForeignKey(Size, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    price = models.IntegerField()
    image = models.ImageField(upload_to="uploads/products/", blank=True, null=True)
    thumbnail = models.ImageField(upload_to="uploads/products/thumbnails/", blank=True, null=True)
    created_date = models.DateField(null=True, blank=True, default=timezone.now)
    status = models.IntegerField(null=True, blank=True, choices=PRODUCT_STATUS_CODES, default=1)
    new = models.BooleanField(default=False)
    is_sugar_free = models.BooleanField(default=False)
    is_whole_grain = models.BooleanField(default=False)
    # internal use
    cost = models.IntegerField(default=0)

    def __str__(self):
        return self.get_full_name() + " " + self.get_size_name()

    def get_full_name(self):
        if self.flavor:
            return smart_str(self.category) + " " + smart_str(self.flavor.name)
        else:
            return smart_str(self.category)

    @property
    def full_name(self):
        if self.flavor:
            return smart_str(self.category) + " " + smart_str(self.flavor.name)
        else:
            return smart_str(self.category)

    @property
    def size_name(self):
        if self.size:
            return self.size.name
        return ''

    @property
    def category_name(self):
        if self.category:
            return self.category.name
        return ''

    @property
    def flavor_name(self):
        if self.flavor:
            return self.flavor.name
        return ''

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

    # ToDo dont allow to create product with empty flavor if its category already has flavor(s)

    class Meta:
        unique_together = (("category", "flavor", "size", "is_sugar_free", "is_whole_grain"),)
        app_label = 'management'
        db_table = 'product'


class CustomUserManager(BaseUserManager):
    def create_user(
            self,
            email,
            password=None,
            confirm_password=None,
            full_name=None,
            phone_number=None
        ):
        """
        Creates and saves a User with the given email, and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            full_name=full_name,
            phone_number=phone_number
        )

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
    full_name = models.CharField(max_length=100, null=True, blank=True)
    profile_image = models.ImageField(upload_to="uploads/users/", blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    phone_number = models.CharField(max_length=30, null=True, blank=True)
    rut = models.CharField(max_length=30, null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def get_full_name(self):
        return self.full_name

    def get_short_name(self):
        return self.full_name.split(" ")[0]

    # On Python 3: def __str__(self):
    def __str__(self):
        return self.full_name

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
    # order info
    order_time = models.DateTimeField(default=timezone.now)
    retire_time = models.DateTimeField()
    order_source = models.IntegerField(null=True, blank=True, choices=ORDER_SOURCE, default=1)
    status = models.IntegerField(null=True, blank=True, choices=ORDER_STATUS_CODES, default=1)
    total = models.IntegerField(null=True, blank=True)
    # internal fields
    migrated_from_old_system = models.BooleanField(default=False)
    admin_notes = models.TextField(null=True, blank=True)
    comments = models.TextField(null=True, blank=True)
    factura_required = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'

    def __str__(self):
        return str(self.id)

    @property
    def contains_products_sugar_free(self):
        products = ProductInOrder.objects.filter(order=self)
        if products.count() == 0:
            return False

        for product in products:
            if product.product.is_sugar_free:
                return True
        return False

    def _format_product_desc(self, product, product_quantity):
        product_name = product.get_full_name()
        product_size = None
        if product.size:
            product_size = product.size.name

        if float(product_quantity) != 1.0:
            if product_quantity == 0.5:
                product_quantity = '1/2'
            else:
                product_quantity = int(product_quantity)
            if product_size:
                if product.is_sugar_free:
                    return '{} {} sin azúcar ({})'.format(product_quantity, product_name, product_size)
                else:
                    return '{} {} ({})'.format(product_quantity, product_name, product_size)
            else:
                if product.is_sugar_free:
                    return '{} {} sin azúcar'.format(product_quantity, product_name)
                else:
                    return '{} {}'.format(product_quantity, product_name)
        if product_size:
            if product.is_sugar_free:
                return '{} sin azúcar ({})'.format(product_name, product_size)
            else:
                return '{} ({})'.format(product_name, product_size)
        return product_name

    @property
    def description(self):
        products = ProductInOrder.objects.filter(order=self)
        if products.count() == 0:
            return "No hay productos"

        if products.count() == 1:
            return self._format_product_desc(products[0].product, products[0].quantity)

        if products.count() == 2:
            return self._format_product_desc(products[0].product, products[0].quantity) + " y " + self._format_product_desc(products[1].product, products[1].quantity)
        else:
            return self._format_product_desc(products[0].product, products[0].quantity) + " y {} productos más".format(products.count() - 1)

    @property
    def status_description(self):
        return ORDER_STATUS_CODES_DESC.get(self.status)

    @property
    def user_info(self):
        if not self.user:
            return "-"
        return '{} - {}'.format(self.user.full_name, self.user.phone_number)

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

    class Meta:
        unique_together = (("order", "product", "wedding"),)
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

class CostItem(models.Model):
    name = models.CharField(max_length=200, blank=False, null=False)
    unit = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return smart_str(self.name) + " (" + smart_str(self.unit) + ")"

    class Meta:
        app_label = 'management'
        db_table = 'cost_item'
        ordering = ['name',]

class Cost(models.Model):
    cost_item = models.ForeignKey(CostItem)
    quantity = models.DecimalField(max_digits=6, decimal_places=1)
    total = models.IntegerField(null=True, blank=True)
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return smart_str(self.cost_item) + " - " + smart_str(self.total)

    def total_display(self):
        """ returns scores with dots as thousands separators in the admin display """
        return '{:,}'.format(self.total).replace(',','.')

    class Meta:
        unique_together = (("cost_item", "date"),)
        app_label = 'management'
        db_table = 'cost'
