from django.http import JsonResponse
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from projects.models import Project,review
from .serializers import ProjectSerializer

@api_view(['GET'])
def routes(request):
    routes=[{'GET':'api/projects'},{'GET':'api/projects/id'},{'POST':'projects/id/vote'},{'POST':'api/users/token'},{'POST':'/api/users/token/refresh'}]
    return Response(routes)
@api_view(['GET'])
def projects(request):
    projects=Project.objects.all()
    serializer=ProjectSerializer(projects,many=True)
    return Response(serializer.data)
@api_view(['GET'])
def project(request,pk):
    projects=Project.objects.get(id=pk)
    serializer=ProjectSerializer(projects,many=False)
    return Response(serializer.data)
@api_view(['POST','PUT'])
@permission_classes([IsAuthenticated])
def projectVote(request,pk):
    project=Project.objects.get(id=pk)
    user=request.user.profile
    data=request.data
    reviews,created=review.objects.get_or_create(owner=user,project=project)
    review.value=data['value']
    review.save()
    project.getVote
    serializer=ProjectSerializer(project,many=False)
    return Response(serializer.data)

