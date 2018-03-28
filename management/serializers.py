from rest_framework import serializers
from management.models import CustomUser as User
from management.models import Product, Order, ProductInOrder, Category, Flavor, Background, Size, GlobalValues
from django.contrib.auth.models import Group
from django.contrib.auth import update_session_auth_hash
from _constants.constants import WEEDING_SURCHARGE


class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    confirm_password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email','password',
                  'confirm_password',)
        lookup_field= 'id' # whithout this it shows an error


        def create(self, validated_data):
            return User.objects.create(**validated_data)

        def update(self, instance, validated_data):

            #instance.username = validated_data.get('username', instance.username)
            #instance.tagline = validated_data.get('tagline', instance.tagline)

            password = validated_data.get('password', None)
            confirm_password = validated_data.get('confirm_password', None)

            if password and confirm_password and password == confirm_password:
                instance.set_password(password)
                instance.save()

            update_session_auth_hash(self.context.get('request'), instance)

            return instance


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class ProductSerializer(serializers.ModelSerializer):

    """
    Serializer to parse Product's data
    """

    image = serializers.SerializerMethodField('show_image_url')
    thumbnail = serializers.SerializerMethodField('show_thumbnail_url')
    name = serializers.SerializerMethodField('show_product_full_name')
    size = serializers.SerializerMethodField('get_size_name')
    wedding_surcharge = serializers.SerializerMethodField()

    def show_image_url(self, product):
        return product.get_image_url()

    def show_thumbnail_url(self, product):
        return product.get_thumbnail_url()

    def show_product_full_name(self, product):
        return product.get_full_name()

    def get_size_name(self, product):
        return product.get_size_name()

    def get_wedding_surcharge(self, product):
        if product.category.name == "Torta de Panqueque":
            return WEEDING_SURCHARGE
        else:
            return False

    class Meta:
        model = Product
        fields = ('id', 'category', 'flavor', 'size', 'description', 'price', 'image', 'thumbnail', 'created_date', 'status', 'discount', 'sold_units', 'new', 'name', 'wedding_surcharge')


class CategorySerializer(serializers.ModelSerializer):

    """ Model Serializer to parse Category's data """

    image = serializers.SerializerMethodField('show_image_url')

    def show_image_url(self, category):
        return category.get_image_url()

    class Meta:
        model = Category


class FlavorSerializer(serializers.ModelSerializer):

    """ Model Serializer to parse Flavor's data """

    image = serializers.SerializerMethodField('show_image_url')

    def show_image_url(self, flavor):
        return flavor.get_image_url()

    class Meta:
        model = Flavor


class SizeSerializer(serializers.ModelSerializer):

    """ Model Serializer to parse Size's data """

    image = serializers.SerializerMethodField('show_image_url')

    def show_image_url(self, size):
        return size.get_image_url()

    class Meta:
        model = Size


class ProductInOrderSerializer(serializers.ModelSerializer):

    """ Model Serializer to parse ProductInOrder's data """

    class Meta:
        model = ProductInOrder


class OrderSerializer(serializers.ModelSerializer):

    """
    Serializer to parse Order's data
    """
    user = CustomUserSerializer(read_only=True, required=False)
    class Meta:
        model = Order

        fields = ('id', 'user', 'name', 'phone_number', 'email', 'order_time', 'retire_time', 'order_source',
                  'status', 'discount', 'total')
        read_only_fields = ('id', 'order_time')

    def get_validation_exclusions(self, *args, **kwargs):
        exclusions = super(OrderSerializer, self).get_validation_exclusions()

        return exclusions + ['user']


class BackgroundSerializer(serializers.ModelSerializer):

    """ Model Serializer to parse Background's data """

    image = serializers.SerializerMethodField('show_image_url')

    def show_image_url(self, background):
        return background.get_image_url()

    class Meta:
        model = Background