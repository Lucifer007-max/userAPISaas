import base64
import json
from django.shortcuts import get_object_or_404
from rest_framework import viewsets , status
from rest_framework.response import Response
from Crypto.Cipher import AES
from .models import Cart, Users , Login
from .serializers import  CartSerializer, LoginSerializer, UserSerializer

class Auth(viewsets.ViewSet):
    

    def userExist(self, request):
        # print(self.__ne__({"help" : "hjshdfhs"}))
        # """ Check if a user with the given email already exists. """
        # users = Users.objects.get(email=request.data['email'])
        # print(users)
        # userdeleted = Users.objects.get(email=request.data['email'])
        # if userdeleted.Isdeleted == 0:
        #     try:
        #         if Users.objects.filter(email=request.data['email']).exists():
        #             return Response({"message": "User Exist", "socialLogin": users.socialLogin, "status":status.HTTP_200_OK })
        #         return Response({"message": "User Not Exists", "socialLogin": users.socialLogin, "status":status.HTTP_404_NOT_FOUND})
        #     except Users.DoesNotExist:
        #         return Response({"message": "User Does Not Exist", "status":status.HTTP_404_NOT_FOUND})
        # else:
        #     return Response({"message": "Account is deleted" , "status":status.HTTP_400_BAD_REQUEST})
        email = request.data.get('email')
        try:
            user = Users.objects.exclude(Isdeleted="1").get(email=email)
        except Users.DoesNotExist:
            return Response({"message": "User Does Not Exist", "status": status.HTTP_404_NOT_FOUND})

        if user.Isdeleted == 0:
            return Response({"message": "User Exist", "socialLogin": user.socialLogin, "status": status.HTTP_200_OK})
        else:
            return Response({"message": "Account is deleted", "status": status.HTTP_400_BAD_REQUEST})

        
        
        
    def create(self, request):
        serializer = UserSerializer(data=request.data)
        # userdeleted = Users.objects.get(email=request.data['email'])
        # if userdeleted.Isdeleted == 0:
        # userdeleted.Isdeleted == 1
        # if userdeleted == request.data['email']:
        #     userdeleted.Isdeleted == 0  
        # if userdeleted == 0:
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # else:
            
        # else:
        #     if serializer.is_valid():
        #         serializer.save()
        #         return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        # else:
        #     return Response({"message": "Account is deleted" , "status":status.HTTP_400_BAD_REQUEST})
    
    def delete(self, request):
        try:
            response = Users.objects.filter(userID=request.data['id']).update(Isdeleted = 1,   reason = request.data['reason'])
            if response == 1:
                return Response({"message": "User Deleted successfully" , "status":status.HTTP_200_OK})
            else:
                return Response({"message": "User Already Deleted" , "status":status.HTTP_400_BAD_REQUEST})
        except Users.DoesNotExist:
            return Response({"message": "User Already Deleted"}, status=status.HTTP_404_NOT_FOUND)

    def validatePassword(self, request):
        password = request.data.get('password')
        user_id = request.data.get('userID')
        try:
            user = Users.objects.get(userID=user_id)
            if user.password == password:
                return Response({"message": "Password is correct", "status": status.HTTP_200_OK})
            else:
                return Response({"message": "Incorrect password", "status": status.HTTP_400_BAD_REQUEST})
        except Users.DoesNotExist:
            return Response({"message": "User not found", "status": status.HTTP_404_NOT_FOUND})
        
        

    # '''Authenticate'''
    def authenticate(self,request):
        email = request.data.get('email')
        # token = request.data.get('token')
        userdeleted = Users.objects.exclude(Isdeleted="1").get(email=email)
        print(userdeleted)
        if userdeleted.Isdeleted == 0:
            serializer = LoginSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Login successfully","status":status.HTTP_201_CREATED})
        else:
            return Response({"message": "Account is deleted" , "status":status.HTTP_400_BAD_REQUEST})
            
    # '''Logout'''
    def logout(self,request):
        email = request.data.get('email')
        response = Login.objects.filter(email=email).update(token='')
        if response == 1:
            return Response({"message": "Logout successfully"} , status=status.HTTP_200_OK)
        else:
            return Response({"message": "Email Doesn't match"}, status=status.HTTP_400_BAD_REQUEST)
       
    
    def getUserById(self, request, user_id):
        try:
            print(user_id)
            user = Users.objects.get(userID=user_id)
            print(user)
        except Users.DoesNotExist:
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(user)
        return Response(serializer.data)
      
    def updateUser(self, request, user_id):
        try:
            user = Users.objects.get(userID=user_id)
        except Users.DoesNotExist:
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return  Response({"message":"User Update successfully"},status=status.HTTP_200_OK)
            # return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)   
       
    def pad(self, s):
        block_size = AES.block_size
        padding = block_size - len(s) % block_size
        return s + chr(padding) * padding
    
    def unpad(self, s):
        return s[:-ord(s[-1])]

    def encrypt(self, txt):
        cipher = AES.new(b'\x12\x8cX\xe0zvV\xfd\x17\xf7\xe0\x17\xde5\x8f\x87\xc9\xbf\x1e8y\xa3\xb0\x96\xec7\x9a\xd2\xd6d0\xd0', AES.MODE_CBC)
        ct_bytes = cipher.encrypt(self.pad(txt).encode())
        iv = base64.b64encode(cipher.iv).decode('utf-8')
        ct = base64.b64encode(ct_bytes).decode('utf-8')
        return json.dumps({'iv': iv, 'ct': ct})

    def decrypt(self, txt_to_decrypt, key):
        try:
            b64 = json.loads(txt_to_decrypt)
            iv = base64.b64decode(b64['iv'])
            ct = base64.b64decode(b64['ct'])
            cipher = AES.new(key, AES.MODE_CBC, iv)
            return self.unpad(cipher.decrypt(ct)).decode('utf-8')
        except (ValueError, KeyError):
            return "Incorrect decryption"

    
    def getCartDataById(self, request, user_id):
        try:
            data = Cart.objects.get(user_id=user_id)
        except Cart.DoesNotExist:
            return Response( {
                "id": user_id,
                "user_id": None,
                "cartID": None
            }, status=status.HTTP_200_OK)

        serializer = CartSerializer(data)
        return Response(serializer.data)
 
    def updateCart(self, request, user_id):
        try:
            # Try to get the cart associated with the user_id
            cart = get_object_or_404(Cart, user_id=user_id)
            print(cart )
            # Update the cartId for the existing cart
            cart.cartID = request.data.get('cartID', cart.cartID)
            cart.save()
            print(cart.cartID)
            return Response({"message": "User cart updated successfully"}, status=status.HTTP_200_OK)
        except:
            # If cart does not exist, create a new cart with the provided data
            data = request.data.copy()
            data['user_id'] = user_id
            serializer = CartSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Cart added successfully"}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  

