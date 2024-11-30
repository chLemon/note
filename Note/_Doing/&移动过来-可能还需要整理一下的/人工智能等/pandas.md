drop可以删行、列

直接赋值columns可以改列名



# Pandas数据读取

需要读取表格类型的数据
数据类型|说明|读取方法
---|---|---
csv、tsv、txt|逗号分割，tab分割，任意分割|pd.read_csv
excel|微软|pd.read_excel
mysql|关系型数据库表|pd.read_sql

读取：
```
data=pd.read_csv(fpath,sep="分隔符",header=None,names=['列名']) #header表示文件无列名，names自定义列名
```
index_column：如果原本的数据有索引，要设置成0（索引列？）

查看前几行：
    data.head() #index行序号，columns列名，head里可以传参数，前n行
查看形状，返回行数列数
    data.shape
查看列名列表
    data.columns
查看索引列
    data.index
查看每列的数据类型
    data.dtypes

# Pandas数据结构
DataFrame和Series
## Series
类似于一维数组的对象，由数据和索引组成

### 创建方法
用列表产生
    s1=pd.Series([1,2,3])
    # 获取索引
​    s1.index
    # 获取数据
​    s1.values
可以指定索引：
​    s2=pd.Series([1,2,3],index=["a","b","c"])
用字典产生：key会成为索引，value成为数据
​    s3.pd.Series(dict)

### 查询数据
类似字典
    s2['a']#获取值
    type(s2['a'])#获取类型，如int
    s2[ ['b','a'] ]#获取多个值，传一个列表进去，此时返回的还是一个series

## DataFrame
行索引：index，列索引：columns
可以看作Series组成的字典
    data={
    'c1':[1,2,3]
    'c2':[4,5,6]
    }
    df=pd.DataFrame(data)

查询列类似字典
查询行：
    df.loc[i]
查询多行：**注意！！！！此处包含第3行**
    df.loc[1:3]

# Pandas数据查询
## 查询方法
1. df.loc，根据行、列的标签值查询
2. df.iloc，根据行、列的数字位置查询
3. df.where
4. df.query

df.loc方法即能查询，又能覆盖写入，很好用
## df.loc查询的方法
1. 使用单个label值查询
2. 使用值列表批量查询
3. 使用数值区间范围查询
4. 使用条件表达式查询
5. 调用函数查询

注意：以上方法既适用于行，也适用于列
## 实例
重置索引
    df.set_index('time',inplace=True, drop=True)
    # 将time设置成索引，并且直接改变原DataFrame，drop默认为True，会删掉原来的time列
替换数据
    df.loc[:,"bWendu"] = df["bWendu"].str.replace("℃","").astype('int32')

    # 筛选出bWendu列，并替换为，将bWendu列的值，字符串中的℃换位空，并改变类型为int32

### 单个label值查询：
    df.loc['index1','column1']
### 值列表批量
    df.loc[ [index1,index2],[column1,column2] ]
### 使用数值区间进行范围查询
**注意区间两侧都是闭区间**
    df.loc[ [index1:index5],c1 ] #这里index两侧不用加[ ]
### 条件表达式查询
bool列表的长度要等于行数或者列数 
    df.loc[ df[c1]<5,: ]
    #输出c1那一列数值小于5的全部行
**条件组合用&**
### 调用函数查询
    df.loc[ function ,: ]
    def function(df):
        return bool
注意，函数是直接传进去的，并没有调用，传进去后会把每个行传入函数调用

# Pandas新增数据列
1. 直接赋值
2. df.apply
3. df.assign
4. 按条件选择分组分别赋值

## 直接赋值
更改某一列的值，详见上节实例中的那个℃替换
    df[:,c1] = Series
新增某一列
    df[:,newc] = Series
## df.apply方法
df.apply本身返回的是一个Series，新增也用的是```df[:,newc]```
    df.apply(function,axis=1)
apply传入一个函数，和axis的值  
这个函数的参数是一个Series，axis是0的时候，函数内的Series的index就是df的index；如果是1，函数内的Series的index就是df的columns
    def function(x):
        if x[a]>2:
            return 0
原文：沿着df的一个轴应用了一个函数，函数的对象是一个Series，Series的index要么是DataFrame的index（axis=0），要么是DataFrame的columns（axis=1）

对某一列的每个值进行计数：
    df['c1'].value_counts()
## df.assign方法
可以同时新增多个列，不会修改原来的DataFrame，会返回一个新的DataFrame，包含原来的所有列和新增列
    df.assign(
        c1_key = lambda x : x['c2']+1
        c2_key = funtion
    )
## 按条件选择分组分别赋值
按条件先选择数据，然后对这部分数据赋值新列
    df['new_c']=''#这是第一种方法新增的列，直接赋值，这里出现了广播现象
    df.loc[ df[c1]>2,'new_c'] = '1'
    df.loc[ df[c1]<=2,'new_c'] = '2'

# Pandas数据统计函数
1. 汇总类统计
2. 唯一去重和按值计数
3. 相关系数和协方差

## 汇总类统计
提取所有数字列的统计结果
    df.describe()
count：计数
mean：平均值
std：标准差
min：最小值
25%、50%、75%：分位数
max：最大值

查看单个Series的数据
    df['c1'].mean()
    df['c1'].max()
    df['c1'].min()

## 唯一去重和按值计数
唯一去重，主要应用于非数值列，看看有哪些取值
按值计数，看看各个取值出现的次数
    df['c1'].unique()
    df['c1'].value_counts()

## 相关系数和协方差
协方差：正，说明X、Y同向变化，负为反向变化，值越大程度越高

协方差矩阵
    df.cov()
相关系数矩阵
    df.corr()

单独查看两列的相关系数
    df['c1'].corr(df['c2'])

# 缺失值的处理
1. 检测
isnull notnull，检测是否为空值，可以用于DataFrame和Series
2. 丢弃
dropna：丢弃、删除缺失值
    axis：删除行还是列，{0 or 'index', 1 or 'columns'}, default 0
    how：如果是any，任何值为空都删除；如果是all，所有值为空才删除
    inplace：True，修改当前df；False，返回新的df
3. 填充
fillna：填充空值
    value：用于填充的值，可以是单个值，也可以是个字典（key是列名，value是值）
    method：ffill，forward fill，使用前一个不为空的值填充；bfill，backward fill，使用后一个不为空的值填充
    axis：同上
    inplace：同上

## 检测
    df.isnull()
    df['c1'].isnull()
    df['c1'].notnull()
返回一个True和False组成的DataFrame或Series，notnull多用于数据筛选
## 丢弃
删除全nan的列
    df.dropna(axis="columns",how="all",inplace=True)
## 填充
c1列如果为空替换成0
    df.fillna({'c1':0})
等同于
    df.loc[:,'c1']=df['c1'].fillna(0)

## 保存excel
    df.to_excel("path",index=False) # 不将index输出

# SettingWithCopyWarning
    df[condition]['new_c'] = df['c1']-df['c2']
当出现这个报警，修改有时候成功有时候不成功
## 原因
警告的代码相当于df.get(condition).set(newc)
这个get操作可能是view也可能是copy，后面的set就不一定能成功
## 解决
修改在原始DataFrame上一步到位
方法1：
    df.loc[condition, 'new_c'] = ...
方法2：
    df_new = df[condition].copy()
    df_new['new_c']=...

# Pandas数据排序
    Series.sort_values(ascending=True, inplace=False)
ascending：True是升序，False是降序
```
DataFrame.sort_values(by, ascending=True, inplace=False)
```
by：字符串或字符串list，对单列排序或多列排序
ascending：此处可以为bool list，对应by的多列

说明：
如果是Series或单列DataFrame排序，都是根据那一列，扩展单元格，进行排序
如果是多列DataFrame排序，先根据第一个列进行排序，当第一个列的值相同时，根据第二个列的值进行排序
# Pandas字符串处理
1. 使用方法：先获取Series的str属性，然后在该属性上调用函数
2. 只能在字符串列上使用，不能在数字列上属性
3. DataFrame上没有str属性
4. Series.str不是Python的原生字符串，而是有自己的一套方法

str默认支持正则表达式
# Pandas的axis参数
+ axis=0或”index“：
  + 如果是单行操作，就指的是某一行
  + 如果是聚合操作，指的是跨行cross rows
+ axis=1或"columns"：
  + 如果是单列操作，就指的是某一列
  + 如果是聚合操作，值得是跨列cross columns
**按哪个axis，就是这个axis要动起来（类似被for遍历），其它的axis保持不动**

# Pandas的索引index的用途
1. 更方便的数据查询
2. 使用index可以获得性能提升
3. 自动的数据对齐功能
4. 更多更强大的数据结构支持

%timeit ipython的魔法命令，重复多次执行命令计算运行时间

索引是否递增，属性
df.index.is_monotonic_increasing
索引是否唯一，属性
df.index.is_unique
索引排序，方法
df.sort_index()

# Pandas的Merge
```pd.merge(left, right, how='inner', on=None, left_on=None, right_on=None, left_index=False, right_index=False, sort=True, suffixes=('_x', '_y'), copy=True, indicator=False, validate=None)```
+ left，right：要merge的DataFrame，或有name的Series
+ how：join类型，包含left，right，inner，outer
+ on，join的key，left和right都需要有
+ left_on、 right_on：当key不一样的时候可以分别指定
+ left_index、right_index：当join的key不在普通列而在index的时候
+ suffixes，如果列有重名，自动添加后缀

engine='python'的用处：sep包含2+个字符的时候，会认为是正则表达式，指定engine后，就是这两个字符，不是正则

## merge的时候数量的对齐关系
+ 一对一：
  关联的key都唯一，如 （学号，姓名）merge（学号，年龄），结果就是（学号，姓名，年龄）
+ 一对多：数据会被复制
  左边唯一key，右边不唯一key，如 （学号，姓名）merge（学号，[语文成绩、数学成绩]），结果会是[ （学号，姓名，语文成绩），（学号，姓名，数学成绩），左边的会被复制 ]
+ 多对多：数据会被复制
  左右key都不唯一，如 （学号，[语文成绩、数学成绩]）merge（学号，[篮球、排球]），结果会变成4条

## left、right、outer、inner join的区别
### left join
左边的key都会出现在结果里，右边的无法匹配则为null
### right join
右边的都会出现在结果里，左边的如果无法匹配则为null
### inner
两边都有的才会出现在结果里，交集
### outer
左边和右边的都会出现在结果里，如果无法匹配则为null，全集

## 非key字段重名
相同的columns名后会加上后缀
# Pandas的concat
+ 使用场景：
批量合并相同格式的Excel、给DataFrame添加行、给DataFrame添加列
+ 作用：
使用某种合并方式（inner/outer），沿着某个轴向，把多个Pandas对象合并成一个

```pandas.concat(objs, axis=0, join='outer', ignore_index=False)```
+ objs：一个列表，内容可以是DataFrame或Series，可以混合
+ axis：默认0，按行合并，1按列
+ join：合并的时候索引的对齐方式，outer：不匹配的索引也会保留
+ ignore_index：是否忽略掉原来的数据索引

```DataFrame.append(other, ignore_index=Fasle)```
append只有按行合并，没有按列合并，相当于concat按行的简写形式
+ other：DataFrame、Series、dict或列表

一行行给DataFrame添加数据：
```
    # 一个空的df
    df = pd.DataFrame(columns=['A'])
```
```python
    # 往里面一行一行写数据
    #方法1：
    for i in range(5):
        df = df.append( {'A':1}, ignore_index=True)
    #方法2：生成了一个列表，传入了concat
    pd.concat(
        [pd.DataFrame( [i],columns=['A'] ) for i in range(5)],
        ignore_index=True
    )
```

 ​ ​ ​ ​ ​ 
# 