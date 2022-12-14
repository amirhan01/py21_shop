from rest_framework import serializers

from applications.cart.models import Cart
from applications.product.models import Category, Product, Image, Rating, Comment


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # print(representation)
        # representation['hello'] = 'hello john'
        if not instance.parent:
            representation.pop('parent')
        return representation


class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = ['image']


class CommentSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')

    class Meta:
        model = Comment
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')
    images = ImageSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = '__all__'

    def create(self, validated_data):
        requests = self.context.get('request')
        images = requests.FILES
        for i in range(10):
            product = Product.objects.create(**validated_data)
        print(images)
        for image in images.getlist('images'):
            Image.objects.create(product=product, image=image)

        return product

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # print(instance.likes.filter(like=True).count())
        representation['likes'] = instance.likes.filter(like=True).count()

        rating_result = 0
        for rating in instance.ratings.all():
            rating_result += int(rating.rating)
        try:
            representation['rating'] = rating_result / instance.ratings.all().count()
        except ZeroDivisionError:
            # representation['rating'] = 0
            pass
        representation['best name'] = 'John'
        return representation


class RatingSerializer(serializers.Serializer):
    rating = serializers.IntegerField(required=True, min_value=1, max_value=5)

