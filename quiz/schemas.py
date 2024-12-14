from rest_framework import status
from drf_yasg import openapi

QuizStepByUserSchema = {
    status.HTTP_200_OK: openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
           'status': openapi.Schema(
              type=openapi.TYPE_STRING
           ),
           "question": openapi.Schema(
              type=openapi.TYPE_OBJECT,
              properties={
                    "id":       openapi.Schema(
                                    type=openapi.TYPE_INTEGER
                                ),
                    "question": openapi.Schema(
                                    type=openapi.TYPE_STRING
                                ),
                    "image":      openapi.Schema(
                                    type=openapi.TYPE_STRING
                                ),
                    "answers": openapi.Schema(
                                    type=openapi.TYPE_ARRAY,
                                    items=openapi.Items(type=openapi.TYPE_STRING)
                                )
                }
            )
        }
    )
}

LoginSchema = {
    status.HTTP_200_OK: openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
           'token': openapi.Schema(
              type=openapi.TYPE_STRING
           ),
           "user": openapi.Schema(
              type=openapi.TYPE_OBJECT,
              properties={
                    "id":       openapi.Schema(
                                    type=openapi.TYPE_INTEGER
                                ),
                    "username": openapi.Schema(
                                    type=openapi.TYPE_STRING
                                ),
                    "email":      openapi.Schema(
                                    type=openapi.TYPE_STRING
                                )
                }
            )
        }
    )
}
