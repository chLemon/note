# 岭回归Ridge Regression

RR

先标准化

多元回归的时候

$$\beta = (X^TX)^{-1}X^TY$$

其中

$$X^TX$$

在特征数多余样本数

样本矩阵间有强相关性，即不满秩【不满秩无法求逆，实际数据有误差，会使得结果不稳定，就像除0.0001,0.0005，偏差很小除完的误差却很大】

会无法求逆



$$\beta (k)= (X^TX+kI)^{-1}X^TY$$

那么加上一个k倍的单位方阵【扰动】，使得可以求逆

k叫岭参数

![image-20200610142903806](C:\Users\55012\AppData\Roaming\Typora\typora-user-images\image-20200610142903806.png)



![image-20200610142841368](C:\Users\55012\AppData\Roaming\Typora\typora-user-images\image-20200610142841368.png)

这里lambda就是k



## Lasso对岭回归的改进

擅长多重共线性的数据筛选

有偏估计

![image-20200610145259367](C:\Users\55012\AppData\Roaming\Typora\typora-user-images\image-20200610145259367.png)

![image-20200610145442007](C:\Users\55012\AppData\Roaming\Typora\typora-user-images\image-20200610145442007.png)

https://www.bilibili.com/video/BV1jt411R7kw?p=4

![image-20200610145722746](C:\Users\55012\AppData\Roaming\Typora\typora-user-images\image-20200610145722746.png)





# LAR最小角回归

LAR进行修正，可以求解Lasso



