import os
from django.db import models
from django.urls import reverse
import operator
# Create your models here.

# Table 1
class LOAICA(models.Model):
     ma_loai_ca = models.AutoField(primary_key=True)
     ten_loai_ca = models.TextField()

     def __str__(self):
          return f'{str(self.ma_loai_ca)} - {self.ten_loai_ca}'

# Table 2
class CA_BETTA(models.Model):
     class Gioitinh(models.TextChoices):
          Duc = ('M', 'đực')
          Cai = ('F', 'cái')
     ma_ca = models.AutoField(primary_key=True)
     ten_ca = models.TextField()
     gioi_tinh = models.CharField(max_length=1, choices=Gioitinh.choices, default=Gioitinh.Duc)
     gia = models.DecimalField(max_digits=8, decimal_places=2)
     hinh_anh1 = models.CharField(max_length=300, blank=True, null=True)
     hinh_anh2 = models.CharField(max_length=300, blank=True, null=True)
     hinh_anh3 = models.CharField(max_length=300, blank=True, null=True)
     hinh_anh4 = models.CharField(max_length=300, blank=True, null=True)
     ma_loai_ca = models.ForeignKey('LOAICA', on_delete=models.CASCADE)
     dac_biet = models.BooleanField(default=False)
     so_luong = models.IntegerField(null=True)

     def __str__(self):
          return f'{str(self.ma_loai_ca)} - {self.ten_ca}'

# Table 3
class TAIKHOAN(models.Model):
     ma_tai_khoan = models.AutoField(primary_key=True)
     is_admin = models.BooleanField(default=False)
     is_customer = models.BooleanField(default=False)
     is_actived = models.BooleanField(default=False)
     ten_tai_khoan = models.TextField(blank=True, null=True)
     tai_khoan = models.TextField(blank=True, null=True)
     mat_khau = models.TextField(blank=True, null=True)
     
     # status = models.BooleanField(default=False)
     verification_token = models.CharField(max_length=255, blank=True, null=True)

     def __str__(self):
          return f'{self.ma_tai_khoan} - {self.ten_tai_khoan}'

# Table 4
class NGUOIDUNG(models.Model):
     ma_nguoi_dung = models.AutoField(primary_key=True)
     ho_ten = models.TextField()
     dia_chi = models.TextField(blank=True, null=True)
     sdt = models.CharField(max_length=12, blank=True, null=True)
     email = models.TextField(blank=True, null=True)
     tai_khoan = models.OneToOneField('TAIKHOAN', blank=True, null=True, on_delete=models.CASCADE)     
     
     def __str__(self):
          return f'{str(self.ma_nguoi_dung)} - {self.ho_ten}'

# Table 5
class GIOHANG(models.Model):
     class TinhTrang(models.TextChoices):
          dang_cho = ('1', 'Đang chờ')
          da_tiep_nhan = ('2', 'Đã tiếp nhận')
          hoan_tat = ('3', 'Hoàn tất')
     ma_tai_khoan = models.OneToOneField('TAIKHOAN', on_delete=models.CASCADE, primary_key=True)
     giohang_set = models.ManyToManyField('CA_BETTA', through='GIOHANG_CA')
     tinh_trang = models.CharField(max_length=1, choices=TinhTrang.choices, default=TinhTrang.dang_cho)

     def __str__(self):
          return f'Mã tài khoản {self.ma_tai_khoan}'

# Table 6
class GIOHANG_CA(models.Model):
    giohang = models.ForeignKey('GIOHANG', on_delete=models.CASCADE)
    ca_betta = models.ForeignKey('CA_BETTA', on_delete=models.CASCADE)
    so_luong = models.IntegerField()
    gia = models.DecimalField(max_digits=10, decimal_places=2)  # Assuming you want to store price as a decimal

    def __str__(self):
        return f'Mã tài khoản {self.giohang.ma_tai_khoan} - Mã cá {self.ca_betta.ma_ca} - Số lượng: {self.so_luong} - Giá: {self.gia}'

# Table 6.1
class GIOHANG_THUCAN(models.Model):
    giohang = models.ForeignKey('GIOHANG', on_delete=models.CASCADE)
    thucan = models.ForeignKey('THUCAN', on_delete=models.CASCADE)
    so_luong = models.IntegerField()
    gia = models.DecimalField(max_digits=10, decimal_places=2)  # Assuming you want to store price as a decimal

    def __str__(self):
        return f'Mã tài khoản {self.giohang.ma_tai_khoan} - Mã thức ăn {self.thucan.ma_thucan} - Số lượng: {self.so_luong} - Giá: {self.gia}'
    
# Table 7
class HOADON(models.Model):
     class TinhTrang(models.TextChoices):
          chua_thanh_toan = ('1', 'Chưa thanh toán')
          da_thanh_toan = ('2', 'Đã thanh toán')
     ma_hoa_don = models.AutoField(primary_key=True)
     ngay = models.DateField(auto_now_add=True)
     tinh_trang = models.CharField(max_length=1, choices=TinhTrang.choices, default=TinhTrang.chua_thanh_toan)
     tong_sl_mua = models.IntegerField(default=0)
     tong_tien = models.DecimalField(max_digits=10, decimal_places=2, default=0)
     ma_nguoi_dung = models.ForeignKey('NGUOIDUNG', on_delete=models.CASCADE)

     def __str__(self):
          return f'Hóa đơn {self.ma_hoa_don}  -  Ngày {self.ngay}'

# Table 8
class CTHD_CA(models.Model):
     ma_cthd = models.AutoField(primary_key=True)
     ma_hoa_don = models.ForeignKey('HOADON', on_delete=models.CASCADE)
     ma_ca = models.ForeignKey('CA_BETTA', on_delete=models.CASCADE)
     soluong = models.IntegerField(default=0)

     def __str__(self):
          return f'{str(self.ma_cthd)} - Hóa đơn {self.ma_hoa_don} - Mã cá {self.ma_ca}'

# Table 8.1
class CTHD_THUCAN(models.Model):
     ma_cthd = models.AutoField(primary_key=True)
     ma_hoa_don = models.ForeignKey('HOADON', on_delete=models.CASCADE)
     ma_thucan = models.ForeignKey('THUCAN', on_delete=models.CASCADE)
     soluong = models.IntegerField(default=0)

     def __str__(self):
          return f'{str(self.ma_cthd)} - Hóa đơn {self.ma_hoa_don} - Mã cá {self.ma_thucan}'
     
# Table 9
class BCDS(models.Model):
     ma_bcds = models.AutoField(primary_key=True)
     thang = models.IntegerField()
     nam = models.IntegerField()
     so_ca_ban_duoc = models.IntegerField(default=0)
     so_thuc_an_ban_duoc = models.IntegerField(default=0)
     doanh_thu = models.DecimalField(max_digits=10, decimal_places=2, default=0)
     most_fish = models.TextField(blank=True, null=True)
     most_food = models.TextField(blank=True, null=True)
     most_customer = models.TextField(blank=True, null=True)
     so_khach_mua_ca = models.IntegerField(default=0)
     so_luong_ca_best_seller = models.IntegerField(default=0)
     so_luong_thucan_best_seller = models.IntegerField(default=0)

     def __str__(self):
          return f'{self.thang}/{self.nam}'

# Table 10
class THUCAN(models.Model):
     class loai_thucan(models.TextChoices):
          lam_san = ('1', 'Đóng hộp')
          song = ('2', 'Không đóng hộp')
     ma_thucan = models.AutoField(primary_key=True)
     ten_thucan = models.TextField()
     gia = models.DecimalField(max_digits=10, decimal_places=2, default=0)
     so_luong = models.IntegerField(default=0)
     kg = models.DecimalField(max_digits=10, decimal_places=5, default=0)
     hinhanh1 = models.CharField(max_length=300, blank=True, null=True)
     hinhanh2 = models.CharField(max_length=300, blank=True, null=True)
     hinhanh3 = models.CharField(max_length=300, blank=True, null=True)

     def __str__(self):
          return f'{self.ma_thucan}  -  {self.ten_thucan}'

# Table 11
class YEUTHICH(models.Model):
     ma_tai_khoan = models.OneToOneField('TAIKHOAN', on_delete=models.CASCADE, primary_key=True)     
     yeuthich_set_betta = models.ManyToManyField('CA_BETTA', through='YEUTHICH_DANHMUC_CA')
     yeuthich_set_thucan = models.ManyToManyField('THUCAN', through='YEUTHICH_DANHMUC_THUCAN')

     def __str__(self):
          return f'{self.ma_tai_khoan}'

# Table 12
class YEUTHICH_DANHMUC_CA(models.Model):
     ma_yeuthich = models.ForeignKey('YEUTHICH', on_delete=models.CASCADE)
     ma_ca = models.ForeignKey('CA_BETTA', on_delete=models.CASCADE, null=True, blank=True)

     def __str__(self):
          return f'{self.ma_yeuthich}'
     
# Table 13
class YEUTHICH_DANHMUC_THUCAN(models.Model):
     ma_yeuthich = models.ForeignKey('YEUTHICH', on_delete=models.CASCADE)
     ma_thucan = models.ForeignKey('THUCAN', on_delete=models.CASCADE, null=True, blank=True)

     def __str__(self):
          return f'{self.ma_yeuthich}'
     
# Phần Signal
from django.db.models.signals import pre_save, post_save, pre_delete, post_delete
from django.dispatch import receiver

# Trigger tạo giohang tương ứng với tài khoản khi tạo tài khoản
@receiver(post_save, sender=TAIKHOAN)
def create_giohang_for_taikhoan(sender, instance, created, **kwargs):
     if created:
          GIOHANG.objects.create(ma_tai_khoan=instance)

post_save.connect(create_giohang_for_taikhoan, sender=TAIKHOAN)

# Trigger tạo yeuthich tương ứng với tài khoản khi tạo tài khoản
@receiver(post_save, sender=TAIKHOAN)
def create_yeuthich_for_taikhoan(sender, instance, created, **kwargs):
     if created:
          YEUTHICH.objects.create(ma_tai_khoan=instance)

post_save.connect(create_yeuthich_for_taikhoan, sender=TAIKHOAN)

# Trigger tự động tính tổng tiền (thêm mới)
@receiver(post_save, sender=CTHD_CA)
@receiver(post_save, sender=CTHD_THUCAN)
def calculate_post_total_money(sender, instance, created, **kwargs):
     mahoadon = instance.ma_hoa_don.ma_hoa_don
     # Xử lý chi tiết hóa đơn cá
     cthds_ca = CTHD_CA.objects.filter(ma_hoa_don=mahoadon)
     count_ca = 0
     total_money_ca = 0
     for item_ca in cthds_ca:
          giaca = CA_BETTA.objects.get(ma_ca=item_ca.ma_ca.ma_ca).gia * item_ca.soluong
          count_ca += item_ca.soluong
          total_money_ca += giaca

     # Xử lý chi tiết hóa đơn thức ăn
     cthds_thucan = CTHD_THUCAN.objects.filter(ma_hoa_don=mahoadon)
     count_thucan = 0
     total_money_thucan = 0
     for item_thucan in cthds_thucan:
          giaca = THUCAN.objects.get(ma_thucan=item_thucan.ma_thucan.ma_thucan).gia * item_thucan.soluong
          count_thucan += item_thucan.soluong
          total_money_thucan += giaca
     count = (count_ca + count_thucan)
     total_money = (total_money_ca + total_money_thucan)

     # Xử lý hóa đơn
     t = HOADON.objects.get(ma_hoa_don=mahoadon)
     t.tong_sl_mua = count
     t.tong_tien = total_money
     t.save()

     
# Trigger tự động tính tổng tiền (sau khi xóa một cthd)
@receiver(post_delete, sender=CTHD_CA)
@receiver(post_save, sender=CTHD_THUCAN)
def calculate_post_total_money_remove(sender, instance, **kwargs):
     mahoadon = instance.ma_hoa_don.ma_hoa_don
     # Xử lý cthd_ca
     cthds = CTHD_CA.objects.filter(ma_hoa_don=mahoadon)
     count_ca = 0
     total_money_ca = 0
     for item in cthds:
          giaca = CA_BETTA.objects.get(ma_ca=item.ma_ca.ma_ca).gia * item.soluong
          count_ca += item.soluong
          total_money_ca += giaca

     # Xử lý cthd_thucan
     cthds = CTHD_THUCAN.objects.filter(ma_hoa_don=mahoadon)
     count_thucan = 0
     total_money_thucan = 0
     for item in cthds:
          giaca = THUCAN.objects.get(ma_thucan=item.ma_thucan.ma_thucan).gia * item.soluong
          count_thucan += item.soluong
          total_money_thucan += giaca

     # Xử lý hóa đơn
     t = HOADON.objects.get(ma_hoa_don=mahoadon)
     t.tong_sl_mua = (count_ca + count_thucan)
     t.tong_tien = (total_money_ca + total_money_thucan)
     t.save()


# Trigger tính báo cáo doanh thu theo tháng
@receiver(pre_save, sender=BCDS)
def calculate_benefit_of_month(sender, instance ,**kwargs):
     mabcds = instance.ma_bcds
     month = instance.thang
     year = instance.nam

     receipt_id = HOADON.objects.filter(ngay__month=month, ngay__year=year, tinh_trang='1').values('ma_hoa_don')
     receipt_money = HOADON.objects.filter(ngay__month=month, ngay__year=year, tinh_trang='1').values('tong_tien')
     receipt_customer = HOADON.objects.filter(ngay__month=month, ngay__year=year, tinh_trang='1').values('ma_nguoi_dung')
     total_fish = 0 # Tổng số cá bán được
     total_food = 0 # Tổng số thức ăn cá bán được
     total_money = 0 # Tổng doanh thu

     # Lấy thông tin loại cá bán chạy nhất
     fish_dict = {}

     for i in list(receipt_id):
          fishes = CTHD_CA.objects.filter(ma_hoa_don=i['ma_hoa_don']).values('ma_ca', 'soluong')
          for j in list(fishes):
               if j['ma_ca'] in fish_dict:
                    fish_dict[j['ma_ca']] += j['soluong']
               else:
                    fish_dict[j['ma_ca']] = j['soluong']
               # Tổng số lượng cá bán được
               total_fish += j['soluong']
     
     best_seller_fish = max(fish_dict.items(), key=operator.itemgetter(1))[0]
     best_seller_fish_name = CA_BETTA.objects.filter(ma_ca=best_seller_fish).values('ten_ca')
     instance.most_fish = best_seller_fish_name[0]['ten_ca']
     instance.so_luong_ca_best_seller = max(fish_dict.items(), key=operator.itemgetter(1))[1]
     instance.so_ca_ban_duoc = total_fish

     # Lấy thông tin loại thức ăn cá bán chạy nhất
     food_dict = {}
     
     for i in list(receipt_id):
          foods = CTHD_THUCAN.objects.filter(ma_hoa_don=i['ma_hoa_don']).values('ma_thucan', 'soluong')
          for j in list(foods):
               if j['ma_thucan'] in food_dict:
                    food_dict[j['ma_thucan']] += j['soluong']
               else:
                    food_dict[j['ma_thucan']] = j['soluong']
               # Tổng số lượng thức ăn cá bán được
               total_food += j['soluong']

     best_seller_food = max(food_dict.items(), key=operator.itemgetter(1))[0]
     best_seller_food_name = THUCAN.objects.filter(ma_thucan=best_seller_food).values('ten_thucan')
     instance.most_food = best_seller_food_name[0]['ten_thucan']
     instance.so_luong_thucan_best_seller = max(food_dict.items(), key=operator.itemgetter(1))[1]
     instance.so_thuc_an_ban_duoc = total_food
     # Lấy thông tin khách hàng giao dịch nhiều nhất
     customer_dict = {}

     for i in list(receipt_customer):
          if i['ma_nguoi_dung'] in customer_dict:
               customer_dict[i['ma_nguoi_dung']] += 1
          else:
               customer_dict[i['ma_nguoi_dung']] = 1
     most_trade_customer = max(customer_dict.items(), key=operator.itemgetter(1))[0]
     most_trade_customer_name = NGUOIDUNG.objects.filter(ma_nguoi_dung=most_trade_customer).values('ho_ten')
     instance.most_customer = most_trade_customer_name[0]['ho_ten']

     # Tổng doanh thu
     for i in list(receipt_money):
          total_money += i['tong_tien']

     instance.doanh_thu = total_money

     # Tổng số khách hàng đã mua cá
     instance.so_khach_mua_ca = HOADON.objects.filter(ngay__month=month, ngay__year=year, tinh_trang='1').values('ma_nguoi_dung').distinct().count()
