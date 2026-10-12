from concurrent.futures import ThreadPoolExecutor
import logging
import os

import grpc
import protovalidate
from sqlmodel import Session, select

from common.database import Database
from common.models import User
from location.v1 import location_pb2, location_pb2_grpc


class LocationService(location_pb2_grpc.LocationServiceServicer):
    def GetUserLocation(self, request, context):
        try:
            protovalidate.validate(request)
        except protovalidate.ValidationError:
            context.abort(
                grpc.StatusCode.INVALID_ARGUMENT,
                "userEmail must be a valid email address",
            )

        with Session(Database().engine) as session:
            user = session.exec(select(User).where(User.user_email == request.user_email)).first()

        if user is None:
            context.abort(grpc.StatusCode.NOT_FOUND, "User not found")

        if user.user_id is None:
            context.abort(grpc.StatusCode.INTERNAL, "Location data is unavailable")

        response = location_pb2.GetUserLocationResponse(
            user_id=user.user_id,
            location_code=user.location_code,
        )
        try:
            protovalidate.validate(response)
        except protovalidate.ValidationError:
            context.abort(grpc.StatusCode.INTERNAL, "Location data is unavailable")

        return response


def serve() -> None:
    port = int(os.environ.get("PORT", "50051"))
    server = grpc.server(ThreadPoolExecutor(max_workers=10))
    location_pb2_grpc.add_LocationServiceServicer_to_server(LocationService(), server)
    server.add_insecure_port(f"[::]:{port}")
    server.start()
    logging.info("Location gRPC service listening on port %s", port)
    server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig(level=os.environ.get("LOG_LEVEL", "INFO"))
    serve()
