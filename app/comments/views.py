from rest_framework.views import APIView
from rest_framework.request import Request
from .models import CommentTable
from rest_framework.response import Response
from app.common.response import validate, success_response
from .serializer import CommentSerializer
from core.common.values import GuayaquilDatetime

class CommentView(APIView):
    @validate(CommentSerializer)
    def post(self, request: CommentSerializer) -> Response:
        data = request.validated_data
        comment = CommentTable(
            content=data['content'],
            starts=data['starts'],
            user_id=data['user_id'],
            service_id=data['service_id'],
            created_at=GuayaquilDatetime.now()
        )
        comment.save()
        return success_response(self.map_comment_to_dict(comment))
    
    @validate()
    def get(self, request: Request) -> Response:
        service_id = request.GET.get('service_id')
        comments = CommentTable.objects.filter(service__id=service_id)
        return success_response([self.map_comment_to_dict(comment) for comment in comments])

    def map_comment_to_dict(self, comment: CommentTable) -> dict:
        return {
            'id': comment.id,
            'content': comment.content,
            'starts': comment.starts,
            'user_id': comment.user.id,
            'service_id': comment.service.id,
            'created_at': comment.created_at.isoformat()
        }