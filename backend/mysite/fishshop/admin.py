from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import *

# Register your models here.
admin.site.register(LOAICA)
admin.site.register(NGUOIDUNG)
admin.site.register(TAIKHOAN)
admin.site.register(GIOHANG)
admin.site.register(GIOHANG_CA)
admin.site.register(GIOHANG_THUCAN)
admin.site.register(HOADON)
admin.site.register(CTHD_CA)
admin.site.register(CTHD_THUCAN)
admin.site.register(BCDS)
admin.site.register(THUCAN)
admin.site.register(YEUTHICH)
admin.site.register(YEUTHICH_DANHMUC_CA)
admin.site.register(YEUTHICH_DANHMUC_THUCAN)

class CA_BETTAAdmin(admin.ModelAdmin):
    list_display = ('ten_ca', 'gioi_tinh', 'gia', 'ma_loai_ca', 'display_image')

    def display_image(self, obj):
        return mark_safe(f'<img src="{obj.get_image_url()}" width="50" height="50" />')

    display_image.short_description = 'Hình ảnh'

admin.site.register(CA_BETTA)