from django.shortcuts import render

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Product

from django.contrib.auth.decorators import login_required


class UserProductsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        products = Product.objects.filter(owner=request.user)
        product_list = [{"name": p.name, "description": p.description} for p in products]
        return Response(product_list)
    
class AddProductView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        product_name = request.data.get('name')
        product_description = request.data.get('description')

        if product_name and product_description:
            # Ürün oluştur ve kullanıcıya ata
            product = Product.objects.create(
                name=product_name,
                description=product_description,
                owner=request.user
            )
            product.save()
            return Response({"message": "Product added successfully!"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "Name and description are required."}, status=status.HTTP_400_BAD_REQUEST)
        
#@login_required
