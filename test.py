# class Register(APIView):
#
#     def post(self, request):
#         password1 = request.data.get("password")
#         password2 = request.data.get("confirm_password")
#         tnc = request.data.get("is_accept")
#         email = request.data.get("email")
#         mobile = request.data.get("mobile")
#         if tnc and password1 and password2 and password2 == password1:
#             if mobile:
#                 user_exists = User.objects.filter(username=mobile).exists()
#                 if user_exists:
#                     user = User.objects.get(username=mobile)
#                     if user.is_active:
#                         return Response({"message": "User with this Mobile No. already exists.", "flag": False},
#                                         status=status.HTTP_400_BAD_REQUEST)
#                     else:
#                         user.set_password(password1)
#                 else:
#                     user = User.objects.create_user(username=mobile, password=password1, email=email)
#                     user.is_active = False
#                     user.save()
#                 if not MobileVerify.objects.filter(number=mobile).exists():
#                     otp = random_with_N_digits(6)
#                     res = send_sms(mobile, otp)
#                     mobile_obj = MobileVerify.objects.create(number=mobile, otp=otp, otp_time=datetime.datetime.now(),
#                                                              status=0)
#                     mobile_obj.save()
#                 else:
#                     otp = random_with_N_digits(6)
#                     res = send_sms(mobile, otp)
#                     mobile_obj = MobileVerify.objects.get(number=mobile)
#                     mobile_obj.otp_time = datetime.datetime.now()
#                     mobile_obj.otp = otp
#                     mobile_obj.save()
#                 return Response({"message": "Otp sent", "details": json.loads(res), "is_otp": True},
#                                 status=status.HTTP_201_CREATED)
#             if email:
#                 user_exists = User.objects.filter(username=email).exists()
#                 user = None
#                 if user_exists:
#                     user = User.objects.get(username=email)
#                     if user.is_active:
#                         return Response({"message": "User with this email already exists", "flag": False},
#                                         status=status.HTTP_400_BAD_REQUEST)
#                     else:
#                         user.set_password(password1)
#                 else:
#                     user = User.objects.create_user(username=email, password=password1, email=email)
#                     user.is_active = False
#                     user.save()
#                 current_site = get_current_site(request)
#                 mail_subject = 'Activate your account.'
#                 message = render_to_string('acc_active_email.html', {
#                     'user': user,
#                     'domain': current_site.domain,
#                     'uid': str(urlsafe_base64_encode(force_bytes(user.pk))),
#                     'token': account_activation_token.make_token(user),
#                 })
#                 email = EmailMessage(mail_subject, message, to=[email])
#                 email.send(fail_silently=True)
#                 return Response({"message": "email sent", "is_otp": False}, status=status.HTTP_201_CREATED)
#         else:
#             return Response({"message": "Please check the form filled."}, status=status.HTTP_400_BAD_REQUEST)
#         return Response({"message": "Please fill either Mobile or Email"}, status=status.HTTP_201_CREATED)
#
#
#
#
#
#
#
#
#
#
#
# class VirifyOtp(APIView):
#     def post(self, request, *args, **kwargs):
#         mobile = request.POST.get('mobile')
#         otp = request.POST.get('otp')
#         profile = User.objects.filter(mobile=mobile).first()
#         if otp == profile.otp:
#             return Response({"message": "Redirect to Next Pages", "status_code": True}, status=status.HTTP_200_OK)
#         else:
#             return Response({"message": "Wrong Otp"}, status=status.HTTP_400_BAD_REQUEST)
#






#
# class LoginOtp(APIView):
#
#     def post(self, request, *args, **kwargs):
#         print(request.user)
#         # mobile = request.session['mobile']
#         mobile = request.POST.get("mobile")
#         otp = request.POST.get("otp")
#         profile = User.objects.filter(mobile=mobile).first()
#
#         if otp == profile.otp:
#             user = User.objects.get(id=profile.user.id)
#             login(request, user)
#             return Response({"message": "Done", "status_code": True}, status=status.HTTP_200_OK)
#         else:
#             return Response({"message": "Wrong OTP", "status_code": False}, status=status.HTTP_400_BAD_REQUEST)





#
# class Login(APIView):
#     def post(self, request, *args, **kwargs):
#         mobile = request.POST.get('mobile')
#         country_code = request.POST.get('country_code')
#         otp = request.POST.get("otp")
#         user = User.objects.filter(mobile=mobile, country_code=country_code).first()
#         # user_obj = User.objects.get(mobile=mobile, otp=otp)
#         if user is None:
#             return Response(
#                 {"message": "mobile no. not registered", "flag": False},
#                 status=status.HTTP_404_NOT_FOUND)
#         # otp = str(random.randint(999, 9999))
#
#         # elif user_obj.otp == otp:
#         #     # user.is_phone_verified = True
#         #     user.save()
#         user.otp = otp
#         user.save()
#         return Response({"message": "Done", "status_code": True},
#                         status=status.HTTP_200_OK)
#
#         # profile = User.objects.filter(mobile=mobile).first()
#
#         # data = profile.otp
#         # if data == profile.otp:
#         #     user.otp = data
#         #     user.save()
#         #
#         # else:
#         #     return Response({"message": "Wrong OTP", "status_code": False}, status=status.HTTP_400_BAD_REQUEST)
#
#         # send_otp(mobile, otp)
#         # request.sessions['mobile'] = mobile
#         # return Response({"message": "redirect to main pages", "status_code": True},
#         #                 status=status.HTTP_201_CREATED)
#
#


#
# class Registration(APIView):
#     def post(self, request, *args, **kwargs):
#         try:
#
#             email = request.POST.get('email')
#             mobile = request.POST.get('mobile')
#             country_code = request.POST.get('country_code')
#             name = request.POST.get('name')
#             birth_date = request.POST.get('birth_date')
#             check_user = User.objects.filter(email=email, mobile=mobile).first()
#
#             if check_user:
#                 return Response({"message": "User Already Exists", status: False}, status=status.HTTP_400_BAD_REQUEST)
#
#             otp = str(random.randint(999, 9999))
#             user = User(email=email, name=name, birth_date=birth_date, mobile=mobile, otp=otp,
#                         country_code=country_code)
#             user.save()
#
#             return Response({"message": "Your Registrations is successfully", "status_code": True},
#                             status=status.HTTP_201_CREATED)
#
#         except Exception as e:
#             print(e)
#             return Response({'flag': False, 'message': 'something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#
