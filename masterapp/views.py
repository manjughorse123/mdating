
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import render, get_object_or_404, redirect
from account. models import *
from account.serializers import *
from friend.models import *
from friend.serializers import *
from django.shortcuts import render, get_object_or_404

# Create your views here.


def index(request):

    return render(request, '../templates/index.html')


class GenderList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'gender.html'

    def get(self, request):
        gender = Gender.objects.all()
        return Response({'genders': gender})

    def post(self, request):
        serializer = GenderSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({'serializer': serializer})
        serializer.save()
        return redirect('genderlist')


class GenderEditView(APIView):
    """
    Retrieve, update or delete  a Passion instance.
    """
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'gender.html'

    # def get(self, request, pk):
    #     profile = get_object_or_404(Profile, pk=pk)
    #     serializer = ProfileSerializer(profile)
    #     return Response({'serializer': serializer, 'profile': profile})
    def get(self, request, pk):

        profile = get_object_or_404(Gender, pk=pk)
        serializer = GenderSerializer(profile)
        return Response({'serializer': serializer, 'genderId': profile})

    def post(self, request, pk):
        profile = get_object_or_404(Gender, pk=pk)
        serializer = GenderSerializer(profile, data=request.data)
        if not serializer.is_valid():
            return Response({'serializer': serializer, 'profile': profile})
        serializer.save()
        return redirect('profile-list')

    def put(self, request, pk, format=None):
        addGender = self.get_object(pk)
        serializer = GenderSerializer(addGender, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": "True", "data": serializer.data})
        return Response(serializer.errors)

    def patch(self, request, pk, format=None):
        addGender = self.get_object(pk)
        serializer = GenderSerializer(
            addGender, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        addGender = self.get_object(pk)
        addGender.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# class GenderPost(APIView):


class PassionList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'passion.html'

    def get(self, request):
        queryset = Passion.objects.all()
        return Response({'passions': queryset})

    def post(self, request):

        serializer = PassionSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({'serializer': serializer})
        serializer.save()
        return redirect('passionlist')


class MaritalStatusList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'marital-status.html'

    def get(self, request):
        queryset = MaritalStatus.objects.all()
        return Response({'maritalstatus': queryset})

    def post(self, request):

        serializer = MaritalStatusSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({'serializer': serializer})
        serializer.save()
        return redirect('maritalstatuslist')


class IdealMatchProfile(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'ideal-match.html'

    def get(self, request):
        queryset = IdealMatch.objects.all()
        return Response({'idealmatch': queryset})

    def post(self, request):

        serializer = IdealMatchSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({'serializer': serializer})
        serializer.save()
        return redirect('idealmatchlist')

# class PassionList(APIView):
#     renderer_classes = [TemplateHTMLRenderer]
#     template_name = 'passion.html'

#     def get(self, request):
#         queryset = Passion.objects.all()
#         return Response({'passions': queryset})

#
# class IdealMatchProfile(APIView):
#     renderer_classes = [TemplateHTMLRenderer]
#     template_name = 'ideal-match.html'
#
#     def get(self, request):
#         queryset = IdealMatch.objects.all()
#         return Response({'idealmatch': queryset})
#
#     def post(self, request):
#
#
#         serializer = IdealMatchSerializer( data=request.data)
#
#         if not serializer.is_valid():
#             return Response({'serializer': serializer})
#         serializer.save()
#         return redirect('idealmatchlist')
#
#


class UserVerifiedList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'user-verified.html'

    def get(self, request):
        queryset = AdminUserVerified.objects.all()
        print(queryset)
        return Response({'userverify': queryset})

    def post(self, request):

        serializer = AdminUserVerifiedSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({'serializer': serializer})
        serializer.save()
        return redirect('userverifiedlist')


class FAQView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'faq.html'

    def get(self, request):
        queryset = FAQ.objects.all()
        return Response({'faqlist': queryset})

    def post(self, request):

        serializer = FAQSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({'serializer': serializer})
        serializer.save()
        return redirect('faqlist')
