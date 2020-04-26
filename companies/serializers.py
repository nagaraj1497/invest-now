from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer, ValidationError
from django.contrib.auth.hashers import make_password, PBKDF2PasswordHasher
from django.core.validators import validate_email
from .models import Investment, Company
from operator import sub, mul


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name','last_name','email','password']

    def create(self, validated_data):
        return validated_data

    def validate(self, attrs):
        for key, value in attrs.items():
            if not attrs.get(key):
                return ValidationError(f"{key} field is a required field")
        username = "{}_{}".format(attrs.get("first_name"),attrs.get("last_name"))
        password = make_password(attrs.get("password"),hasher=PBKDF2PasswordHasher())
        attrs["username"] = username
        attrs['password'] = password
        try:
             validate_email(attrs.get("email"))
             attrs['email'] = attrs.get("email")
        except ValidationError:
            return ValidationError()
        return attrs

    def save(self, **kwargs):
        user = User(**self.validated_data)
        user.save()


class LoginSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["email","password"]

class InvestSerializer(ModelSerializer):
    class Meta:
        model = Investment
        fields = ["no_shares","company","user"]

    def create(self, validated_data):
        try:
            total_balance = Investment.objects.get(user=validated_data.get("user")).total_balance
            validated_data['funds'] = total_balance
        except:
            validated_data['funds'] = 100000
        validated_data['invest_amount'] = mul(validated_data.get("company").share_price, validated_data.get("no_shares"))
        validated_data['total_balance'] = sub(float(validated_data.get("funds")), float(validated_data.get("invest_amount")))
        return Investment.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.no_shares = validated_data.get("no_shares", instance.no_shares)
        instance.company = validated_data.get("company", instance.company)
        if "company" in validated_data and "no_shares" in validated_data:
            instance.invest_amount = mul(validated_data.get("company").share_price, validated_data.get("no_shares"))
            instance.total_balance = sub(float(validated_data.get("funds")), float(instance.invest_amount))
        else:
            raise ValidationError("no_sares and company fields are required.")
        instance.save()
        return instance


class CompanySerializer(ModelSerializer):
    class Meta:
        model = Company
        fields = ["company_id","name","location","share_price"]

    def create(self, validated_data):
        return Company.objects.create(**self.validated_data)

    def validate(self, attrs):
        if "share_price" in attrs and int(attrs["share_price"]) > 699:
            raise ValidationError("Maximum share price exceeded")
        return attrs

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name",instance.name)
        instance.location = validated_data.get("location", instance.location)
        instance.share_price = validated_data.get("share_price", instance.share_price)
        instance.save()
        return instance