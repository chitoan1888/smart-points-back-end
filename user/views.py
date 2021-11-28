from rest_framework import generics, permissions, status
from rest_framework.response import Response
from knox.models import AuthToken
from .serializers import UserSerializer, RegisterSerializer, ChangePasswordSerializer, UserInfoSerializer
from .models import UserInfo, CustomUser
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated   

# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })

from django.contrib.auth import login
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from .models import UserInfo
from rest_framework import generics, filters

class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)

class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = CustomUser
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserAPI(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
# Create your views here.

class UserDataAPI(generics.ListCreateAPIView):
    queryset= UserInfo.objects.all()
    serializer_class = UserInfoSerializer
    
class UserDataAPIDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserInfoSerializer
    lookup_field = "uid"

    def get_queryset(self):
        return UserInfo.objects.filter(uid=self.kwargs['uid'])

class isPremiumPartialUpdateView(APIView):

    def patch(self, request, uid, isPremium):
        # if no model exists by this id, raise a 404 error
        model = get_object_or_404(UserInfo, pk=uid)

        # this is the only field we want to update
        data = {"isPremium": bool(isPremium)}
        serializer = UserInfoSerializer(model, data=data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        # return a meaningful error response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TemplateLikedPartialUpdateView(APIView):

    def patch(self, request, uid, action, idOrIndex):
        # if no model exists by this id, raise a 404 error
        model = get_object_or_404(UserInfo, pk=uid)

        if action=="like":
            model.templateLiked.append(idOrIndex)
        elif action=="unlike":
            model.templateLiked.pop(int(idOrIndex))

        # this is the only field we want to update
        data = {"templateLiked": model.templateLiked}
        serializer = UserInfoSerializer(model, data=data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        # return a meaningful error response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TemplateDownloadedPartialUpdateView(APIView):

    def patch(self, request, uid, id):
        # if no model exists by this id, raise a 404 error
        model = get_object_or_404(UserInfo, pk=uid)
        model.templateDownloaded.append(id)
        # this is the only field we want to update
        data = {"templateDownloaded": model.templateDownloaded}
        serializer = UserInfoSerializer(model, data=data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        # return a meaningful error response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
