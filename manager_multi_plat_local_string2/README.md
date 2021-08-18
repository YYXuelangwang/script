
转换工具的使用说明：

### 支持功能：
1. 将英文的ios本地化文件Localizabel.strings和英文的android本地化文件android.xml，解析合并成csv文件；
2. 更新英文ios本地化文件/英文android本地化文件中，新增/修改的部分到csv文件中；
3. 从csv文件中解析出来各平台需要的本地化文件（包括：英文，繁体，俄语），

### 如何使用：

#### 初次生成csv文件

第一次运行脚本前，需要将ios和android本地化文件放在`../input`目录中，名字需要和下面的保持一致，当然直接改路径也行
```python
    # 配置你的路径，最好是相对路径，也可以拷贝到当前脚本目录下
    ios_path = '../input/localization_ios_en_value.strings'
    android_path = '../input/android_string_en_value.xml' 
    # 最终生成的csv文件地址
    csv_path = '../ios_android_txt.csv'
```

在终端中执行命令
```shell
$ python convert_localization_csv.py
```

#### 更新本地化文件中新增/修改到csv文件中

请确认你要更新的文件路径是否正确，参考[初次生成csv文件](#初次生成csv文件)，此时，你只需要确认你要更新的文件路径存在即可，
eg：你要更新ios本地化文件，你只需关注`ios_path`是否正确，`android_path`不用在乎，设置为None都没关系

需要注意: 脚本现在将文件路径和文件名写死，需要你确认的有：
1. 文件在`..\input`目录中是否存在，
2. 文件名是否正确：
 ios: localization_ios_en_value.strings localization_ios_cn_value.string
 android: android_string_en_value.xml android_string_cn_value.xml

之后直接在终端中运行命令
```shell
$ python convert_localization_csv.py
```

#### 从csv文件解析出各平台需要的本地化文件

在终端中运行命令
```shell
$ python convert_localization_csv.py -t 2
```

#### 脚本拓展

现在脚本中支持的语言有：
EN_VALUE = "en_value"
CN_VALUE = "cn_value"
RU_VALUE = "ru_value"

后期需要支持新的语言的话，按上面这种方式在对应的位置添加；

![image](https://github.com/YYXuelangwang/script/blob/master/manager_multi_plat_local_string2/convert_localization.png)

### 工具阅读/思路

1. 没有csv文件时，生成csv的思路

以android为基准来存储数据，将xml解析为字典；
```json
"xxx":  // 这里是同一份value
{
    "android_key":"abc",
    "ios_key":"bcd",
}
```

然而android里的xml，有几个特殊的元素需要注意：
```xml
      <plurals name="folder_image_count">
        <item quantity="one">Total %1$d card</item>
        <item quantity="other">Total %1$d cards</item>
      </plurals>
      <string-array name="friend_tab">
        <item>Club</item>
        <item>Friends</item>
    </string-array>
      <string name="reward_result_tip1">
        <Data>
            <![CDATA[Your reward request is being processed, if you need any further help, please contact us at <font color="#00CC80">payments@pokio.com.</font>]]></Data>
    </string>
```

因为在通过minidom来解析xml的时候，会将转义字符，比如：`;quot`，转换成对应的特殊字符；所以这里要处理一下，
处理的方式是：以字符串方式读取出xml中所有数据，然后将特殊的字符对应的键值对和原来的键值对进行替换；伪代码如下：
```shell
以文本文件的格式读取xml，
    如果读取到包含特殊符号`&`，
        遍历，拿到初始的tag，^(?=(<[ ]*string|<[ ]*string-array|<[ ]*plurals|<[ ]*array)).*$
        生成key: string|name|
        生成value:
        存在情况
            下一行有特殊符号`&`，在遍历到这一行的时候，需要过滤掉，继续执行循环
```

接下来就遍历ios列表，如果value在android的键值对中有，比如value = "xxx"
则只需要在dic中添加上ios的key即可，数据如下：
```json
"xxx":  // 这里是同一份value
{
    "android_key":"abc",
    "ios_key":"bcd",
}
```

如果没有和android公用的value，则添加新的键值对
```json
    "yyy":{
        "android":"",
        "ios":"ccc",
    }
```

最后将合并到一起的列表写入到csv中；

2. 如果有csv，则更新csv

伪代码如下：
```shell
      通过脚本比对上次和这次更新的不同进行比较，将不同的地方抠取出来；
      读取到csv里面的资源，生成一个总的list，每个item都是一个key_value
            拿到android的列表，new_list_android, key-value
            拿到ios的列表，new_list_ios，key-value
            遍历list, new_list逐个剔除掉重复的元素
                  new_list 新增
                  dic android_key ios_key value
                        if android_key and android_key in new_list_android:
                              if value == new_android
                                    if ios_key && ios_key in new_list_ios:
                                          if value == new_ios_value
            剩下不是重复的元素，就是新增的元素；然后进行合并，重复的元素进行整合；
            最后在总的list后面拼接上新增的元素；
            重新写入到csv文件中；
```

3. 将csv转化成对应的资源，这里就是将第一步再逆向走一遍就可以了，至于顺序，则是通过替换原始文件中的数据来实现的；

```shell
读取到csv里面的资源，生成一个总的list，
    遍历list，
    dic android_key ios_key en_value cn_value ru_value
        if android_key/ios_key:
            检查对应的value，有值，就写入对应的文件中；
```


