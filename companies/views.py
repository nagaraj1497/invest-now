from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView
from .serializers import UserSerializer, LoginSerializer, InvestSerializer, CompanySerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password
from django.contrib.auth import login
from .models import Investment, Company
from django.db.models import Sum

# Create your views here.
class RegisterView(CreateAPIView):
    queryset = User.objects.none()
    serializer_class = UserSerializer

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        user_info = request.POST
        serializer = self.serializer_class(data=user_info)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"saved successfully"}, status=200, content_type="json")
        return Response({"msg":serializer.errors}, status=400, content_type="json")

class LoginView(CreateAPIView):
    queryset = User.objects.none()
    serializer_class = LoginSerializer

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        email = request.POST["email"]
        password = request.POST["password"]
        serializer = self.serializer_class(data=request.POST)
        if not serializer.is_valid():
            return Response({"msg": serializer.errors}, status=400)

        queryset = User.objects.get(email__iexact=email)
        if not check_password(password,queryset.password):
            return Response({"msg":"Invalid password. Please check the password once again"}, status=400)

        login(request, queryset)
        return Response({"msg":"Logged in successfully"}, status=200)

class InvestView(RetrieveUpdateDestroyAPIView):
    queryset = Investment.objects.all()
    serializer_class = InvestSerializer
    permission_classes = [IsAuthenticated]

    @csrf_exempt
    def get(self, request, pk):
        invest = Investment.objects.filter(user=pk).values("company__name", "no_shares")
        investment_list = [inv for inv in invest]
        if len(investment_list) == 0:
            return Response({"msg":"Investment info not found"}, status=400)
        total_amount = Investment.objects.filter(user=pk).aggregate(total_amount = Sum('invest_amount'))
        remainig_balance = Investment.objects.filter(user=pk).last()
        investment_list.append(
            {'total_investment_amount':total_amount.get("total_amount"),
             'total_remaining_balance':remainig_balance.total_balance}
        )
        return Response(investment_list, status=200)

    @csrf_exempt
    def put(self, request, pk):
        invest_obj = get_object_or_404(self.get_queryset(),pk=pk)
        update_info = request.POST
        serializer = self.serializer_class(instance=invest_obj, data=update_info, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"msg":f"investment info updated successfully"}, status=200)
        return Response({"msg":"Unable to update"}, status=400)

class InvestRView(CreateAPIView):
    serializer_class = InvestSerializer
    permission_classes = [IsAuthenticated]

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        invest_info = request.POST
        serializer = self.serializer_class(data=invest_info)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"msg": "invest info added successfully"}, status=200)
        return Response({"msg": "unable to save investment info"}, status=400)

class CompanyRegisterView(CreateAPIView):
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated]

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        company_info = request.POST
        seralizer = CompanySerializer(data=company_info)
        if seralizer.is_valid():
            seralizer.save()
            return Response({"msg": "Company added successfully"}, status=200)
        return Response(seralizer.errors, status=400)

class CompanyUpdateView(RetrieveUpdateDestroyAPIView):
    queryset = Company.objects.none()
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Company.objects.all()

    @csrf_exempt
    def put(self, request, pk):
        comp_object = get_object_or_404(self.get_queryset(),pk=pk)
        update_info = request.data
        seralizer = CompanySerializer(instance=comp_object, data=update_info, partial=True)
        if seralizer.is_valid(raise_exception=True):
            seralizer.save()
            return Response({"msg":f"Company updated successfully"}, status=200)
        return Response({"msg":"Unable to update"}, status=400)

    @csrf_exempt
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset().values("company_id","name","location","share_price")
        serializer = CompanySerializer(data=list(map(lambda q: q,queryset)), many=True)
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.data, status=200)
        return Response({"msg":"Unable to fetch the data"}, status=400)

    @csrf_exempt
    def delete(self, request, pk):
        company = get_object_or_404(self.get_queryset(), pk=pk)
        company.delete()
        return Response({"msg": f"Company {pk} is deleted"}, status=200)