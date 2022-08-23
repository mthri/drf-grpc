import user_pb2_grpc
from storage.services import UserService


urlpatterns = [
    
]


def grpc_handlers(server):
    user_pb2_grpc.add_UserControllerServicer_to_server(UserService.as_servicer(), server)