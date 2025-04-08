from rest_framework import serializers

from apps.accounts.serializers import CustomUserDetailSerializer
from apps.prices_x_cards.models import ProductPocket, ToBuyerUser, Card, Payment


class ProductPocketSerializer(serializers.ModelSerializer):
    price_digits = serializers.ReadOnlyField()

    class Meta:
        model = ProductPocket
        fields = ['id', 'title', 'description', 'price', 'price_type', 'price_digits', 'count_typing']


class ToBuyerUserSerializer(serializers.ModelSerializer):
    user = CustomUserDetailSerializer(read_only=True)
    product_pocket = ProductPocketSerializer(read_only=True)

    class Meta:
        model = ToBuyerUser
        fields = ['id', 'user', 'product_pocket', 'created']


    def create(self, validated_data):
        create = ToBuyerUser.objects.create(**validated_data)
        create.user = self.context['request'].user
        create.save()
        return create


class CardSerializer(serializers.ModelSerializer):
    user = CustomUserDetailSerializer(read_only=True)

    class Meta:
        model = Card
        fields = ['id', 'user', 'card_number', 'expiry_date', 'cardholder_name', 'added']

    def create(self, validated_data):
        create = Card.objects.create(**validated_data)
        create.user = self.context['request'].user
        create.save()
        return create


class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = ['id', 'user', 'product_pocket', 'card', 'amount', 'status', 'created']
        read_only_fields = ['user', 'status']

    card = serializers.PrimaryKeyRelatedField(queryset=Card.objects.all(), required=True)
    product_pocket = serializers.PrimaryKeyRelatedField(queryset=ProductPocket.objects.all(), required=True)

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        validated_data['status'] = 'pending'
        return super().create(validated_data)


class PaymentDetailSerializer(PaymentSerializer):
    user = CustomUserDetailSerializer(read_only=True)
    product_pocket = ProductPocketSerializer(read_only=True)
    card = CardSerializer(read_only=True)

    class Meta:
        model = Payment
        fields = ['id', 'user', 'product_pocket', 'card', 'amount', 'status', 'created']
