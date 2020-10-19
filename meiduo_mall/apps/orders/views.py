from django.shortcuts import render

# Create your views here.
"""
需求：
    提交订单页面的展示
前端：
        发送一个axios请求来获取 地址信息和购物车中选中商品的信息
后端：
    请求：         必须是登录用户才可以访问
    业务逻辑：      地址信息，购物车中选中商品的信息
    响应：         JSON
    路由：
            GET     orders/settlement/
    步骤：
        
        1.获取用户信息
        2.地址信息
            2.1 查询用户的地址信息 [Address,Address,...]
            2.2 将对象数据转换为字典数据
        3.购物车中选中商品的信息
            3.1 连接redis
            3.2 hash        {sku_id:count,sku_id:count}
            3.3 set         [1,2]
            3.4 重新组织一个 选中的信息
            3.5 根据商品的id 查询商品的具体信息 [SKU,SKU,SKu...]
            3.6 需要将对象数据转换为字典数据
"""
from django.views import View
from utils.views import LoginRequiredJSONMixin
from apps.users.models import Address
from django_redis import get_redis_connection
from apps.goods.models import SKU
from django.http import JsonResponse

class OrderSettlementView(LoginRequiredJSONMixin,View):

    def get(self,request):
        # 1.获取用户信息
        user=request.user
        # 2.地址信息
        #     2.1 查询用户的地址信息 [Address,Address,...]
        addresses=Address.objects.filter(is_deleted=False)
        #     2.2 将对象数据转换为字典数据
        addresses_list=[]
        for address in addresses:
            addresses_list.append({
                'id': address.id,
                'province': address.province.name,
                'city': address.city.name,
                'district': address.district.name,
                'place': address.place,
                'receiver': address.receiver,
                'mobile': address.mobile
            })
        # 3.购物车中选中商品的信息
        #     3.1 连接redis
        redis_cli=get_redis_connection('carts')
        pipeline=redis_cli.pipeline()
        #     3.2 hash        {sku_id:count,sku_id:count}
        # 特别强调：：：  不要在这里接收redis的响应 all=pipeline.hgetall() 错误的 应该execute（）里接收
        pipeline.hgetall('carts_%s'%user.id)
        #     3.3 set         [1,2]
        pipeline.smembers('selected_%s'%user.id)
        # 我们接收 管道统一执行之后，返回的结果
        result=pipeline.execute()
        # result = [hash结果，set结果]
        sku_id_counts=result[0]         #{sku_id:count,sku_id:count}
        selected_ids=result[1]          # [1,2]
        #     3.4 重新组织一个 选中的信息
        #  selected_carts = {sku_id:count}
        selected_carts={}
        for sku_id in selected_ids:
            selected_carts[int(sku_id)]=int(sku_id_counts[sku_id])

        # {sku_id:count,sku_id:count}
        #     3.5 根据商品的id 查询商品的具体信息 [SKU,SKU,SKu...]
        sku_list=[]
        for sku_id,count in selected_carts.items():
            sku=SKU.objects.get(pk=sku_id)
            #     3.6 需要将对象数据转换为字典数据
            sku_list.append({
                'id':sku.id,
                'name':sku.name,
                'count':count,
                'default_image_url': sku.default_image.url,
                'price': sku.price
            })

        # 运费
        from decimal import Decimal
        freight=Decimal('10')
        # float double
        # decimal   -- 货币类型

        # 01010101
        # 整数
        # 小数的保存 特殊
        # 12.5
        # 12  0.5
        # 1100  1

        # 12.33
        # 0.33

        # 100 / 3 = 33.33

        # 33.33   33.33     33.34


        context = {
            'skus':sku_list,
            'addresses':addresses_list,
            'freight':freight        # 运费
        }

        return JsonResponse({'code':0,'errmsg':'ok','context':context})

"""
需求：
        点击提交订单，生成订单
前端：
        会发送axiso请求。 POST   携带数据  地址id,支付方式  携带用户的session信息（cookie）
        
        没有必须要携带  总金额， 商品id和数量 （后端自己都可以获取到）
        
后端：
    请求：         接收请求，验证数据
    业务逻辑：      数据入库
    响应：         返回响应
    
    路由：     POST
    步骤：
        
        1. 接收请求     user,address_id,pay_method
        2. 验证数据
        order_id 主键（自己生成）
        支付状态由支付方式决定
        总数量，总金额，运费
        连接redis
        hash
        set
        根据商品id，查询商品信息 sku.price
        
        3. 数据入库     生成订单（订单基本信息表和订单商品信息表）
            3.1先保存订单基本信息
                
            3.2再保存订单商品信息
              连接redis
              获取hash
              获取set     v
              最好重写组织一个数据，这个数据是选中的商品信息 
              根据选中商品的id进行查询
              判断库存是否充足，
              如果充足，则库存减少，销量增加
              如果不充足，下单失败
              保存订单商品信息
        4. 返回响应
        
        
        一。接收请求     user,address_id,pay_method
        二。验证数据
        order_id 主键（自己生成）
        支付状态由支付方式决定
        总数量，总金额， = 0
        运费
        三。数据入库     生成订单（订单基本信息表和订单商品信息表）
            1.先保存订单基本信息
                
            2 再保存订单商品信息
              2.1 连接redis
              2.2 获取hash
              2.3 获取set   
              2.4 遍历选中商品的id，
                最好重写组织一个数据，这个数据是选中的商品信息
                {sku_id:count,sku_id:count}
            
              2.5 遍历 根据选中商品的id进行查询
              2.6 判断库存是否充足，
              2.7 如果不充足，下单失败
              2.8 如果充足，则库存减少，销量增加
              2.9 累加总数量和总金额
              2.10 保存订单商品信息
          3.更新订单的总金额和总数量
          4.将redis中选中的商品信息移除出去
        四。返回响应
"""
import json
from apps.orders.models import OrderInfo,OrderGoods
class OrderCommitView(LoginRequiredJSONMixin,View):

    def post(self,request):
        user=request.user
        # 一。接收请求     user,address_id,pay_method
        data=json.loads(request.body.decode())
        address_id=data.get('address_id')
        pay_method=data.get('pay_method')

        # 二。验证数据
        if not all([address_id,pay_method]):
            return JsonResponse({'code':400,'errmsg':'参数不全'})

        try:
            address=Address.objects.get(id=address_id)
        except Address.DoesNotExist:
            return JsonResponse({'code':400,'errmsg':'参数不正确'})

        # if pay_method not in [1,2]:   这么写是没有问题的。
        # 从代码的可读性来说很差。 我都不知道 1 什么意思 2 什么意思

        if pay_method not in [OrderInfo.PAY_METHODS_ENUM['CASH'],OrderInfo.PAY_METHODS_ENUM['ALIPAY']]:
            return JsonResponse({'code': 400, 'errmsg': '参数不正确'})
        # order_id 主键（自己生成）   年月日时分秒 + 用户id（9位数字）
        from django.utils import timezone
        from datetime import datetime
        # datetime.strftime()
        # Year
        # month
        # day
        # Hour
        # Minute
        # Second
        # %f 毫秒
        # timezone.localtime() 2020-10-19 10:03:10
        order_id=timezone.localtime().strftime('%Y%m%d%H%M%S') + '%09d'%user.id

        # 支付状态由支付方式决定
        # 代码是对的。可读性差
        # if pay_method == 1: # 货到付款
        #     pay_status=2
        # else:
        #     pay_status=1

        if pay_method == OrderInfo.PAY_METHODS_ENUM['CASH']:
            status=OrderInfo.ORDER_STATUS_ENUM['UNSEND']
        else:
            status=OrderInfo.ORDER_STATUS_ENUM['UNPAID']

        # 总数量，总金额， = 0
        total_count=0
        from decimal import Decimal
        total_amount=Decimal('0')        #总金额
        # 运费
        freight=Decimal('10.00')

        # 三。数据入库     生成订单（订单基本信息表和订单商品信息表）
        #     1.先保存订单基本信息
        orderinfo=OrderInfo.objects.create(
            order_id=order_id,
            user=user,
            address=address,
            total_count=total_count,
            total_amount=total_amount,
            freight=freight,
            pay_method=pay_method,
            status=status
        )
        #     2 再保存订单商品信息
        #       2.1 连接redis
        redis_cli=get_redis_connection('carts')
        #       2.2 获取hash
        sku_id_counts=redis_cli.hgetall('carts_%s'%user.id)
        #       2.3 获取set
        selected_ids=redis_cli.smembers('selected_%s'%user.id)
        #       2.4 遍历选中商品的id，
        carts={}
        #         最好重写组织一个数据，这个数据是选中的商品信息
        #         {sku_id:count,sku_id:count}
        for sku_id in selected_ids:
            carts[int(sku_id)]=int(sku_id_counts[sku_id])

        ##         {sku_id:count,sku_id:count}
        #       2.5 遍历
        for sku_id,count in carts.items():
            # 根据选中商品的id进行查询
            sku=SKU.objects.get(id=sku_id)
            #       2.6 判断库存是否充足
            if sku.stock<count:
                #       2.7 如果不充足，下单失败
                return JsonResponse({'code':400,'errmsg':'库存不足'})

            #       2.8 如果充足，则库存减少，销量增加
            sku.stock -= count
            sku.sales += count
            sku.save()  #记得保存

            #       2.9 累加总数量和总金额
            orderinfo.total_count+=count
            orderinfo.total_amount+=(count*sku.price)

            #       2.10 保存订单商品信息
            OrderGoods.objects.create(
                order=orderinfo,
                sku=sku,
                count=count,
                price=sku.price
            )
        #   3.更新订单的总金额和总数量
        orderinfo.save()
        #   4.将redis中选中的商品信息移除出去 （暂缓）
        # 四。返回响应
        return JsonResponse({'code':0,'errmsg':'ok','order_id':order_id})

