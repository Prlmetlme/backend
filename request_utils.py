from rest_framework.response import Response
from decouple import config
from Accounts import models
import jwt


def user_from_access_token(request):
    try:
        request.headers['authorization']
    except KeyError:
        return Response(status=401)
    auth_token:str = request.headers['authorization'].split(' ')[1]
    decoded_token = jwt.decode(auth_token, config('SIGNATURE'), algorithms=['HS256'])
    user_id = decoded_token.get('generated_member_id')
    data:models.User = models.User.objects.get(static_user_id=user_id)
    return data

def get_engagement_data_or_400(request):
    """Intended to be used as following: 'type, id, vote = get_engagement_data_or_400'"""
    try:
        type:str = request.data.get('type')
    except:
        raise {'error': 'Please specify if model is "post" or "comment"'}
    try:
        id:str = request.data.get('id')
    except:
        raise {'error': 'Please specify the id for the post or comment'}
    try:
        like_or_dislike:str = request.data.get('vote')
    except:
        raise {'error': 'Please specify whether the request is a like or dislike'}
    return (type, id, like_or_dislike)
    