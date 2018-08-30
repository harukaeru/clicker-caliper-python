from django.db import models

class Answer(models.Model):
    userId = models.CharField('userId', max_length=255)

    clickerItem = models.ForeignKey('ClickerItem', related_name='answers', blank=True, on_delete=models.CASCADE)
    clickerOption = models.ForeignKey('ClickerOption', related_name='answers', blank=True, on_delete=models.CASCADE)


class ClickerItem(models.Model):
    STATUS_NEW = 0
    STATUS_ONGOING = 1
    STATUS_COMPLETED = 2

    STATUS_CHOICES = (
        (0, 'Status New'),
        (1, 'Status Ongoing'),
        (2, 'Status Completed'),
    )

    status = models.IntegerField('status', default=2, choices=STATUS_CHOICES)
    body = models.TextField('Body')
    resourceLinkId = models.TextField('ResourceLinkId')

    @property
    def isNew(self):
        return self.status == ClickerItem.STATUS_NEW

    @property
    def isActive(self):
        return self.status == ClickerItem.STATUS_ONGOING


# Create your models here.
class ClickerOption(models.Model):

    title = models.TextField('Title')
    clickerItem = models.ForeignKey(ClickerItem, related_name='clickerOptions', blank=True, on_delete=models.CASCADE)
