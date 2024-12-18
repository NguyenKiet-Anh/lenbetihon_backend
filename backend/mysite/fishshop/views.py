from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.serializers import Serializer
from .models import *
from .serializers import *
from fishshop import serializers
# For bills & reports
from reportlab.pdfgen import canvas
from reportlab.lib import fonts
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
# For authentication
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.contrib.auth import login
from django.contrib.auth.models import User
# Verify Email Import
import secrets
from django.core.mail import send_mail
from django.core.cache import cache
from validate_email import validate_email    # pip install py3-validate-email==1.0.4, pip install dnspython==2.4.1
# For encoding images
import base64
# Create your views here.

# Tất cả cá
@api_view(['GET'])
def getFish(request):
     # Lấy dữ liệu từ database
     fishes = CA_BETTA.objects.all()
     # Chuyển từ dạng Queryset sang định dạng Json, many = True vì có nhiều dòng dữ liệu
     serializers = CA_BETTA_Serializer(fishes, many=True)
     # Mã hóa hình ảnh trước khi gửi
     for item in serializers.data:        
        if item["hinh_anh1"]:
            with open(item["hinh_anh1"], "rb") as file:
                data = file.read()
                base64_encoded_data = base64.b64encode(data).decode("utf-8")
                item["hinh_anh1"] = base64_encoded_data
        if item["hinh_anh2"]:
            with open(item["hinh_anh2"], "rb") as file:
                data = file.read()
                base64_encoded_data = base64.b64encode(data).decode("utf-8")
                item["hinh_anh2"] = base64_encoded_data
        if item["hinh_anh3"]:
            with open(item["hinh_anh3"], "rb") as file:
                data = file.read()
                base64_encoded_data = base64.b64encode(data).decode("utf-8")
                item["hinh_anh3"] = base64_encoded_data
        if item["hinh_anh4"]:
            with open(item["hinh_anh4"], "rb") as file:
                data = file.read()
                base64_encoded_data = base64.b64encode(data).decode("utf-8")
                item["hinh_anh4"] = base64_encoded_data
     # Trả về dạng Json
     return Response(serializers.data)

@api_view(['GET'])
def getFish_no_special(request):
     # Lấy dữ liệu từ database
     fishes = CA_BETTA.objects.filter(dac_biet=False)
     # Chuyển từ dạng Queryset sang định dạng Json, many = True vì có nhiều dòng dữ liệu
     serializers = CA_BETTA_Serializer(fishes, many=True)
     # Mã hóa hình ảnh trước khi gửi
     for item in serializers.data:        
        if item["hinh_anh1"]:
            with open(item["hinh_anh1"], "rb") as file:
                data = file.read()
                base64_encoded_data = base64.b64encode(data).decode("utf-8")
                item["hinh_anh1"] = base64_encoded_data
        if item["hinh_anh2"]:
            with open(item["hinh_anh2"], "rb") as file:
                data = file.read()
                base64_encoded_data = base64.b64encode(data).decode("utf-8")
                item["hinh_anh2"] = base64_encoded_data
        if item["hinh_anh3"]:
            with open(item["hinh_anh3"], "rb") as file:
                data = file.read()
                base64_encoded_data = base64.b64encode(data).decode("utf-8")
                item["hinh_anh3"] = base64_encoded_data
        if item["hinh_anh4"]:
            with open(item["hinh_anh4"], "rb") as file:
                data = file.read()
                base64_encoded_data = base64.b64encode(data).decode("utf-8")
                item["hinh_anh4"] = base64_encoded_data
     # Trả về dạng Json
     return Response(serializers.data)

@api_view(['GET'])
def getFish_special(request):
     # Lấy dữ liệu từ database
     fishes = CA_BETTA.objects.filter(dac_biet=True)
     # Chuyển từ dạng Queryset sang định dạng Json, many = True vì có nhiều dòng dữ liệu
     serializers = CA_BETTA_Serializer(fishes, many=True)
     # Mã hóa hình ảnh trước khi gửi
     for item in serializers.data:        
        if item["hinh_anh1"]:
            with open(item["hinh_anh1"], "rb") as file:
                data = file.read()
                base64_encoded_data = base64.b64encode(data).decode("utf-8")
                item["hinh_anh1"] = base64_encoded_data
        if item["hinh_anh2"]:
            with open(item["hinh_anh2"], "rb") as file:
                data = file.read()
                base64_encoded_data = base64.b64encode(data).decode("utf-8")
                item["hinh_anh2"] = base64_encoded_data
        if item["hinh_anh3"]:
            with open(item["hinh_anh3"], "rb") as file:
                data = file.read()
                base64_encoded_data = base64.b64encode(data).decode("utf-8")
                item["hinh_anh3"] = base64_encoded_data
        if item["hinh_anh4"]:
            with open(item["hinh_anh4"], "rb") as file:
                data = file.read()
                base64_encoded_data = base64.b64encode(data).decode("utf-8")
                item["hinh_anh4"] = base64_encoded_data
     # Trả về dạng Json
     return Response(serializers.data)

# Thực hiện mua cá - dọn giỏ hàng
     # Nhận thông tin giỏ hàng - thực hiện insertion
@api_view(['POST'])
def addCart(request):
     ma_ca = request.data.get('ma_ca')
     ma_thucan = request.data.get('ma_thucan')
     gia = request.data.get('gia')
     so_luong_ca = request.data.get('so_luong_ca')
     so_luong_ta = request.data.get('so_luong_thucan')
     ma_tai_khoan = request.data.get('ma_tai_khoan')
     # Lấy mã giỏ hàng
     user_id = GIOHANG.objects.get(ma_tai_khoan=ma_tai_khoan)
     try:
          # Lấy tên tên cá
          fish_name = CA_BETTA.objects.get(ma_ca=ma_ca)
          
          # Kiểm tra cá đã tồn tại trong giỏ hàng
          check_fish = GIOHANG_CA.objects.filter(ca_betta=fish_name, giohang=user_id)
     except CA_BETTA.DoesNotExist:
          pass

     try:
          # Lấy tên thức ăn
          food_name = THUCAN.objects.get(ma_thucan=ma_thucan)
          
          # Kiểm tra thức ăn đã tồn tại trong giỏ hàng
          check_food = GIOHANG_THUCAN.objects.filter(thucan=food_name, giohang=user_id)
     except THUCAN.DoesNotExist:
          pass

     if not ma_ca and not ma_thucan:
          return Response({'success': False})
     else:
          if ma_ca and not check_fish:
               so_luong_ton = CA_BETTA.objects.get(ma_ca=ma_ca).so_luong
               if so_luong_ca > so_luong_ton:
                    return Response({'success': False, 'message': 'vượt quá số lượng tồn'})
               # Thêm cá vào GIOHANG_CA
               new_giohang_ca = GIOHANG_CA.objects.create(
                    giohang = user_id,
                    ca_betta = fish_name,
                    so_luong = so_luong_ca,
                    gia = gia,
               )
               new_giohang_ca.save()

               taikhoan = TAIKHOAN.objects.get(ma_tai_khoan=ma_tai_khoan)
               giohang = GIOHANG.objects.get(ma_tai_khoan=taikhoan)
               giohang_ca = GIOHANG_CA.objects.filter(giohang=giohang)
               giohang_thucan = GIOHANG_THUCAN.objects.filter(giohang=giohang)
               
               serializer1 = GIOHANG_CA_Serializer(giohang_ca, many=True)     
               serializer2 = GIOHANG_THUCAN_Serializer(giohang_thucan, many=True)
               # Mã hóa hình ảnh trước khi gửi
               for item in serializer1.data:      
                    if item["ca_betta_info"]["hinh_anh1"]:
                         with open(item["ca_betta_info"]["hinh_anh1"], "rb") as file:
                              data = file.read()
                              base64_encoded_data = base64.b64encode(data).decode("utf-8")
                              item["ca_betta_info"]["hinh_anh1"] = base64_encoded_data

               merged_data = {'giohang_ca': serializer1.data, 'giohang_thucan': serializer2.data}

               return Response({'data': merged_data})
          elif ma_ca and check_fish:
               return Response({'success': False, 'message': 'cá đã tồn tại'})
          
          elif ma_thucan and not check_food:
               so_luong_ton = THUCAN.objects.get(ma_thucan=ma_thucan).so_luong
               if so_luong_ta > so_luong_ton:
                    return Response({'success': False, 'message': 'vượt quá số lượng tồn'})
               # Thêm thức ăn vào GIOHANG_THUCAN
               new_giohang_thucan = GIOHANG_THUCAN.objects.create(
                    giohang = user_id,
                    thucan = food_name,
                    so_luong = so_luong_ta,
                    gia = gia,
               )
               new_giohang_thucan.save()

               taikhoan = TAIKHOAN.objects.get(ma_tai_khoan=ma_tai_khoan)
               giohang = GIOHANG.objects.get(ma_tai_khoan=taikhoan)
               giohang_ca = GIOHANG_CA.objects.filter(giohang=giohang)
               giohang_thucan = GIOHANG_THUCAN.objects.filter(giohang=giohang)
               
               serializer1 = GIOHANG_CA_Serializer(giohang_ca, many=True)     
               serializer2 = GIOHANG_THUCAN_Serializer(giohang_thucan, many=True)

               merged_data = {'giohang_ca': serializer1.data, 'giohang_thucan': serializer2.data}

               return Response({'data': merged_data})
          elif ma_thucan and check_food:
               return Response({'success': False, 'message': 'thức ăn đã tồn tại'})
          else:
               return Response({'success': False})
     
# Xóa một GIOHANG_CA
@api_view(['POST'])
def removeCart(request):
     ma_tai_khoan = request.data.get('ma_tai_khoan')
     ma_item = request.data.get('ma_item')
     loai_item = request.data.get('loai_item')

     if loai_item != "thucan":
          # Lấy GIOHANG_CA instance
          tai_khoan = GIOHANG.objects.get(ma_tai_khoan=ma_tai_khoan)
          fish_name_remove = CA_BETTA.objects.get(ma_ca=ma_item)
          giohang_ca_instance = GIOHANG_CA.objects.get(ca_betta=fish_name_remove, giohang=tai_khoan)
          giohang_ca_instance.delete()

          return Response({'success': True, 'message': 'Xóa thành công sản phẩm!'})
     
     if loai_item != "ca":
          # Lấy GIOHANG_THUCAN instance
          tai_khoan = GIOHANG.objects.get(ma_tai_khoan=ma_tai_khoan)
          food_name_remove = THUCAN.objects.get(ma_thucan=ma_item)
          giohang_thucan_instance = GIOHANG_THUCAN.objects.get(thucan=food_name_remove, giohang=tai_khoan)
          giohang_thucan_instance.delete()

          return Response({'success': True, 'message': 'Xóa thành công sản phẩm!'})
     
# Cập nhật GIOHANG_CA - khi có thay đổi trong giỏ hàng
@api_view(['POST'])
def updateCart(request):
     ma_tai_khoan = request.data.get('ma_tai_khoan')
     ma_ca = request.data.get('ma_ca')
     ma_thucan = request.data.get('ma_thucan')
     action = request.data.get('increase')
     if ma_ca != None:
          # Tăng số lượng cá
          if action == True:
               tai_khoan = GIOHANG.objects.get(ma_tai_khoan=ma_tai_khoan)
               fish_name_update = CA_BETTA.objects.get(ma_ca=ma_ca)
               soluong = GIOHANG_CA.objects.get(ca_betta=fish_name_update, giohang=tai_khoan)
               
               if soluong.so_luong >= fish_name_update.so_luong:
                    return Response({'success': False, 'message': 'vượt số lượng tồn'})
               
               soluong.so_luong += 1

               soluong.save()
               return Response({'success': True})
          
          # Giảm số lượng cá
          elif action == False:
               tai_khoan = GIOHANG.objects.get(ma_tai_khoan=ma_tai_khoan)
               fish_name_update = CA_BETTA.objects.get(ma_ca=ma_ca)
               soluong = GIOHANG_CA.objects.get(ca_betta=fish_name_update, giohang=tai_khoan)

               if soluong.so_luong == 0:
                    return Response({'success': False})
               else:
                    soluong.so_luong -= 1
                    if soluong.so_luong == 0:
                         soluong.delete()
                    else:
                         soluong.save()
               
               return Response({'success': True})
          
     if ma_thucan != None:
          # Tăng số lượng thức ăn
          if action == True:
               tai_khoan = GIOHANG.objects.get(ma_tai_khoan=ma_tai_khoan)
               food_name_update = THUCAN.objects.get(ma_thucan=ma_thucan)
               soluong = GIOHANG_THUCAN.objects.get(thucan=food_name_update, giohang=tai_khoan)

               if soluong.so_luong >= food_name_update.so_luong:
                    return Response({'success': False, 'message': 'vượt số lượng tồn'})
               
               soluong.so_luong += 1

               soluong.save()
               return Response({'success': True})
          
          # Giảm số lượng thức ăn
          elif action == False:
               tai_khoan = GIOHANG.objects.get(ma_tai_khoan=ma_tai_khoan)
               food_name_update = THUCAN.objects.get(ma_thucan=ma_thucan)
               soluong = GIOHANG_THUCAN.objects.get(thucan=food_name_update, giohang=tai_khoan)
               
               if soluong.so_luong == 0:
                    return Response({'success': False})
               else:
                    soluong.so_luong -= 1
                    if soluong.so_luong == 0:
                         soluong.delete()
                    else:
                         soluong.save()
               
               return Response({'success': True})
     
# Truy vấn giỏ hàng - dành cho việc sau khi đăng nhập/ đăng xuất
@api_view(['POST'])
def selectCart(request):
     ma_tai_khoan = request.data.get('ma_tai_khoan')
     if ma_tai_khoan == None:
          return Response({'success': False})
     
     taikhoan = TAIKHOAN.objects.get(ma_tai_khoan=ma_tai_khoan)
     giohang = GIOHANG.objects.get(ma_tai_khoan=taikhoan)
     giohang_ca = GIOHANG_CA.objects.filter(giohang=giohang)
     giohang_thucan = GIOHANG_THUCAN.objects.filter(giohang=giohang)

     serializer1 = GIOHANG_CA_Serializer(giohang_ca, many=True)
     data1 = serializer1.data
     # Mã hóa hình ảnh trước khi gửi
     for item in data1:        
          if item["ca_betta_info"]["hinh_anh1"]:
               with open(item["ca_betta_info"]["hinh_anh1"], "rb") as file:
                    data = file.read()
                    base64_encoded_data = base64.b64encode(data).decode("utf-8")
                    item["ca_betta_info"]["hinh_anh1"] = base64_encoded_data        
          if item["ca_betta_info"]["hinh_anh2"]:
               with open(item["ca_betta_info"]["hinh_anh2"], "rb") as file:
                    data = file.read()
                    base64_encoded_data = base64.b64encode(data).decode("utf-8")
                    item["ca_betta_info"]["hinh_anh2"] = base64_encoded_data        
          if item["ca_betta_info"]["hinh_anh3"]:
               with open(item["ca_betta_info"]["hinh_anh3"], "rb") as file:
                    data = file.read()
                    base64_encoded_data = base64.b64encode(data).decode("utf-8")
                    item["ca_betta_info"]["hinh_anh3"] = base64_encoded_data        
          if item["ca_betta_info"]["hinh_anh4"]:
               with open(item["ca_betta_info"]["hinh_anh4"], "rb") as file:
                    data = file.read()
                    base64_encoded_data = base64.b64encode(data).decode("utf-8")
                    item["ca_betta_info"]["hinh_anh4"] = base64_encoded_data        
     serializer2 = GIOHANG_THUCAN_Serializer(giohang_thucan, many=True)
     
     return Response({'success': True, 'data1': data1, 'data2': serializer2.data})

# api for logging in
@api_view(['POST'])
def logIn(request):
     username = request.data.get('username')
     password = request.data.get('password')

     try:
          account = TAIKHOAN.objects.get(ten_tai_khoan=username, mat_khau=password)
          if account.is_actived:     
               return Response({'success': True, 'message': 'Đăng nhập thành công!', 'isAdmin': account.is_admin,
                              'isLoggedIn': account.is_customer, 'ma_tai_khoan': account.ma_tai_khoan})
          else:
               return Response({'success': False, 'message': 'Tài khoản chưa được xác nhận!'})
     except:
          return Response({'success': False, 'message': 'Đăng nhập thất bại!'})

# api for signing up     
@api_view(['POST'])
def signUp(request):

     if request.data.get('is_first_request', False):
          username = request.data.get('username')
          password = request.data.get('password')
          fullname = request.data.get('fullname')
          email = request.data.get('email')
          phone_number = request.data.get('phone_number')
          address = request.data.get('address')

          # Kiểm tra email có tồn tại
          # is_exists = validate_email(email_address=email,  smtp_from_address='my@from.addr.ess', smtp_helo_host='my.host.name')
          # if is_exists == True: print('Email is found !!!')
          # else: 
          #      print('Email is not found !!!')
          #      return Response({'success': False, 'message': 'Email is not found !!!'})
          
          try:
               account = TAIKHOAN.objects.filter(ten_tai_khoan=username)
               if account:
                    return Response({'success': False, 'message': 'USERNAME đã tồn tại!'})
               
               email_used = NGUOIDUNG.objects.filter(email=email)
               if email_used:
                    return Response({'success': False, 'message': 'Email đã được sử dụng trên tài khoản khác'})
               
               phone_used = NGUOIDUNG.objects.filter(sdt=phone_number)
               if phone_used:
                    return Response({'success': False, 'message': 'Số điện thoại đã được sử dụng trên tài khoản khác'})

          except TAIKHOAN.DoesNotExist:
               pass
          
          verification_token=secrets.token_urlsafe(32)
          token = {'token': verification_token}

          cache_key = f'signup_data_{verification_token}'
          cache.set(cache_key, token, timeout=300)

          ok = send_mail(
               'Verify Your Email',
               f'Click the following link to verify your email: http://localhost:3000/signup?token={verification_token}',
               'anhkiet.nguyen798@gmail.com',
               [request.data['email']],
               fail_silently=False,
               )
          
          if ok:
               new_account = TAIKHOAN.objects.create(
                    is_admin = False,
                    is_customer = True,
                    is_actived = False,
                    ten_tai_khoan = username,
                    tai_khoan = username,
                    mat_khau = password,
                    verification_token=verification_token,
               )
               new_account.save()

               new_user = NGUOIDUNG.objects.create(
                    ho_ten = fullname,
                    dia_chi = address,
                    sdt = phone_number,
                    email = email,
                    tai_khoan = new_account,
               )
               new_user.save()
               
               return Response({'success': True, 'message': 'Đăng ký thành công!'})
          else: 
               return Response({'success': False, 'message': 'Đăng ký thất bại. Email không tồn tại!'})
     
     elif request.data.get('activate', False):

          cache_key = f'signup_data_{request.data["token"]}'
          cached_data = cache.get(cache_key)

          if not cached_data:
               return Response({'success': False, 'message': 'Cached data not found or expired.'})

          try:
               verification_token = cached_data.get('token')

               activate_account = TAIKHOAN.objects.get(verification_token = verification_token)
               if activate_account:
                    activate_account.is_actived = True
                    activate_account.save()
                    return Response({'success': True, 'message': 'Tài khoản kích hoạt thành công!'})
               else:
                    return Response({'success': False, 'message': 'Tài khoản đã bị xoá trước khi được kích hoạt!'})
          except:
               return Response({'success': False, 'message': 'Lỗi hệ thống!!!'})





# API for create payment link
@api_view(['POST'])
def create_payment_link(request):
     try:
          # Get data for payment 
          total_price = request.data.get('total_price')
          # total_price = request.data.get("totalPrice")
          # Data for create payment link
          import json
          import uuid
          import requests
          import hmac
          import hashlib
          # parameters send to MoMo get get payUrl
          endpoint = "https://test-payment.momo.vn/v2/gateway/api/create"
          accessKey = "F8BBA842ECF85"
          secretKey = "K951B6PE1waDMi640xX08PD3vg6EkVlz"
          orderInfo = "pay with MoMo"
          partnerCode = "MOMO"
          redirectUrl = "https://webhook.site/b3088a6a-2d17-4f8d-a383-71389a6c600b"
          ipnUrl = "https://6e3d-2001-ee0-d708-eb50-fffc-a6c6-6bac-a01a.ngrok-free.app/getNotification/"
          amount = str(total_price)
          orderId = str(uuid.uuid4())
          requestId = str(uuid.uuid4())
          extraData = ""  # pass empty value or Encode base64 JsonString
          partnerName = "MoMo Payment"
          requestType = "payWithMethod"
          storeId = "Test Store"
          orderGroupId = ""
          autoCapture = True
          lang = "vi"
          orderGroupId = ""
          # before sign HMAC SHA256 with format: accessKey=$accessKey&amount=$amount&extraData=$extraData&ipnUrl=$ipnUrl
          # &orderId=$orderId&orderInfo=$orderInfo&partnerCode=$partnerCode&redirectUrl=$redirectUrl&requestId=$requestId
          # &requestType=$requestType
          rawSignature = "accessKey=" + accessKey + "&amount=" + amount + "&extraData=" + extraData + "&ipnUrl=" + ipnUrl + "&orderId=" + orderId \
                         + "&orderInfo=" + orderInfo + "&partnerCode=" + partnerCode + "&redirectUrl=" + redirectUrl\
                         + "&requestId=" + requestId + "&requestType=" + requestType
          # puts raw signature
          print("--------------------RAW SIGNATURE----------------")
          print(rawSignature)
          # signature
          h = hmac.new(bytes(secretKey, 'ascii'), bytes(rawSignature, 'ascii'), hashlib.sha256)
          signature = h.hexdigest()
          print("--------------------SIGNATURE----------------")
          print(signature)
          # json object send to MoMo endpoint
          data = {
               'partnerCode': partnerCode,
               'orderId': orderId,
               'partnerName': partnerName,
               'storeId': storeId,
               'ipnUrl': ipnUrl,
               'amount': amount,
               'lang': lang,
               'requestType': requestType,
               'redirectUrl': redirectUrl,
               'autoCapture': autoCapture,
               'orderInfo': orderInfo,
               'requestId': requestId,
               'extraData': extraData,
               'signature': signature,
               'orderGroupId': orderGroupId
          }
          # Convert to JSON file
          data = json.dumps(data)
          # Send link create to MOMO
          response = requests.post(endpoint, data=data, headers={'Content-Type': 'application/json', 'Content-Length': str(len(data))})
          # Check response from MOMO
          if response.status_code == 200:
               result = response.json()               
               if result['resultCode'] == 0:
                    # Trả về link thanh toán nếu thành công
                    return Response({'success': True, 'result': result, 'message': result["message"]})
               else:
                    return Response({'success': False, 'error': result["message"]})
          else:
               return Response({'success': False, 'error': 'Request failed', 'details': response.text})
     except Exception as e:
          print(e)
          return Response({'success': False, 'error': str(e)})

from channels.layers import get_channel_layer
from rest_framework.response import Response
from adrf.views import APIView
import asyncio
# # For receive MOMO response
class GetNotificationView(APIView):
     async def post(self, request):
          order_id = request.data.get("orderId")
          status = request.data.get("status")
          message = request.data.get("message")     
          
          print("MOMO response for Order Id: ", order_id)

          if status is None and message == "Successful.":
               status = "success"

          if status == "success":
               print(f"Payment for Order {order_id} was successful.")
          else:
               print(f"Payment for Order {order_id} failed or has an issue.")

          channel_layer = get_channel_layer()
          group_name = f"payment_{order_id}"

          # Wait for send information to websocket          
          await channel_layer.group_send(
               group_name,
               {
                    'type': 'payment_status_update',
                    'status': status,
                    'message': message,
               }
          )

          # Trả về Response đồng bộ sau khi hoàn thành các tác vụ bất đồng bộ
          return Response({"details": request.data})






# api for check out
@api_view(['POST'])
def check_out(request):
     ma_ca = [x for x in request.data.get('ma_ca') if x != None]
     ma_thucan = [x for x in request.data.get('ma_thucan') if x != None]
     ma_tai_khoan = request.data.get('ma_tai_khoan')

     # Tạo tổng tiền & tổng số lượng
     tong_tien = float(0)
     tong_so_luong = int(0)

     # Lấy mã giỏ hàng
     user_id = GIOHANG.objects.get(ma_tai_khoan=ma_tai_khoan)

     # Xử lý cá
     for i in ma_ca:
          fish_name = CA_BETTA.objects.get(ma_ca=i)

          # Kiểm tra cá đã tồn tại trong giỏ hàng
          fish = GIOHANG_CA.objects.filter(ca_betta=fish_name, giohang=user_id)
          tong_so_luong += fish[0].so_luong
          tong_tien += float(fish[0].so_luong * fish[0].gia)
          # Cập nhật số lượng tồn
          fish_name.so_luong -= fish[0].so_luong
          fish_name.save()

     # Xử lý thức ăn
     for i in ma_thucan:
          food_name = THUCAN.objects.get(ma_thucan=i)

          # Kiểm tra cá đã tồn tại trong giỏ hàng
          food = GIOHANG_THUCAN.objects.filter(thucan=food_name, giohang=user_id)

          tong_so_luong += food[0].so_luong
          tong_tien += float(food[0].so_luong * food[0].gia)
          # Cập nhật số lượng tồn
          food_name.so_luong -= food[0].so_luong
          food_name.save()
     
     new_nguoi_dung = NGUOIDUNG.objects.get(tai_khoan=ma_tai_khoan)
     # Tạo hóa đơn
     new_hoa_don = HOADON.objects.create(
          ngay=timezone.now(),
          tong_sl_mua = tong_so_luong,
          tong_tien = tong_tien,
          ma_nguoi_dung=new_nguoi_dung
     )
     new_hoa_don.save()
     
     # Tạo cthd_ca và thêm từng hạng mục vào
     for i in ma_ca:
          fish_name = CA_BETTA.objects.get(ma_ca=i)


          fish = GIOHANG_CA.objects.filter(ca_betta=fish_name, giohang=user_id)
          new_cthds = CTHD_CA.objects.create(
               ma_hoa_don = new_hoa_don,
               ma_ca = fish_name,
               soluong = fish[0].so_luong,
          )

          # Xóa hết cá trong giỏ hàng
          fish.delete()
     
     # Tạo cthd_thucan và thêm từng hạng mục vào
     for i in ma_thucan:
          food_name = THUCAN.objects.get(ma_thucan=i)

          food = GIOHANG_THUCAN.objects.filter(thucan=food_name, giohang=user_id)

          new_cthds = CTHD_THUCAN.objects.create(
               ma_hoa_don = new_hoa_don,
               ma_thucan = food_name,
               soluong = food[0].so_luong,
          )

          # Xóa hết cá trong giỏ hàng
          food.delete()

     # Trả phản hồi     
     return Response({'success': True, 'message': 'Đã tạo hóa đơn!', 'ma_hoa_don': new_hoa_don.ma_hoa_don})

@api_view(['GET'])
def export_hoadon_pdf(request, ma_hoa_don):
    
     # Lấy đối tượng HOADON từ cơ sở dữ liệu
     hoadon = get_object_or_404(HOADON, ma_hoa_don=ma_hoa_don)
     ma_nguoi_dung_str = str(hoadon.ma_nguoi_dung)
     ma_nguoi_dung_lst = list(ma_nguoi_dung_str.split(' - '))
     user_id = int(ma_nguoi_dung_lst[0])

     nguoidung = NGUOIDUNG.objects.get(ma_nguoi_dung=user_id)     
     
     # Lấy các đối tượng cá trong cthd thuộc về hóa đơn (tên + số lượng)
     fish_dict = {}
     cthd_id = CTHD_CA.objects.filter(ma_hoa_don=ma_hoa_don).values('ma_ca', 'soluong')
     index_ca = 0
     for i in cthd_id:
          info_list = []          
          # Lấy tên cá
          fish_name = CA_BETTA.objects.filter(ma_ca=i['ma_ca']).values('ten_ca')
          info_list.append(fish_name[0]['ten_ca'])
          # Lấy số lượng mua
          info_list.append(i['soluong'])
          # Đánh số thứ tự
          info_list.append(index_ca)
          index_ca += 1

          fish_dict[i['ma_ca']] = info_list

     # Lấy các đối tượng thức ăn trong cthd thuộc về hóa đơn (tên + số lượng)
     food_dict = {}
     cthd_food = CTHD_THUCAN.objects.filter(ma_hoa_don=ma_hoa_don).values('ma_thucan', 'soluong')
     index_thucan = 0
     for i in cthd_food:
          info_list = []
          # Lấy tên thức ăn
          food_name = THUCAN.objects.filter(ma_thucan=i['ma_thucan']).values('ten_thucan')
          info_list.append(food_name[0]['ten_thucan'])
          # Lấy số lượng mua
          info_list.append(i['soluong'])
          # Đánh số thứ tự
          info_list.append(index_thucan)
          index_thucan += 1

          food_dict[i['ma_thucan']] = info_list
     
     # In hóa đơn
     # Tạo đối tượng HttpResponse với kiểu nội dung là application/pdf
     response = HttpResponse(content_type='application/pdf')

     # Thiết lập header để tạo tên file khi tải về
     response['Content-Disposition'] = f'attachment; filename="hoadon_{ma_hoa_don}.pdf"'

     # Đường dẫn đến font trên hệ thống
     font_path = 'D:/UIT/HK I 2023-2024/SE347.O11/UIT/web_app/new_version/backend/fonts/times.ttf'
     # Đăng ký font
     pdfmetrics.registerFont(TTFont('times', font_path))

     # Tạo đối tượng PDF sử dụng ReportLab
     p = canvas.Canvas(response)
     p.setFont("times", 12)
     
     # Vẽ nội dung PDF từ dữ liệu
     p.drawString(100, 800, f'THÔNG TIN NGƯỜI DÙNG')
     p.drawString(100, 780, f'Họ tên: {nguoidung.ho_ten}')
     p.drawString(100, 760, f'Địa chỉ: {nguoidung.dia_chi}')
     p.drawString(100, 740, f'Số điện thoại: {nguoidung.sdt}')

     p.drawString(100, 680, f'THÔNG TIN HÓA ĐƠN')
     p.drawString(100, 660, f'Mã hóa đơn: {hoadon.ma_hoa_don}')
     p.drawString(100, 640, f'Ngày: {hoadon.ngay}')
     p.drawString(100, 620, f'Tình trạng: {hoadon.get_tinh_trang_display()}')
     p.drawString(100, 600, f'Tổng số lượng mua: {hoadon.tong_sl_mua}')
     p.drawString(100, 580, f'Tổng tiền: {hoadon.tong_tien}')
     p.showPage()     
     # Đặt lại cài đặt font cho trang mới
     p.setFont("times", 12)

     # Thêm thông tin từng cá mua vào pdf - thêm vào trang sau
     count_ca = 0
     count_stt_ca = 0
     while count_ca < index_ca:
          p.drawString(100, 800, f'CHI TIẾT CÁ')
          p.drawString(100, 750, f'TÊN CÁ')
          p.drawString(450, 750, f'SỐ LƯỢNG')
          default_line = 700
          for ten_ca, so_luong, stt in fish_dict.values():
               if stt == count_stt_ca:
                    p.drawString(100, default_line, f'{ten_ca}')
                    p.drawString(500, default_line, f'{so_luong}')
                    default_line -= 20
                    count_ca += 1
                    count_stt_ca += 1
                    if count_ca == index_ca:
                         break
                    if default_line <= 100:
                         p.showPage()
                         # Đặt lại cài đặt font cho trang mới
                         p.setFont("times", 12)
                         break
     
     # In hết thông tin cá = chuyển qua in thông tin thức ăn
     if index_ca != 0:
          p.showPage()
          # Đặt lại cài đặt font cho trang mới
          p.setFont("times", 12)
     
     # Thêm thông tin thức ăn vào pdf
     count_thucan = 0
     count_stt_thucan = 0
     while count_thucan < index_thucan:
          p.drawString(100, 800, f'CHI TIẾT THỨC ĂN')
          p.drawString(100, 750, f'TÊN THỨC ĂN')
          p.drawString(450, 750, f'SỐ LƯỢNG')
          default_line = 700
          for ten_thucan, so_luong, stt in food_dict.values():
               if stt == count_stt_thucan:
                    p.drawString(100, default_line, f'{ten_thucan}')
                    p.drawString(500, default_line, f'{so_luong}')
                    default_line -= 20
                    count_thucan += 1
                    count_stt_thucan += 1
                    if count_thucan == index_thucan:
                         break
                    if default_line <= 100:
                         p.showPage()
                         # Đặt lại cài đặt font cho trang mới
                         p.setFont("times", 12)
                         break

     # In hết thông tin thức ăn thì hết trang và lưu pdf
     p.showPage()
     p.save()

     return response

@api_view(['POST'])
def getReports(request):
     month, year = request.data.get('month'), request.data.get('year')
     
     try:
          report_valid = BCDS.objects.filter(thang=month, nam=year)
          if report_valid:
               report_del = BCDS.objects.get(thang=month, nam=year)
               report_del.delete()

               report_upt = BCDS.objects.create(
                    thang = month,
                    nam = year,
               )
               report_upt.save()

               serializers = BCDS_Serializer(report_upt)
               return Response({'success': True, 'message': 'Đã tìm thấy BCDS', 'serializers': serializers.data})
          else:
               new_report = BCDS.objects.create(
               thang = month,
               nam = year,
               )
               new_report.save()

               serializers = BCDS_Serializer(new_report)

               return Response({'success': True, 'message': 'Đã tạo BCDS', 'serializers': serializers.data})
     except:
          return Response({'success': False, 'message': 'Lỗi hệ thống!!!'})

@api_view(['POST'])
def get_user_info(request):
     user_id = request.data.get('user_id')
     user = NGUOIDUNG.objects.get(ma_nguoi_dung=user_id)
     serializers = NGUOIDUNG_Serializer(user)

     # Trả về dạng Json
     return Response(serializers.data)

@api_view(['POST'])
def user_info(request):
     user_id = request.data.get('user_id')
     full_name = request.data.get('full_name')
     phone_number = request.data.get('phone_number')
     address = request.data.get('address')

     update_user = NGUOIDUNG.objects.get(ma_nguoi_dung=user_id)

     if full_name != '' and full_name != update_user.ho_ten:
          update_user.ho_ten = full_name

     if phone_number != '' and phone_number != update_user.sdt:
          update_user.sdt = phone_number

     if address != '' and address != update_user.dia_chi:
          update_user.dia_chi = address

     update_user.save()

     return Response({'success': True})

# Xử lý giỏ hàng yêu thích
@api_view(['POST'])
def select_wishlist(request):
     try:
          ma_tai_khoan = request.data.get('ma_tai_khoan')
          if ma_tai_khoan == None:
               return Response({'success': False})
          taikhoan = TAIKHOAN.objects.get(ma_tai_khoan=ma_tai_khoan)
          yeuthich = YEUTHICH.objects.get(ma_tai_khoan=taikhoan)
          yeuthich_danhmuc_ca = YEUTHICH_DANHMUC_CA.objects.filter(ma_yeuthich=yeuthich)

          yeuthich_danhmuc_thucan = YEUTHICH_DANHMUC_THUCAN.objects.filter(ma_yeuthich=yeuthich)

          serializer1 = YEUTHICH_DANHMUC_CA_Serializer(yeuthich_danhmuc_ca, many=True)
          data1 = serializer1.data
          # Mã hóa hình ảnh trước khi gửi
          for item in data1:      
               if item["ca_betta_info"]["hinh_anh1"]:
                    with open(item["ca_betta_info"]["hinh_anh1"], "rb") as file:
                         data = file.read()
                         base64_encoded_data = base64.b64encode(data).decode("utf-8")
                         item["ca_betta_info"]["hinh_anh1"] = base64_encoded_data
               # if item["ca_betta_info"]["hinh_anh2"]:
               #      with open(item["ca_betta_info"]["hinh_anh2"], "rb") as file:
               #           data = file.read()
               #           base64_encoded_data = base64.b64encode(data).decode("utf-8")
               #           item["ca_betta_info"]["hinh_anh2"] = base64_encoded_data
               # if item["ca_betta_info"]["hinh_anh3"]:
               #      with open(item["ca_betta_info"]["hinh_anh3"], "rb") as file:
               #           data = file.read()
               #           base64_encoded_data = base64.b64encode(data).decode("utf-8")
               #           item["ca_betta_info"]["hinh_anh3"] = base64_encoded_data
               # if item["ca_betta_info"]["hinh_anh4"]:
               #      with open(item["ca_betta_info"]["hinh_anh4"], "rb") as file:
               #           data = file.read()
               #           base64_encoded_data = base64.b64encode(data).decode("utf-8")
               #           item["ca_betta_info"]["hinh_anh4"] = base64_encoded_data
          serializer2 = YEUTHICH_DANHMUC_THUCAN_Serializer(yeuthich_danhmuc_thucan, many=True)
          merged_data = {'yeuthich_ca': data1, 'yeuthich_thucan': serializer2.data}

          # Sử dụng serializer tổng hợp để gộp cả hai serializer
          # Truy cập dữ liệu đã gộp bằng cách sử dụng data attribute
          return Response({'success': True, 'data': merged_data})
     except Exception as e:
          print(e)

@api_view(['POST'])
def add_wishlist(request):
     ma_tai_khoan = request.data.get('ma_tai_khoan')
     ma_ca = request.data.get('ma_ca')
     
     # Lấy YEUTHICH
     user_id = YEUTHICH.objects.get(ma_tai_khoan=ma_tai_khoan)

     # Lấy tên tên cá
     fish_name = CA_BETTA.objects.get(ma_ca=ma_ca)
     # Kiểm tra cá đã tồn tại trong wishlist hay không ?
     check_fish = YEUTHICH_DANHMUC_CA.objects.filter(ma_ca=fish_name, ma_yeuthich=user_id)
     if check_fish:
          return Response({'success': False, 'message': 'cá đã tồn tại'})
     else:
          # Thêm cá vào YEUTHICH_DANHMUC_CA
          new_yeuthich_ca = YEUTHICH_DANHMUC_CA.objects.create(
               ma_yeuthich = user_id,
               ma_ca = fish_name,
          )

          taikhoan = TAIKHOAN.objects.get(ma_tai_khoan=ma_tai_khoan)
          yeuthich = YEUTHICH.objects.get(ma_tai_khoan=taikhoan)
          yeuthich_danhmuc_ca = YEUTHICH_DANHMUC_CA.objects.filter(ma_yeuthich=yeuthich, ma_ca=ma_ca)
          serializer = YEUTHICH_DANHMUC_CA_Serializer(yeuthich_danhmuc_ca, many=True)
          # Mã hóa hình ảnh trước khi gửi
          for item in serializer.data:      
               if item["ca_betta_info"]["hinh_anh1"]:
                    with open(item["ca_betta_info"]["hinh_anh1"], "rb") as file:
                         data = file.read()
                         base64_encoded_data = base64.b64encode(data).decode("utf-8")
                         item["ca_betta_info"]["hinh_anh1"] = base64_encoded_data
          return Response(serializer.data)
     
     return Response({'success': True})

@api_view(['POST'])
def remove_wishlist(request):
     ma_tai_khoan = request.data.get('ma_tai_khoan')
     ma_ca = request.data.get('ma_ca')
     ma_thucan = request.data.get('ma_thucan')

     if ma_ca != None:
          # Lấy YEUTHICH_DANHMUC_CA instance
          tai_khoan = YEUTHICH.objects.get(ma_tai_khoan=ma_tai_khoan)
          fish_name_remove = CA_BETTA.objects.get(ma_ca=ma_ca)
          yeuthich_danhmuc_ca_instance = YEUTHICH_DANHMUC_CA.objects.get(ma_ca=fish_name_remove, ma_yeuthich=tai_khoan)
          yeuthich_danhmuc_ca_instance.delete()

          return Response({'success': True, 'message': 'Xóa thành công sản phẩm!'})
     
     if ma_thucan != None:
          # Lấy YEUTHICH_DANHMUC_THUCAN instance
          tai_khoan = YEUTHICH.objects.get(ma_tai_khoan=ma_tai_khoan)
          food_name_remove = THUCAN.objects.get(ma_thucan=ma_thucan)
          yeuthich_danhmuc_thucan_instance = YEUTHICH_DANHMUC_THUCAN.objects.get(ma_thucan=food_name_remove, ma_yeuthich=tai_khoan)
          yeuthich_danhmuc_thucan_instance.delete()

          return Response({'success': True, 'message': 'Xóa thành công sản phẩm!'})

# Xử lý mua bán rong rêu, thức ăn
@api_view(['GET'])
def getFoods(request):
     # Lấy dữ liệu từ database
     foods = THUCAN.objects.all()
     # Chuyển từ dạng Queryset sang định dạng Json, many = True vì có nhiều dòng dữ liệu
     serializers = THUCAN_Serializer(foods, many=True)
     # Trả về dạng Json
     return Response({'success': True, 'data': serializers.data})

# Lấy một thức ăn theo ma_thucan
@api_view(['POST'])
def get_one_food(request):
     ma_thucan = request.data.get('ma_thucan')
     thucan = THUCAN.objects.get(ma_thucan=ma_thucan)
     serializers = THUCAN_Serializer(thucan, many=False)
     return Response({'success': True, 'data': serializers.data})

# Thêm thức ăn vào danh mục yêu thích 
@api_view(['POST'])
def add_food_wishlist(request):
     ma_tai_khoan = request.data.get('ma_tai_khoan')

     ma_thucan = request.data.get('ma_thucan')

     # Lấy YEUTHICH
     user_id = YEUTHICH.objects.get(ma_tai_khoan=ma_tai_khoan)

     # Lấy tên tên cá
     food_name = THUCAN.objects.get(ma_thucan=ma_thucan)
     # Kiểm tra cá đã tồn tại trong wishlist hay không ?
     check_food = YEUTHICH_DANHMUC_THUCAN.objects.filter(ma_thucan=food_name, ma_yeuthich=user_id)
     if check_food:
          return Response({'success': False, 'message': 'thức ăn đã tồn tại'})
     else:
          # Thêm cá vào YEUTHICH_DANHMUC_CA
          new_yeuthich_thucan = YEUTHICH_DANHMUC_THUCAN.objects.create(
               ma_yeuthich = user_id,
               ma_thucan = food_name,
          )

          taikhoan = TAIKHOAN.objects.get(ma_tai_khoan=ma_tai_khoan)
          yeuthich = YEUTHICH.objects.get(ma_tai_khoan=taikhoan)
          yeuthich_danhmuc_thucan = YEUTHICH_DANHMUC_THUCAN.objects.filter(ma_yeuthich=yeuthich, ma_thucan=ma_thucan)
          serializer = YEUTHICH_DANHMUC_THUCAN_Serializer(yeuthich_danhmuc_thucan, many=True)
          return Response(serializer.data)
