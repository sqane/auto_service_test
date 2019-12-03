from autoservice import models
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token


class RegisterUser(APIView):
    def post(self, request):
        user = models.User()
        as_user = models.AS_user()
        try:
            user.username = request.query_params['username']
            user.set_password(request.query_params['password'])
            user.first_name = request.query_params['first_name']
            user.last_name = request.query_params['last_name']
            user.email = request.query_params['email']
            user.save()
            as_user.user = user
            lang = models.Language.objects.filter(short_code=request.query_params['lang'])
            as_user.lang = lang
            as_user.save()
        except:
            return Response('bad data',status=500)



class GetAllUsers(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        users = models.User.objects.all().values('id','username','email','first_name','last_name','last_login','password')
        for each in users:
            as_user = models.AS_user.objects.get(user=each['id'])
            each['as_pk'] = as_user.pk
            each['as_lang'] = as_user.lang.name
            each['as_lang_pk'] = as_user.lang.pk

        return Response({"users": users})
class GetUserData(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self,request):
        user = request.user
        user1 = models.User.objects.get(pk=user.pk).values('id','username','email','first_name','last_name','last_login')
        as_user = models.AS_user.objects.get(user=user).values('id','lang__name')

        return Response(user1,as_user)

class GetUserCars(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self,request):
        user = request.user
        as_user = models.AS_user.objects.get(user=user)
        lang = as_user.lang.short_code
        cars = models.UserCar.objects.filter(user=as_user).values('car_id','car__name_'+lang,
                                                                  'user_id','car__date_added',
                                                                  'car__year','in_rent',
                                                                  'already_leased','rent_user__user_id',
                                                                  'rent_user__user__username','rent_user__user__email',
                                                                  'rent_user__user__last_name','rent_user__user__first_name')
        return Response({"cars": cars})

class ChangUserData(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self,request):
        pk = request.query_params['pk']
        user = models.User.objects.get(pk=pk)
        as_user = models.AS_user.objects.get(user=user)
        changes = {}
        if 'new_pass' in request.query_params:
            new_pass = request.query_params['new_pass']
            user.set_password(new_pass)
            changes['password'] = 'new_password'

        if 'new_usr_name' in request.query_params:
            new_usr_name = request.query_params['new_usr_name']
            user.username = new_usr_name
            changes['username'] = new_usr_name
        if 'last_name' in request.query_params:
            last_name = request.query_params['last_name']
            user.last_name = last_name
            changes['last_name'] = last_name
        if 'first_name' in request.query_params:
            first_name = request.query_params['first_name']
            user.first_name = first_name
            changes['first_name'] = first_name
        if 'lang' in request.query_params:
            lang = request.query_params['lang']
            new_lang = models.Language.objects.filter(short_code=lang)[0]
            as_user.lang = new_lang
            changes['lang'] = new_lang.short_code
        as_user.save()
        user.save()
        return Response({"changes": changes})
