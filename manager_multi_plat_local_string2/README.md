
转换工具的使用说明：

### 支持功能：
1. 将英文的ios本地化文件Localizabel.strings和英文的android本地化文件android.xml，解析合并成csv文件；
2. 更新英文ios本地化文件/英文android本地化文件中，新增/修改的部分到csv文件中；
3. 从csv文件中解析出来各平台需要的本地化文件（包括：英文，繁体，俄语），

### 如何使用：

#### 初次生成csv文件

第一次运行脚本前，需要设置脚本中，ios本地化文件路径，不能为空；android本地化文件路径，不能为空；
```python
    # 配置你的路径，最好是相对路径，也可以拷贝到当前脚本目录下
    ios_path = '../client_ios2/Pokio/en.lproj/Localizable.strings'    
    android_path = 'strings_en.xml'
    csv_path = 'result.csv'
```

在终端中执行命令
```shell
$ python convert_localization_csv.py
```

#### 更新本地化文件中新增/修改到csv文件中

请确认你要更新的文件路径是否正确，参考[初次生成csv文件](#初次生成csv文件)，此时，你只需要确认你要更新的文件路径存在即可，
eg：你要更新ios本地化文件，你只需关注`ios_path`是否正确，`android_path`不用在乎，设置为None都没关系

之后直接在终端中运行命令
```shell
$ python convert_localization_csv.py
```

#### 从csv文件解析出各平台需要的本地化文件

在终端中运行命令
```shell
$ python convert_localization_csv.py -t 2
```

#### 隐藏功能

1. 支持从其他语言更新到csv文件中，比如繁体本地化文件更新到csv文件中；因为涉及代码改动和潜在风险，不对外提供，

操作：
  * 修改代码中的，action_type = 3
  * 修改其他语言的路径
  * 修改方法update_csv_other_lang中CN_VALUE为你要更新的语言；

```python
    # 不对外开放，更新其他语言翻译，需要确认你的文件是否正确
    elif action_type == 3:
        android_path = 'strings_cn.xml'
        # ios_path = '../client_ios2/Pokio/zh-Hant.lproj/Localizable.strings'
        ios_path = 'none'
        update_csv_other_lang(csv_path, CN_VALUE, ios_path, android_path)
```

