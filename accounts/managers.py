from django.contrib.auth.base_user import BaseUserManager

class CustomUserManager(BaseUserManager):

    def create_user(self, phone, password=None, **extra_fields):
        phone = self.normalize_phone(phone)
        username = extra_fields.pop("username", phone)
        user = self.model(phone=phone, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password, **extra_fields):

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self.create_user(phone, password, **extra_fields)

    @classmethod
    def normalize_phone(cls, phone):
        phone = (phone or "").strip()
        if len(phone) != 11 or not phone.isdigit():
            raise ValueError('Phone number must be 11 digits')
        return phone
