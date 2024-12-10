from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .permissions import IsAdminOrReadOnly
from .models import *
from .serializers import *
from drf_yasg.utils import swagger_auto_schema
from .serializers import UserCreateSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer
from django.http import HttpResponse
from rest_framework.permissions import IsAuthenticated
from drf_yasg import openapi
import csv

class CreateUserView(APIView):
    permission_classes = [IsAdminOrReadOnly] 
    @swagger_auto_schema(
        request_body=UserCreateSerializer,  # Specify the request body schema
        operation_description="Endpoint to create a new user",
    )
    def post(self, request, *args, **kwargs):
        # Use UserCreateSerializer, not UserSerializer
        serializer = UserCreateSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class BookList(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request):
        """
        Retrieve the list of all books.
        """
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    @swagger_auto_schema(
    operation_description="Create a new book",
    request_body=BookSerializer,
    responses={201: BookSerializer},
    )
    def post(self, request):
        """
        Add a new book to the database.
        """
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookDetail(APIView):

    permission_classes = [IsAdminOrReadOnly]
    def get(self, request, pk):
        """
        Retrieve a specific book by ID.
        """
        try:
            book = Book.objects.get(pk=pk)
            serializer = BookSerializer(book)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Book.DoesNotExist:
            return Response({"error": "Book not found."}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_description="Update an existing book",
        request_body=BookSerializer,  # Use the full model serializer for PUT
        responses={200: BookSerializer},  # Define the response schema
    )    
    def put(self, request, pk):
        """
        Update a specific book by ID.
        """
        try:
            book = Book.objects.get(pk=pk)
            serializer = BookSerializer(book, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Book.DoesNotExist:
            return Response({"error": "Book not found."}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        """
        Delete a specific book by ID.
        """
        try:
            book = Book.objects.get(pk=pk)
            book.delete()
            return Response({"message": "Book deleted successfully."}, status=status.HTTP_200_OK)
        except Book.DoesNotExist:
            return Response({"error": "Book not found."}, status=status.HTTP_404_NOT_FOUND)

# Base API view with authentication
class ActiveAuthenticatedAPIView(APIView):
    permission_classes = [IsAuthenticated]


class ViewBorrowRequests(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request):
        requests = BorrowRequest.objects.all()
        serializer = BorrowRequestSerializer(requests, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Create a new borrow request",
        request_body=BorrowRequestSerializer,  # This defines the fields to show in Swagger
        responses={
            201: openapi.Response("Created", BorrowRequestSerializer),
            400: "Bad Request - Invalid data",
        },
    )
    
    def post(self, request):
        serializer = BorrowRequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ViewPersonalBorrowHistory(ActiveAuthenticatedAPIView):
    def get(self, request):
        # Retrieve borrow history for the authenticated user
        history = BorrowHistory.objects.all()
        serializer = BorrowHistorySerializer(history, many=True)
        return Response(serializer.data, status=200)


class DownloadBorrowHistory(ActiveAuthenticatedAPIView):
    def get(self, request):
        history = BorrowHistory.objects.filter(user=request.user)
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="borrow_history.csv"'

        writer = csv.writer(response)
        writer.writerow(['Book Title', 'Borrowed At', 'Returned At'])
        writer.writerows([[h.book.title, h.borrowed_at, h.returned_at] for h in history])

        return response
