from django.db import models

# Create your models here.
class User(models.Model):
    gender = (('male', '男'), ('female', '女'))
    phone = models.CharField(max_length=11,unique=True,null=False)
    name = models.CharField(max_length=64,null=False)
    password = models.CharField(max_length=128,null=False)
    email = models.EmailField(unique=True)
    sex = models.CharField(max_length=32,choices=gender,default='男')
    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['c_time']
        verbose_name = '用户'
        verbose_name_plural = '用户'

class UnreadMessage(models.Model):
    phone = models.CharField(max_length=11,null=False)
    sender = models.ForeignKey(User,on_delete=models.CASCADE)
    message = models.CharField(max_length=512,null=False)
    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.phone

    class Meta:
        ordering = ['c_time']
        verbose_name = '未读消息'
        verbose_name_plural = '未读消息'

class HistoricalMessage(models.Model):
    sender = models.ForeignKey(User,on_delete=models.CASCADE)
    message = models.CharField(max_length=512,null=False)
    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message

    class Meta:
        ordering = ['c_time']
        verbose_name = '历史消息'
        verbose_name_plural = '历史消息'