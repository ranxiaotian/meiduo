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
"""