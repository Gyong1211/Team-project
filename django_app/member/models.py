from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from group.models import MyGroup
from group.tasks import task_update_num_of_member
from utils.fields import CustomImageField


class MyUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class MyUser(AbstractBaseUser, PermissionsMixin):
    """
    Email, password and nickname are required. Other fields are optional.
    """
    email = models.EmailField(_('이메일'), unique=True)
    username = models.CharField(_('이름'), max_length=12, blank=True)
    nickname = models.CharField(_('닉네임'), max_length=16, unique=True)
    profile_img = CustomImageField(
        upload_to='member',
        blank=True,
        default_static_image='images/no_profile.png'
    )
    is_staff = models.BooleanField(
        _('스태프 권한'),
        default=False,
        help_text=_('Admin page에 접속할 수 있는 권한을 부여합니다.'),
    )
    is_active = models.BooleanField(
        _('계정 활성화'),
        default=True,
        help_text=_(
            '계정을 삭제하지 않고 비활성화 시킬때 체크를 해제하십시오.'
        ),
    )
    date_joined = models.DateTimeField(_('가입일자'), default=timezone.now)
    relations = models.ManyToManyField(
        'self',
        through='UserRelation',
        symmetrical=False
    )
    group = models.ManyToManyField(
        MyGroup,
        through='Membership',
        related_name='member',
    )

    objects = MyUserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nickname']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ['-pk']

    def clean(self):
        super(MyUser, self).clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        "유저의 이름(실명)을 반환합니다."
        username = self.username
        return username.strip()

    def get_short_name(self):
        "유저의 닉네임을 반환합니다. (Django admin page에서 사용)"
        return self.nickname

    def follow(self, user):
        if not isinstance(user, MyUser):
            raise ValueError("'user' 는 반드시 MyUser 인자여야 합니다")
        self.following.get_or_create(
            to_user=user,
        )

    def unfollow(self, user):
        self.following.get(
            to_user=user,
        ).delete()

    def follow_toggle(self, user):
        relation, relation_created = self.following.get_or_create(to_user=user)
        if not relation_created:
            relation.delete()
        else:
            return relation

    def is_follow(self, user):
        # 해당 유저(self)가 입력받은 유저를 follow하고 있는지의 여부를 Boolean 값으로 반환
        return self.following.filter(to_user=user).exists()

    def is_follower(self, user):
        # 해당 유저(self)가 입력받은 유저의 follower인지 여부를 Boolean 값으로 반환
        return self.follower.filter(from_user=user).exists()


class UserRelation(models.Model):
    from_user = models.ForeignKey(MyUser, related_name='following')
    to_user = models.ForeignKey(MyUser, related_name='follower')
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Relation from {} to {}'.format(
            self.from_user,
            self.to_user,
        )

    class Meta:
        unique_together = (
            ('from_user', 'to_user'),
        )


class Membership(models.Model):
    user = models.ForeignKey(
        MyUser,
        on_delete=models.CASCADE
    )
    group = models.ForeignKey(
        MyGroup,
        on_delete=models.CASCADE
    )
    joined_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (
            ('user', 'group')
        )


@receiver(post_save, sender=Membership, dispatch_uid='membership_save_update_num_of_members')
@receiver(post_delete, sender=Membership, dispatch_uid='membership_delete_update_num_of_members')
def update_num_of_members(sender, instance, **kwargs):
    if 'membership_save_update_num_of_members' in [kwargs['signal'].receivers[i][0][0] for i in
                                                   range(len(kwargs['signal'].receivers))]:
        instance.group.num_of_members += 1
    else:
        instance.group.num_of_members -= 1
    instance.group.save()
    task_update_num_of_member.delay(group_pk=instance.group.pk)
