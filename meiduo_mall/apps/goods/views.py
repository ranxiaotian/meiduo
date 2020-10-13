from django.shortcuts import render

# Create your views here.
"""
关于模型的分析
1. 根据页面效果 尽量多的分析字段
2. 去分析是保存在一个表中 还是多个表中 （多举例说明）

分析表的关系的时候 最多不要超过3个表

多对多（一般是 3个表）

学生 和 老师

学生表
stu_id      stu_name

100             张三
200             李四

老师表
teacher_id  teacher_name
666             牛老师
999             齐老师


第三张表

stu_id      teacher_id
100             666
100             999
200             666
200             999

商品day01    模型的分析 --》  Fdfs(用于保存图片，视频等文件) --》 为了部署Fdfs学习Docker


"""

############上传图片的代码################################
# from fdfs_client.client import Fdfs_client
#
# # 1. 创建客户端
# # 修改加载配置文件的路径
# client=Fdfs_client('utils/fastdfs/client.conf')
#
# # 2. 上传图片
# # 图片的绝对路径
# client.upload_by_filename('/home/ubuntu/Desktop/img/c.png')

# 3. 获取file_id .upload_by_filename 上传成功会返回字典数据
# 字典数据中 有file_id
"""
{'Group name': 'group1', 'Remote file_id': 'group1/M00/00/02/wKgTgF-FCP-AHcq2AAMTeyk-Y3M402.png', 'Status': 'Upload successed.', 'Local file name': '/home/ubuntu/Desktop/img/c.png', 'Uploaded size': '196.00KB', 'Storage IP': '192.168.19.128'}

"""

from django.views import View
from utils.goods import get_categories
from apps.contents.models import ContentCategory

class IndexView(View):

    def get(self,request):

        """
        首页的数据分为2部分
        1部分是 商品分类数据
        2部分是 广告数据

        """
        # 1.商品分类数据
        categories=get_categories()
        # 2.广告数据
        contents = {}
        content_categories = ContentCategory.objects.all()
        for cat in content_categories:
            contents[cat.key] = cat.content_set.filter(status=True).order_by('sequence')

        # 我们的首页 后边会讲解页面静态化
        # 我们把数据 传递 给 模板
        context = {
            'categories': categories,
            'contents': contents,
        }
        # 模板使用比较少，以后大家到公司 自然就会了
        return render(request,'index.html',context)

