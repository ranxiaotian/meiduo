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

    def get(self,request,username):
        # 1.  接收用户名，对这个用户名进行一下判断
        # if not re.match('[a-zA-Z0-9_-]{5,20}',username):
        #     return JsonResponse({'code':200,'errmsg':'用户名不满足需求'})
        # 2.  根据用户名查询数据库
        count=User.objects.filter(username=username).count()
        # 3.  返回响应
        return JsonResponse({'code':0,'count':count,'errmsg':'ok'})

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

    def post(self,request):
        # 1. 接收请求（POST------JSON）
        body_bytes=request.body
        body_str=body_bytes.decode()
        body_dict=json.loads(body_str)

        # 2. 获取数据
        username=body_dict.get('username')
        password=body_dict.get('password')
        password2=body_dict.get('password2')
        mobile=body_dict.get('mobile')
        allow=body_dict.get('allow')

        # 3. 验证数据
        #     3.1 用户名，密码，确认密码，手机号，是否同意协议 都要有
        # all([xxx,xxx,xxx])
        # all里的元素 只要是 None,False
        # all 就返回False，否则返回True
        if not all([username,password,password2,mobile,allow]):
            return JsonResponse({'code':400,'errmsg':'参数不全'})
        #     3.2 用户名满足规则，用户名不能重复
        if not re.match('[a-zA-Z_-]{5,20}',username):
            return JsonResponse({'code': 400, 'errmsg': '用户名不满足规则'})
        #     3.3 密码满足规则
        #     3.4 确认密码和密码要一致
        #     3.5 手机号满足规则，手机号也不能重复
        #     3.6 需要同意协议
        # 4. 数据入库
        # user=User(username=username,password=password,moble=mobile)
        # user.save()

        # User.objects.create(username=username,password=password,mobile=mobile)

        #以上2中方式，都是可以数据入库的
        # 但是 有一个问题 密码没有加密

        # 密码就加密
        user=User.objects.create_user(username=username,password=password,mobile=mobile)

        # 如何设置session信息
        # request.session['user_id']=user.id

        # 系统（Django）为我们提供了 状态保持的方法
        from django.contrib.auth import login
        # request, user,
        # 状态保持 -- 登录用户的状态保持
        # user 已经登录的用户信息
        login(request,user)

        # 5. 返回响应
        return JsonResponse({'code':0,'errmsg':'ok'})

"""
如果需求是注册成功后即表示用户认证通过，那么此时可以在注册成功后实现状态保持 (注册成功即已经登录)  v
如果需求是注册成功后不表示用户认证通过，那么此时不用在注册成功后实现状态保持 (注册成功，单独登录)

实现状态保持主要有两种方式：
    在客户端存储信息使用Cookie
    在服务器端存储信息使用Session

"""