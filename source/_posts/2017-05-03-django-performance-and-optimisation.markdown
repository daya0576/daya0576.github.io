---
layout: post
title: "Django 性能优化官方文档笔记(主要针对ORM)"
date: 2017-05-04 1:34:09
comments: true
tags: [django, orm]
---

最近看了django关于性能优化的文档:     [https://docs.djangoproject.com/en/1.11/topics/performance/](https://docs.djangoproject.com/en/1.11/topics/performance/)   
[https://docs.djangoproject.com/en/1.8/topics/db/optimization/](https://docs.djangoproject.com/en/1.8/topics/db/optimization/)   
整理了一下笔记, 并写下几点比较深的感触**和我优化django代码的总结**.  

<!--more-->




### 1. 你的时间才是最宝贵的:
文档里的这句话还是挺有意思的(自己的时间和性能优化的trade-off): Your own time is a valuable resource, more precious than CPU time. Some improvements might be too difficult to be worth implementing, or might affect the portability or maintainability of the code. Not all performance improvements are worth the effort.



### 2. 最重要的原则: Work at the appropriate level
意思就是说要在对应的level(M V C)做对应的事. e.g. 如果计算court, 在最低的数据库level里是最快的 (如果只需要知道此记录是否存在的话, 用`exists()`会更快).   
但要`注意`: queryset是lazy的, 所以有时候在higher level(例如模板)里控制queryset是否真的执行, 说不定会更高效.   
_   
下面这段代码很好的解释了不同level的意思:    
```python
# QuerySet operation on the database
# fast, because that's what databases are good at
my_bicycles.count()

# counting Python objects
# slower, because it requires a database query anyway, and processing
# of the Python objects
len(my_bicycles)

# Django template filter
# slower still, because it will have to count them in Python anyway,
# and because of template language overheads
\{\{ my_bicycles|length \}\}
```




### 3. 用database中传统的优化手段

1. 加索引. 对你经常要用的字段进行加索引, 会大大的提升查找数据(filter(), exclude(), order_by(), etc.)的速度, 毕竟O(1)或O(logn)对于O(n)相差还是很大的.    
2. 使用合适的字段类型. 例如你的数据多到几亿条了, 合适的字段也会帮你节省很多的空间.




### 4. 理解Django中的QuerySets
**对于queryset lazy特性的说明:**   
这段代码看上去对数据库进行了三次查找, 但其实只在最后一行的时候执行了数据库的操作.   
```python
>>> q = Entry.objects.filter(headline__startswith="What")
>>> q = q.filter(pub_date__lte=datetime.date.today())
>>> q = q.exclude(body_text__icontains="food")
>>> print(q)

# ps.上边的这种多条件查询, 官方推荐这种写法:
Entry.objects.filter(
    headline__startswith='What'
).exclude(
    pub_date__gte=datetime.date.today()
).filter(
    pub_date__gte=datetime(2005, 1, 30)
)
```

**那么问题来了**, 既然queryset是lazy的, queryset[什么时候会被evaluate呢](https://docs.djangoproject.com/en/1.8/ref/models/querysets/#when-querysets-are-evaluated)?

1. Iteration, ie. 对Queryset进行For循环的操作.
2. [slicing](https://docs.djangoproject.com/en/1.8/topics/db/queries/#limiting-querysets), e.g. `Entry.objects.all()[:5]`, 获取queryset中的前五个对象, 相当于sql中的`LIMIT 5`
3. picling/caching
4. repr/str
5. len (Note: 如果你只想知道这个queryset结果的长度的话, 最高效的还是在数据库的层级调用count()方法, 也就是sql中的COUNT(). )
6. list()
7. bool()   

以上的情况一旦发生, 就会查询数据库并生成cache(**生成的cache就存在这个queryset对象之内的**),    
之后再对queryset做以上的操作就就不用再重新hit数据库进行查询了.)   

**举个栗子: **  
```python
>>> queryset = Entry.objects.all()
>>> print([p.headline for p in queryset]) # Evaluate the query set.
>>> print([p.pub_date for p in queryset]) # Re-use the cache from the evaluation.
```

**注意! 不会cache的情况:**   
Specifically, this means that limiting the queryset using an array slice or an index will not populate the cache.   
意思就是说queryset[5]和queryset[:5]是不会生成cache的. 还有exists()和iterator()这样的也不会生成cache.    
**举个栗子:**   
```python
>>> queryset = Entry.objects.all()
>>> print queryset[5] # Queries the database
>>> print queryset[5] # Queries the database again

>>> queryset = Entry.objects.all()
>>> [entry for entry in queryset] # Queries the database
>>> print queryset[5] # Uses cache
>>> print queryset[5] # Uses cache
```

最近发现`values`和`values_list`这两个方法也会重新查询数据库, 不知道是为什么.    
TODO: 有空看一下 具体的实现原理.   
_   
**研究的结果:**   
当调用values或values_list的时候, 会生成一个新的queryset with no cache.    
也就是说, 除了上边说到的七种会产生cache的情况, 其他都会重新去数据库拿数据.    
<img style="max-height:350px" class="lazy" data-original="/images/blog/170503_django_performace/disqus.png">    



### 5. 数据库层级的优化的总结
官方的文档介绍了很多, 我写几点最有效的和最常用的:   

- 利用[queryset lazy的特性](https://docs.djangoproject.com/en/1.8/topics/performance/#understanding-laziness)去优化代码, 尽可能的减少连接数据库的次数.
- 如果查出的queryset只用一次, 可以使用iterator()去来防止占用太多的内存, e.g.`for star in star_set.iterator(): print(star.name)`.    
感兴趣可以看看ModelIterable中重写的`__iter__`方法.   
- 尽可能把一些数据库层级的工作放到数据库, 例如使用filter/exclude, F, annotate, aggregate, etc.   
aggregate: https://docs.djangoproject.com/en/1.11/topics/db/aggregation/#cheat-sheet   
F(): getting the database, rather than Python, to do work
- 一次性拿出所有你要的数据, 不去取那些你不需要的数据.   
意思就是要巧用select_related(), prefetch_related() 和 values_list(), values().   
如果不用select_related的话, 去取外键的属性就会连数据再去查找.   
如果只需要id字段的话, 用values_list('id', flat=True)也能节约很多资源.   
<div style='margin-left: 20px'>
```python
class ModelA(models.Model):
    pass

class ModelB(models.Model):
    a = ForeignKey(ModelA)

ModelB.objects.select_related('a').all() # Forward ForeignKey relationship
ModelA.objects.prefetch_related('modelb_set').all() # Reverse ForeignKey relationship
```</div>
- bulk(批量)地去insert update和delete数据.     
- 查找一条数据时, 尽量用有索引的字段去查询, O(1)或O(log n) 和 O(n)差别还是很大的.   
- 用`count()`代替`len(queryset)`, 用`exists()`代替`if queryset:`   





### 6. 解决性能问题的具体方法:
- connection.queries:   
可以利用这两两句代码来分析你的代码的sql执行情况和花费时间:
<div style='margin-left: 20px'>
```python
from django.db import connection
connection.queries
>> [{'sql': 'SELECT polls_polls.id, polls_polls.question, polls_polls.pub_date FROM polls_polls',
     'time': '0.002'}]

from django.db import reset_queries
reset_queries()
```
</div>

- **django-debug-toolbar**:   
一个在github上有四千多个星星的开源项目: [https://github.com/dcramer/django-devserver](https://github.com/dcramer/django-devserver)   
很棒的一个可视化的工具, 但缺点是只能处理`text/html`类型的response, 因为是通过中间件修改返回的html代码实现的.       
**解决办法:** 可以再使用这个库: [django-debug-panel](https://github.com/recamshak/django-debug-panel),    
再配合链接中最后的chrome插件使用, 就可以查看所有异步请求的详细信息!   
如图:   
<img style="max-height:350px" class="lazy" data-original="/images/blog/170503_django_performace/IMG_3017.PNG">    
**优点:**   

    1. 统计了总的SQL查询时间.
    2. **重复查询的sql的数量, 在每条sql详细信息中显示重复的次数**.
    3. **执行sql的具体代码位置!!!**
    4. sql 语句的高亮
    5. sql 查询到的数据结果.  

<div style='margin-left: 20px'>
配置参考:   
``` python
#debug_toolbar settings
if DEBUG:
    INTERNAL_IPS = ('127.0.0.1',)
    MIDDLEWARE_CLASSES = (
        # 'debug_toolbar.middleware.DebugToolbarMiddleware',
        'debug_panel.middleware.DebugPanelMiddleware',
    ) + MIDDLEWARE_CLASSES

    INSTALLED_APPS += (
        'debug_toolbar',
        'debug_panel',
    )

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
```
</div>

- django-devserver   
项目github主页: [https://github.com/drinksober/django-devserver](https://github.com/drinksober/django-devserver)   
这个项目好久没有维护了..已经跑不起来了. 可以试试同事的修复版:   
[https://github.com/drinksober/django-devserver](https://github.com/drinksober/django-devserver)

- **line profiler:**    
其实最好用的还是用line profiler去找程序的瓶颈:    
效果如图所示, 显示了一个方法内哪行代码运行的时间最久:    
<img style="max-height:350px" class="lazy" data-original="/images/blog/170503_django_performace/profile_liner.png">    
使用方法(从同事黄俊那偷来的代码):   
<div style='margin-left: 20px'>
```python
class Line_Profiler(object):
    """put @profile on ur functions"""
    def __init__(self, follow=None):
        self.follow = follow or []

    def __call__(self, func):
        def profiled_func(*args, **kwargs):
            line_profiler = LineProfiler()
            line_profiler.add_function(func)
            map(lambda x: line_profiler.add_function(x), self.follow)
            line_profiler.enable_by_count()
            result = func(*args, **kwargs)

            line_profiler.disable_by_count()
            line_profiler.print_stats(stripzeros=True)
            return result

        return functools.wraps(func)(profiled_func)

__builtin__.profile = Line_Profiler()
```
</div>



### 7.举个栗子:   
最近重新写了一个项目里很常用的方法(之前也是我写的, 但感觉稍微有些慢), 利用上文说的一些知识, 把执行时间从100多ms降到了20ms.    
```python
def users(self, add_self=False, add_share=True, select_id=False, **kwargs):
    """Return 当前用户能看到的所有用户, 返回queryset, 以便做性能优化:

    参数:
        1. add_self:  是否添加当前用户(self).
        2. add_share: 是否添加因为共享(account/campaign)而可见的用户. e.g. u2共享a1给u1, u1.users(add_share=True)就能看到u2
        3. select_id: 是否只取id字段
    逻辑:
        1. add_share=False 时:
            +----------+-------------------------------------+
            | Type     | 可见的用户集合                        |
            +----------+-------------------------------------+
            | Root     | 所有 [Advanced, Member] - blacklist |
            +----------+-------------------------------------+
            | Admin    | 同组 [Advanced, Member] - blacklist |
            +----------+-------------------------------------+
            | other    | []                                  |
            +----------+-------------------------------------+
        2. add_share=True 时:
            利用当前用户能看到的所有accounts, 获取创建它们的用户(permission=2)
    """
    # 1. users_shared
    if add_share:
        # 共享给该用户的account的主人们
        aps = AccountPermission.objects.filter(
            account__status='ACTIVE', permission='2', account__in=self.accounts()
        ).select_related('share_user').values_list('share_user__id', flat=True)
        users_shared = User.objects.filter(id__in=aps)
    else:
        users_shared = User.objects.none()

    # 2. users
    if self.score <= 2:
        query_dict = dict(role__in=['ADVANCED', 'MEMBER'])
        # Admin
        self.score == 2 and query_dict.update(usergroup=self.usergroup)
        users = User.objects.filter(**query_dict).exclude(id__in=self.blacklist)
    else:
        users = User.objects.filter(id=self.id)

    users = users | users_shared

    # 控制是否添加本身, 主要是user1.has_permission(user1)的时候用到
    if not add_self:
        users = users.exclude(id=self.id)
    else:
        users |= User.objects.filter(id=self.id)

    # 过滤停用的用户:
    users = users.filter(is_active=True, usergroup__status='ACTIVE')
    users = users.filter(**kwargs)

    # 大部分情况下只需要id. 用户列表很多时, 可以大幅度提高性能.
    if select_id:
        users = users.values_list('id', flat=True)

    return set(users)
```


