from django.contrib.auth import get_user_model

from django_grpc_framework.services import Service
import grpc
from google.protobuf import empty_pb2

from storage.serializers import UserProtoSerializer

User = get_user_model()


class UserService(Service):
    serializer_class = UserProtoSerializer

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            self.context.abort(grpc.StatusCode.NOT_FOUND, 'User:%s not found!' % pk)

    def List(self, request, context):
        users = User.objects.all()
        serializer = UserProtoSerializer(users, many=True)
        for msg in serializer.message:
            yield msg
    
    def Create(self, request, context):
        serializer = UserProtoSerializer(message=request)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer.message

    def Retrieve(self, request, context):
        post = self.get_object(request.id)
        serializer = UserProtoSerializer(post)
        return serializer.message

    def Update(self, request, context):
        post = self.get_object(request.id)
        serializer = UserProtoSerializer(post, message=request)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer.message

    def Destroy(self, request, context):
        user = self.get_object(request.id)
        user.delete()
        return empty_pb2.Empty()