from django.db import models


class DefaultManager(models.Manager):

    def __init__(self, *args, **kwargs):
        super(DefaultManager, self).__init__()
        self.args = args
        self.kwargs = kwargs

    def get_queryset(self):
        return super(DefaultManager, self).get_queryset().filter(*self.args, **self.kwargs)

    def public_all(self):
        return self.get_queryset().filter(is_deleted=False)


class BaseModel(models.Model):
    created_dt = models.DateTimeField(auto_now_add=True, verbose_name="作成日時")
    updated_dt = models.DateTimeField(auto_now=True, verbose_name="更新日時")
    is_deleted = models.BooleanField(default=False, editable=False, verbose_name="削除フラグ")
    deleted_dt = models.DateTimeField(blank=True, null=True, editable=False, verbose_name="削除日時")

    objects = DefaultManager()

    class Meta:
        abstract = True
