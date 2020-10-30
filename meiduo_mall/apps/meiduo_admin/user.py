# 当系统的功能 不能满足我们需求的时候就要重写

def jwt_response_payload_handler(token, user=None, request=None):
    # token,        认证成功之后,生成的token
    # user=None,    认证成功之后的用户
    # request=None  请求
    return {
        'token': token,
        'username':user.username,
        'id':user.id
    }