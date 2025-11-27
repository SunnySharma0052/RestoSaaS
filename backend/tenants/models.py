from django.db import models
from django.utils.text import slugify
import qrcode
from io import BytesIO
from django.core.files.base import ContentFile


class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    address = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=15)
    logo = models.ImageField(upload_to='restaurant_logos/', blank=True, null=True)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Table(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='tables')
    table_number = models.CharField(max_length=10)

    # New: QR Code image file
    qr_code_image = models.ImageField(upload_to="qr_codes/", blank=True, null=True)

    # New: QR Link (auto generate)
    qr_code_link = models.URLField(blank=True, null=True)

    def save(self, *args, **kwargs):
        # ---- MAKE UNIQUE URL FOR QR ----
        self.qr_code_link = f"https://yourdomain.com/{self.restaurant.slug}/table-{self.table_number}"

        super().save(*args, **kwargs)

        # ---- GENERATE QR CODE IMAGE ----
        qr = qrcode.make(self.qr_code_link)
        buffer = BytesIO()
        qr.save(buffer, format="PNG")
        file_name = f"qr_{self.restaurant.slug}_table{self.table_number}.png"

        self.qr_code_image.save(file_name, ContentFile(buffer.getvalue()), save=False)

        # Save again to save the QR image
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.restaurant.name} - Table {self.table_number}"
