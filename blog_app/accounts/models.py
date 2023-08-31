from django.contrib.auth import models as auth_models
from django.core.validators import MinLengthValidator
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.defaultfilters import slugify
from django.utils.translation import gettext_lazy as _
from PIL import Image

from blog_app.accounts.managers import BlogAppUserManager
from blog_app.accounts.validators import validate_letters_dash_only


class BlogAppUser(auth_models.AbstractBaseUser, auth_models.PermissionsMixin):
    '''
    The BlogAppUser extends the AbstractBaseUser and PermissionsMixin.

    It overwrites the AUTH_USER_MODEL = 'auth_app.AppUser' in settings.py
    to tell Django that there is a customer user model.

    Also, the user creation and change forms and
    their Meta-s were overwritten as they refer to the standard user model.

    The managers were taken from Django inner documentation and overwritten
    according to the specifics of the custom user.
    '''

    email = models.EmailField(_("email address"), unique=True)

    is_staff = models.BooleanField(_('staff status'), default=False,
                                   help_text=_('Designates whether the user can log into this admin '
                                               'site.'))
    is_active = models.BooleanField(_('active'), default=True,
                                    help_text=_('Designates whether this user should be treated as '
                                                'active. Unselect this instead of deleting accounts.'))

    date_joined = models.DateTimeField(
        auto_now_add=True,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = BlogAppUserManager()

    def __str__(self):
        return self.email

class Profile(models.Model):

    FIRST_NAME_MIN_LENGTH = 2
    FIRST_NAME_MAX_LENGTH = 40
    LAST_NAME_MIN_LENGTH = 2
    LAST_NAME_MAX_LENGTH = 60
    BIO_MAX_LENGTH = 1000
    BIO_MIN_LENGTH = 70

    first_name = models.CharField(
        max_length=FIRST_NAME_MAX_LENGTH,
        validators=(
            MinLengthValidator(FIRST_NAME_MIN_LENGTH),
            validate_letters_dash_only,
            )
        )

    last_name = models.CharField(
        max_length=LAST_NAME_MAX_LENGTH,
        validators=(
            MinLengthValidator(LAST_NAME_MIN_LENGTH),
            validate_letters_dash_only,
            )
        )


    bio = models.TextField(max_length=BIO_MAX_LENGTH,
                           validators = (MinLengthValidator(BIO_MIN_LENGTH),))

    image = models.ImageField(blank=True, null=True, default = 'accounts/default-avatar-profile-icon-of-social-media-user-vector.jpg', upload_to="accounts" )
    slug = models.SlugField(max_length=72, unique=True, null=False, blank=True)

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def generate_unique_slug(self):
        full_name_slug = slugify(self.full_name)
        base_slug = full_name_slug
        index = 1

        #handing the case when the full name is not unique
        while Profile.objects.filter(slug=self.slug).exists():
            self.slug = f"{base_slug}-{index}"
            index += 1

    def save(self, *args, **kwargs):
        if not self.slug:  # Only generate the slug if it's not already set
            self.slug = slugify(self.full_name)
            self.generate_unique_slug()
        super().save(*args, **kwargs)

        if self.image:  # Only process the image if it's not None
            image = Image.open(self.image.path)
            if image.height > 150 or image.width > 150:
                new_image_size = (150, 150)
                image.thumbnail(new_image_size)
                image.save(self.image.path)


    user = models.OneToOneField(
        BlogAppUser,
        on_delete=models.CASCADE,
        primary_key=True,
        )


    def __str__(self):
        return self.full_name

