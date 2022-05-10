from django.shortcuts import render

# Create your views here.
"""
需求分析： 根据页面的功能（从上到下，从左到右），哪些功能需要和后端配合完成
如何确定 哪些功能需要和后端进行交互呢？？？
        1.经验
        2.关注类似网址的相似功能

"""

"""
判断用户名是否重复的功能。

前端(了解)：     当用户输入用户名之后，失去焦点， 发送一个axios(ajax)请求

后端（思路）：
    请求:         接收用户名 
    业务逻辑：     
                    根据用户名查询数据库，如果查询结果数量等于0，说明没有注册
                    如果查询结果数量等于1，说明有注册
    响应          JSON 
                {code:0,count:0/1,errmsg:ok}

    路由      GET         usernames/<username>/count/        
   步骤：
        1.  接收用户名
        2.  根据用户名查询数据库
        3.  返回响应         

"""
from django.views import View
from apps.users.models import User
from django.http import JsonResponse
import re


class UsernameCountView(View):

    def get(self, request, username):
        # 1.  接收用户名，对这个用户名进行一下判断
        # if not re.match('[a-zA-Z0-9_-]{5,20}',username):
        #     return JsonResponse({'code':200,'errmsg':'用户名不满足需求'})
        # 2.  根据用户名查询数据库
        count = User.objects.filter(username=username).count()
        # 3.  返回响应
        return JsonResponse({'code': 0, 'count': count, 'errmsg': 'ok'})


"""
我们不相信前端提交的任何数据！！！！

前端：     当用户输入 用户名，密码，确认密码，手机号，是否同意协议之后，会点击注册按钮
            前端会发送axios请求

后端：
    请求：             接收请求（JSON）。获取数据
    业务逻辑：          验证数据。数据入库
    响应：             JSON {'code':0,'errmsg':'ok'}
                     响应码 0 表示成功 400表示失败

    路由：     POST    register/

    步骤：

        1. 接收请求（POST------JSON）
        2. 获取数据
        3. 验证数据
            3.1 用户名，密码，确认密码，手机号，是否同意协议 都要有
            3.2 用户名满足规则，用户名不能重复
            3.3 密码满足规则
            3.4 确认密码和密码要一致
            3.5 手机号满足规则，手机号也不能重复
            3.6 需要同意协议
        4. 数据入库
        5. 返回响应


"""
import json


class RegisterView(View):

    def post(self, request):
        # 1. 接收请求（POST------JSON）
        body_bytes = request.body
        body_str = body_bytes.decode()
        body_dict = json.loads(body_str)

        # 2. 获取数据
        username = body_dict.get('username')
        password = body_dict.get('password')
        password2 = body_dict.get('password2')
        mobile = body_dict.get('mobile')
        allow = body_dict.get('allow')

        # 3. 验证数据
        #     3.1 用户名，密码，确认密码，手机号，是否同意协议 都要有
        # all([xxx,xxx,xxx])
        # all里的元素 只要是 None,False
        # all 就返回False，否则返回True
        if not all([username, password, password2, mobile, allow]):
            return JsonResponse({'code': 400, 'errmsg': '参数不全'})
        #     3.2 用户名满足规则，用户名不能重复
        if not re.match('[a-zA-Z_-]{5,20}', username):
            return JsonResponse({'code': 400, 'errmsg': '用户名不满足规则'})
        #     3.3 密码满足规则
        #     3.4 确认密码和密码要一致
        #     3.5 手机号满足规则，手机号也不能重复
        #     3.6 需要同意协议
        # 4. 数据入库
        # user=User(username=username,password=password,moble=mobile)
        # user.save()

        # User.objects.create(username=username,password=password,mobile=mobile)

        # 以上2中方式，都是可以数据入库的
        # 但是 有一个问题 密码没有加密

        # 密码就加密
        user = User.objects.create_user(username=username, password=password, mobile=mobile)

        # 如何设置session信息
        # request.session['user_id']=user.id

        # 系统（Django）为我们提供了 状态保持的方法
        from django.contrib.auth import login
        # request, user,
        # 状态保持 -- 登录用户的状态保持
        # user 已经登录的用户信息
        login(request, user)

        # 5. 返回响应
        return JsonResponse({'code': 0, 'errmsg': 'ok'})


# 用户中心，也必须是登录用户
class LoginView(View):

    def post(self,request):
        # 1. 接收数据
        data=json.loads(request.body.decode())
        username=data.get('username')
        password=data.get('password')
        remembered=data.get('remembered')
        # 2. 验证数据
        if not all([username,password]):
            return JsonResponse({'code':400,'errmsg':'参数不全'})


        # 确定 我们是根据手机号查询 还是 根据用户名查询

        # USERNAME_FIELD 我们可以根据 修改 User. USERNAME_FIELD 字段
        # 来影响authenticate 的查询
        # authenticate 就是根据 USERNAME_FIELD 来查询
        if re.match('1[3-9]\d{9}',username):
            User.USERNAME_FIELD='mobile'
        else:
            User.USERNAME_FIELD='username'

        # 3. 验证用户名和密码是否正确
        # 我们可以通过模型根据用户名来查询
        # User.objects.get(username=username)


        # 方式2
        from django.contrib.auth import authenticate
        # authenticate 传递用户名和密码
        # 如果用户名和密码正确，则返回 User信息
        # 如果用户名和密码不正确，则返回 None
        user=authenticate(username=username,password=password)

        if user is None:
            return JsonResponse({'code':400,'errmsg':'账号或密码错误'})

        # 4. session
        from django.contrib.auth import login
        login(request,user)

        # 5. 判断是否记住登录
        if remembered:
            # 记住登录 -- 2周 或者 1个月 具体多长时间 产品说了算
            request.session.set_expiry(None)

        else:
            #不记住登录  浏览器关闭 session过期
            request.session.set_expiry(0)

        # 6. 返回响应
        response = JsonResponse({'code':0,'errmsg':'ok'})
        # 为了首页显示用户信息
        response.set_cookie('username',username)

        # 必须是登录后 合并
        #from apps.carts.utils import merge_cookie_to_redis
        #response = merge_cookie_to_redis(request, response)

        return response

"""
前端：
    当用户点击退出按钮的时候，前端发送一个axios delete请求

后端：
    请求
    业务逻辑        退出
    响应      返回JSON数据

"""
from django.contrib.auth import logout
class LogoutView(View):

    def get(self,request):
        # 1. 删除session信息
        logout(request)

        response = JsonResponse({'code':0,'errmsg':'ok'})
        # 2. 删除cookie信息，为什么要是删除呢？ 因为前端是根据cookie信息来判断用户是否登录的
        response.delete_cookie('username')

        return response

"""

LoginRequiredMixin 未登录的用户 会返回 重定向。重定向并不是JSON数据

我们需要是  返回JSON数据
"""

from utils.views import LoginRequiredJSONMixin


class CenterView(LoginRequiredJSONMixin, View):

    def get(self, request):
        # request.user 就是 已经登录的用户信息
        # request.user 是来源于 中间件
        # 系统会进行判断 如果我们确实是登录用户，则可以获取到 登录用户对应的 模型实例数据
        # 如果我们确实不是登录用户，则request.user = AnonymousUser()  匿名用户
        info_data = {
            'username': request.user.username,
            'mobile': request.user.mobile,
        }

        return JsonResponse({'code': 0, 'errmsg': 'ok', 'info_data': info_data})


"""
请求
业务逻辑（数据库的增删改查）
响应


增 （注册）
    1.接收数据
    2.验证数据
    3.数据入库
    4.返回响应

删 
    1.查询到指定记录
    2.删除数据（物理删除，逻辑删除）
    3.返回响应

改  （个人的邮箱）
    1.查询指定的记录
    2.接收数据
    3.验证数据
    4.数据更新
    5.返回响应

查   （个人中心的数据展示，省市区）
    1.查询指定数据
    2.将对象数据转换为字典数据
    3.返回响应
"""

"""
需求：
    新增地址

前端：
        当用户填写完成地址信息后，前端应该发送一个axios请求，会携带 相关信息 （POST--body）

后端：

    请求：         接收请求，获取参数,验证参数
    业务逻辑：      数据入库
    响应：         返回响应

    路由：     POST        /addresses/create/
    步骤： 
        1.接收请求
        2.获取参数，验证参数
        3.数据入库
        4.返回响应

"""

"""
from apps.users.models import Address


class AddressCreateView(LoginRequiredJSONMixin, View):

    def post(self, request):
        # 1.接收请求
        data = json.loads(request.body.decode())
        # 2.获取参数，验证参数
        receiver = data.get('receiver')
        province_id = data.get('province_id')
        city_id = data.get('city_id')
        district_id = data.get('district_id')
        place = data.get('place')
        mobile = data.get('mobile')
        tel = data.get('tel')
        email = data.get('email')

        user = request.user
        # 验证参数 （省略）
        # 2.1 验证必传参数
        # 2.2 省市区的id 是否正确
        # 2.3 详细地址的长度
        # 2.4 手机号
        # 2.5 固定电话
        # 2.6 邮箱

        # 3.数据入库
        address = Address.objects.create(
            user=user,
            title=receiver,
            receiver=receiver,
            province_id=province_id,
            city_id=city_id,
            district_id=district_id,
            place=place,
            mobile=mobile,
            tel=tel,
            email=email
        )

        address_dict = {
            'id': address.id,
            "title": address.title,
            "receiver": address.receiver,
            "province": address.province.name,
            "city": address.city.name,
            "district": address.district.name,
            "place": address.place,
            "mobile": address.mobile,
            "tel": address.tel,
            "email": address.email
        }

        # 4.返回响应
        return JsonResponse({'code': 0, 'errmsg': 'ok', 'address': address_dict})


class AddressView(LoginRequiredJSONMixin, View):

    def get(self, request):
        # 1.查询指定数据
        user = request.user
        # addresses=user.addresses

        addresses = Address.objects.filter(user=user, is_deleted=False)
        # 2.将对象数据转换为字典数据
        address_list = []
        for address in addresses:
            address_list.append({
                "id": address.id,
                "title": address.title,
                "receiver": address.receiver,
                "province": address.province.name,
                "city": address.city.name,
                "district": address.district.name,
                "place": address.place,
                "mobile": address.mobile,
                "tel": address.tel,
                "email": address.email
            })
        # 3.返回响应
        return JsonResponse({'code': 0, 'errmsg': 'ok', 'addresses': address_list})

"""
#################################################