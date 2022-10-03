from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.commons.models import TimeStampedUUIDModel
from apps.inventory.dependencies.constants import PROCESSING_STATUS


class PastryType(TimeStampedUUIDModel):
    name: str = models.CharField(max_length=512)

    def __str__(self) -> str:
        return f"{self.pkid}  {self.name} on {self.created_at}"


class RawMaterialType(TimeStampedUUIDModel):
    name: str = models.CharField(max_length=512)

    def __str__(self) -> str:
        return f"{self.pkid}  {self.name} on {self.created_at}"


class PastryRawMaterialBatch(TimeStampedUUIDModel):
    batch_code = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = _("Pastry Raw Materials Batches")

    def __str__(self) -> str:
        return f"{self.pkid}  {self.batch_code} on {self.created_at}"


class TimeOfDay(TimeStampedUUIDModel):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = _("Time of Day")

    def __str__(self) -> str:
        return f"{self.pkid}  {self.name} on {self.created_at}"


class RawMaterial(models.Model):
    weight = models.FloatField()
    cost = models.FloatField()
    processing_status = models.CharField(choices=PROCESSING_STATUS, max_length=7)
    pastry_type = models.ForeignKey(PastryType, on_delete=models.RESTRICT)
    time_of_day = models.ForeignKey(TimeOfDay, on_delete=models.RESTRICT)
    raw_material_type = models.ForeignKey(RawMaterialType, on_delete=models.RESTRICT)
    batch = models.ForeignKey(PastryRawMaterialBatch, on_delete=models.RESTRICT)

    def __str__(self) -> str:
        return f"{self.pkid}  {self.batch} on {self.created_at}"
