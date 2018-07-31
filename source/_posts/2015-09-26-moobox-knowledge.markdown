---
layout: post
title: "记录moobox的点滴(技术篇)"
date: 2015-09-26 20:43:11 +0800
comments: true
categories: [mysql, django, moobox, work]
---


> 在moobox工作了两个月，用这篇日志记录这段日子的技术点滴。    
ps.虽然一直有这个计划，平时也会作笔记，但是到头来还是记得不太全，   
就粗略的写一下好了。    

<!--more-->

## Mysql   
公司用的数据库是mysql，可惜自己对数据库的知识忘得差不多了，下面记录一些后来回忆起的sql用法。  
有个软件叫做 MySQL Workbanch，还是挺方便的。         
1.增删改查就不说了，还是要熟练，总不能写一次去看一下语法吧。    
2.desc也是必备，以前上学的时候老是记不清，但工作中还是desc用的比较多，asc是默认的升序。   
3.left和inner join，关联多表的时候的必备，还是要保持清醒。    
4.group by后边可以加限制条件，叫做group by having (...), 学数据库的时候学过，小小鸟提起的时候才如梦初醒   
group by的时候可以根据两个条件进行group by， 例如：
```sql
//获取每个地推人员的每天数据
//计算录入
select date(from_unixtime(b.CreatedDate+60*60*8)), count(distinct a.UID),b.CreatedBy from ParkingRawData a
inner join Customer b on a.UID = b.ParkingUID where Source = 'tuhu' and b.CreatedBy != ''
group by date(from_unixtime(b.CreatedDate+60*60*8)), b.CreatedBy
```
4.insert的妙用：
```sql
INSERT INTO ParkingRawDataHistory(RawID,UID,Name)
select ID,UID,Name from ParkingRawData 
where UID =  'e4d1701c-4185-11e5-af26-3c15c2bca022';
```
5.sql 时间戳    
```sql
SELECT FROM_UNIXTIME( 1440015345, '%Y年%m月%d日' )
SELECT UNIX_TIMESTAMP()
SELECT UNIX_TIMESTAMP(Current_TimeStamp)
```
6.模糊查找   
```sql
SELECT * FROM ParkingRawData where name like "%虹景公寓酒店%"
```
总结：学好sql语句也是很重要的，一句好的sql语句能很好的简化代码的复杂度，     
并且提高接口的效率，只恨自己数据库忘得太快。   
 

## Python
1.每次在django中添加接口，我都要检查的问题：       
* - - -数据库中api和page的权限。   
* - setting中数据库变量的配置 和 接口url的配置是否正确。   
* WebInterfaceBase修改跨越问题（后台和前端没有放在一个项目里）。   
* 测试接口时json格式是否正确（可以去网上好多在线检测的网站）。   
2.python list去除重复元素   
```python
list(set(all_workers))
{}.fromkeys(workers).keys()
```
3.django端口占用的问题   
查看端口占用    
```
I:\Users\Daya>netstat -aon|findstr "8000"
  TCP    0.0.0.0:8000           0.0.0.0:0              LISTENING       5664
  TCP    127.0.0.1:8000         127.0.0.1:49640        ESTABLISHED     5664
  TCP    127.0.0.1:8000         127.0.0.1:49851        ESTABLISHED     5664
  TCP    127.0.0.1:8000         127.0.0.1:49852        ESTABLISHED     5664
  TCP    127.0.0.1:49640        127.0.0.1:8000         ESTABLISHED     3716
  TCP    127.0.0.1:49851        127.0.0.1:8000         ESTABLISHED     3716
  TCP    127.0.0.1:49852        127.0.0.1:8000         ESTABLISHED     3716
I:\Users\Daya>tasklist|findstr "5664"
pycharm.exe                   5664 Console                    1    372,204 K
I:\Users\Daya>tasklist|findstr "3716"
chrome.exe                    3716 Console                    1    196,444 K   
```
4.遇到过一个问题就是django的问题就是明明有这个文件夹，却报错说找不到。    
因为这个文件夹里没有init的空文件，django是通过URL和这个标示来找的。   
5.时间戳的一些操作   
```python
# 时间的转换，python的包都很完善了。
print int(time.mktime(time.strptime("20140903131540", '%Y%m%d%H%M%S')))
# 时间戳，统一0时区的时间戳。
vtimestamp = str(time.mktime(datetime.datetime.utcnow().timetuple()))
```
6.后来加的分页操作，注意limit后边两个参数的意义。   
```python
cursor.execute(sql_count)
data = cursor.fetchall()
if len(data) > 0:
    pagecount = data[0][0]/pagesize + 1
    self.pagecount = pagecount

start = (pagenumber-1) * pagesize
sql += " limit %s, %s " % (start, pagesize)
```
先说这这些吧，其实还有好多，不细说了。    
*说一点感悟吧，写代码就是生活中做事一样，一个好的计划是最重要的， 每一步做什么理清楚后，*     
*写起代码来就事半功倍了，所以不要埋头苦写，做点草稿，有好的规划才行。*    

## JS+HTML5
做后台的话，有时候写完接口，还要迫不得已要把前台的东西都包了、   
但说实话，之前对js真的是完全没有实战过，所以写起来还是很吃力。    
有力发不出的感觉，总是被一些小错误困扰很久，把一些简单的问题搞复杂。    
记录一些前端方面的新知识吧。    
1.自适应布局：[http://nec.netease.com/library/101023](http://nec.netease.com/library/101023)   
之前大一学过css布局，但现在都是html5了还要手机适配，原来的样式已经用不了了。    
上面这个网址还不错，有一些自适应的例子，但感觉还是好复杂，应该有更简单的解决方法吧。    
2.jquery的show()和hide()其实就是改变dispay:none
3.设置a标签的超链接    
```html
//以前的超链接
<a href="#"></a>
//现在的写法，防止出错。   
<a href="javascript:;"></a>
```        
4.确认按钮   弹出是否提交？   
```javascript
if (confirm("确认信息无误？")) {}
```
5.动画  旋转    
```css
transform:rotate(90deg)

transform:rotate(0deg);
transition: transform 0.3s;
```
6.滚动条的自动定位     
```javascript
$('.div-fixed-height').animate({scrollTop: $('#reportdetail').height()}, 300);
```
7.遍历所有td    
```javascript
$("#nearparkingscontent").find(":checkbox:checked").each(function(){
	var val = $(this).closest('tr').find('td').eq(7).text();
 	parking_uids += val + " ";
});
```
8.js str去除最后一位
```javascript
type.parkingtype = parkingtypestr.substring(0, parkingtypestr.length-1);
```
9.checkbox 的onchange事件    
```javascript
function alertMerge(check1){
if(check1.checked==true)
  if (confirm("确认合并此停车场？")) {
		//
	}else{
		check1.checked=false;
	 	//check1.attr("checked", "checked");
	}
}
```
10.jquery   移除样式。   
```javascript
$(".syzx > span:first").removeAttr("style"); 
``` 
*总结*：js不会的多，记的笔记也多点，但总的来说，个人觉得js是一个很灵活的语言，    
有时间还是要多掌握一些基础的特性，才能写出一些精炼高效的代码。    

## 参与的所有项目大合照   
<img class="lazy" href="javascript:;" data-original="/images/blog\150923_moobox/sourcetree.png" >    
从上往下简单介绍一下。    
1. 