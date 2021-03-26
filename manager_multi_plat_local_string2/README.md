
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

![image](https://github.com/YYXuelangwang/script/manager_multi_plat_local_string2/blob/master/convert_localization.png)


