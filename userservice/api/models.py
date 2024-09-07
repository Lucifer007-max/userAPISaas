from django.db import models

class Users(models.Model):
    id =  models.AutoField(primary_key=True, unique=True)
    fullname =  models.CharField(max_length=50,null=False )
    email =  models.CharField(max_length=50,null=False )
    password =  models.CharField(max_length=50,null=False )
    dob =  models.BigIntegerField(null=False)
    gender =  models.CharField(max_length=50,null=False)
    number =  models.BigIntegerField(null=True)
    socialLogin = models.IntegerField(null=False)
    userID = models.CharField(max_length=250,null=False)
    profileImage = models.CharField(max_length=500, null=True)
    Isdeleted = models.IntegerField(null=False, default=0)
    reason = models.CharField(max_length=1000 , null=True)
    
class Login(models.Model):
    id =  models.AutoField(primary_key=True, unique=True)
    email =  models.CharField(max_length=500,null=False,unique=True )
    token =  models.CharField(max_length=500,null=True )
 
 
class Cart (models.Model):
    id =  models.AutoField(primary_key=True, unique=True)
    user_id = models.CharField(max_length=250,null=True)
    cartID = models.CharField(max_length=250,null=True)
    