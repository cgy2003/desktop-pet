# Desktop Pet

## 功能简介

#### 宠物主体

![image-20240317163534636](.\resources\png\image-20240317163534636.png)

1. **宠物互动功能：**

  - 静止时能做出较为自然的静止动作，而不是简单地贴一张图片
  - 左键单击可以让宠物随机做出一个动作
  - 可以拖动宠物至用户需要的位置

2. **报时功能：**

  - 整点可以进行报时
  - 用户可以自由选择打开或者关闭这个功能

3. **隐藏/显示：**

  - 可以供用户自由隐藏和显示宠物

4. **闹钟提醒：**

  -  考虑到电脑工作者往往会在静音情况下工作，因而到了设定的时间会进行弹框提醒而不是闹铃

![image-20240317163442252](.\resources\png\image-20240317163442252.png)

#### 聊天室

**对话功能：**

- 需要有一个良好的聊天交互界面
- 宠物可以通过自然语言处理技术理解用户的意思并做出合理的回答

![image-20240317163714371](.\resources\png\image-20240317163714371.png)

#### 闹钟设置界面

主要的设置功能有：

- 设置闹钟时间保存
- 修改已有闹钟的时间
- 删除指定时间的闹钟
- 当前时间的显示

![image-20240317163734013](C:\Users\Lenovo\AppData\Roaming\Typora\typora-user-images\image-20240317163734013.png)

## 文件结构

```shell
Desktop Pet
│  alarm.py  #闹钟设置模块
│  alarms.db #数据库模块，存储闹钟信息
│  pet.py	#宠物主体部分，也是程序入口
│  README.md
│  talk.py		#聊天室模块
│  requirements.txt   # 包含项目所需的依赖库列表
│
├─resources
│  └─png 	#装载各种图片文件，由于图片文件过多，这里不过多展示
│
└─__pycache__
        alarm.cpython-311.pyc
        talk.cpython-311.pyc
```

## 运行

- 环境：
	- 操作系统：windows
	
	- python版本：python3.8或python3.11（以上为作者测试过的版本，其他或许也行）
	
	- requirements:
	
	 ```shell
	 PyQt5
	 openai
	 datetim
	 ```
	
	-  环境准备及运行
	
	  ```shell
	  conda create -n desktop_pet python=3.8
	  conda activate desktop_pet
	  pip install -r requirements
	  python pet.py
	  ```
	
	  