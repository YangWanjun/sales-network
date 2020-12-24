from django.contrib.auth.models import User
from django.db import models

from utils import constants
from utils.model_base import BaseModel


# Create your models here.
class Tenant(BaseModel):
    code = models.CharField(max_length=10, primary_key=True, verbose_name='会社コード')
    name = models.CharField(max_length=50, verbose_name='会社名称')
    user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='ユーザー')

    class Meta:
        db_table = 't_tenant'
        ordering = ('name',)
        verbose_name = "テナント"
        verbose_name_plural = "テナント一覧"


class ProjectOrder(BaseModel):
    tenant_from = models.ForeignKey(
        Tenant, on_delete=models.PROTECT, related_name='project_order_from_set',
        verbose_name='案件注文書作成元テナント会社'
    )
    tenant_to = models.ForeignKey(
        Tenant, on_delete=models.PROTECT, related_name='project_order_to_set',
        verbose_name='案件注文書送付先テナント会社'
    )
    order_no = models.CharField(max_length=20, verbose_name="注文番号")
    publish_date = models.DateField(verbose_name="発行年月日", help_text='協力会社導入時は注文日とする')
    start_date = models.DateField(verbose_name="開始日")
    end_date = models.DateField(verbose_name="終了日")
    contract_type = models.CharField(
        max_length=2, choices=constants.CHOICE_CUSTOMER_CONTRACT_TYPE, verbose_name="契約形態"
    )
    bank_code = models.CharField(max_length=4, blank=True, null=True, verbose_name="金融機関コード")
    branch_no = models.CharField(max_length=3, blank=True, null=True, verbose_name="支店番号")
    account_type = models.CharField(
        max_length=2, choices=constants.CHOICE_BANK_ACCOUNT_TYPE, verbose_name="預金種類"
    )
    account_number = models.CharField(max_length=8, blank=True, null=True, verbose_name="口座番号")
    account_holder = models.CharField(max_length=30, blank=True, null=True, verbose_name="口座名義")
    filename_order = models.CharField(max_length=100, blank=True, null=True, verbose_name="注文書")
    filename_request = models.CharField(max_length=100, blank=True, null=True, verbose_name="注文請書")
    is_translated = models.BooleanField(default=False, verbose_name="注文書情報は協力会社に導入済")

    class Meta:
        db_table = 't_project_order'
        ordering = ('tenant_from', 'tenant_to')
        verbose_name = "案件注文書"
        verbose_name_plural = "案件注文書一覧"


class ProjectOrderMember(BaseModel):
    project_order = models.ForeignKey(ProjectOrder, on_delete=models.PROTECT)

