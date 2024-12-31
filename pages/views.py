from django.shortcuts import get_object_or_404
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Actor, ActorImage, ActorVideo, Application, Recruit
from .permissions import IsCompanyUser, IsOwnerOrReadOnly
from .serializers import (
    ActorImageSerializer,
    ActorSerializer,
    ActorVideoSerializer,
    ApplicationSerializer,
    RecruitSerializer,
)


class RecruitViewSet(viewsets.ModelViewSet):
    queryset = Recruit.objects.all()
    serializer_class = RecruitSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsCompanyUser]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    @action(detail=True, methods=["post"])
    def apply(self, request, pk=None):
        recruit = self.get_object()
        actor = get_object_or_404(Actor, user=request.user)
        application, created = Application.objects.get_or_create(recruit=recruit, actor=actor)
        if created:
            return Response({"status": "application submitted"})
        else:
            return Response({"status": "already applied"}, status=status.HTTP_400_BAD_REQUEST)


class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(actor=self.request.user.actor)


class ActorViewSet(viewsets.ModelViewSet):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    @action(detail=True, methods=["get"])
    def portfolio(self, request, pk=None):
        actor = self.get_object()
        images = ActorImageSerializer(actor.images.all(), many=True).data
        videos = ActorVideoSerializer(actor.videos.all(), many=True).data
        return Response({"images": images, "videos": videos})


class ActorImageViewSet(viewsets.ModelViewSet):
    queryset = ActorImage.objects.all()
    serializer_class = ActorImageSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(actor=self.request.user.actor)


class ActorVideoViewSet(viewsets.ModelViewSet):
    queryset = ActorVideo.objects.all()
    serializer_class = ActorVideoSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(actor=self.request.user.actor)
