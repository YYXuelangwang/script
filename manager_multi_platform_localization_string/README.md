
#### parse_xml.py

##### 概要

多平台本地化合成管理工具，支持ios/android

可以实现的功能：
1. 将ios中localization.strings转换为xml文件，
2. 将多个android中的strings.xml文件合并到同一个xml文件中；
3. 将ios中localization.strings和android的xml文件合并到最终的xml文件中，默认是final.xml文件
4. 逆向解析final.xml文件，生成ios平台需要的localization.strings文件，生成android需要的strings.xml文件
5. 支持ios中localization.strings和android中strings.xml中部分通用key-value键值对的维护

##### 如何使用

1. 将ios中localization.strings中的改动更新到final.xml文件中；

```bash
$ py parse_xml.py -t 1 -i 你的localization.strings文件路径 -s ios [-o final_strings.xml]'
```

说明： `-o final_strings.xml`是可选值，指定你要最终生成的文件，可以是xml文件，可以是文件夹，默认是生成`final_strings.xml`和脚本在同级目录中

如果你觉得每次输入文件路径都比较麻烦，可以直接在generate_pase_xml_command.py中修改对应ios文件路径，生成可执行的shell/bash文件即可；

2. 将更新后的final.xml文件解析到你上次保存下来的`*.strings`文件路径下；

```bash
$ py parse_xml.py -s ios final_strings.xml
```

说明：这里的final_strings.xml，你也可以自己定义，根据你上次生成`final_strings.xml`的地址路径保持一致；

如果你觉得每次输入文件路径都比较麻烦，可以直接在generate_pase_xml_command.py中修改对应`final_strings.xml`文件路径，生成可执行的shell/bash文件即可；

3. 将android中多个strings.xml文件更新到final_strings.xml文件中

```bash
$ py parse_xml.py -t 1 -a 你需要归并到同一个xml文件的多个xml文件 -u 两端可以通用key-value的xml文件 -s android
```

说明：
* 需要归并到同一个xml文件的多个xml文件：一个字符串，以逗号隔开多个文件路径，eg:`project/strings.xml,project/toast_string.xml`；
* 两端可以通用key-value的xml文件：android端通用的key-value的`project/universal_android.xml`文件路径，这个文件是脚本帮你生成

如果你觉得每次输入文件路径都比较麻烦，可以直接在generate_pase_xml_command.py中修改对应android文件路径，生成可执行的shell/bash文件即可；

4. 将更新后的final.xml文件解析到你android项目路径下；

```bash
$ py parse_xml.py -s android final_strings.xml
```

说明：这里的final_strings.xml，你也可以自己定义，根据你上次生成`final_strings.xml`的地址路径保持一致；

如果你觉得每次输入文件路径都比较麻烦，可以直接在generate_pase_xml_command.py中修改对应`final_strings.xml`文件路径，生成可执行的shell/bash文件即可；

5. 通用key-value模块，universal_android.xml

android端会存在一个universal_android.xm文件，用来存储两端（ios/android）通用的key-value键值对；而在ios端，我是通过设置一个标志位来实现的，（`UNIVERSL_TYPE_TAG = 'universal type strings for different platform'`）标志位以下是通用的key-value键值对，标志位以上是不可通用的key-value键值对；

##### 为何制作这个工具

因为大部分公司（那种后期发展到需要多个国家语言适配，比如我现在公司），而现有项目又一直都持续更新在，（两端ios/android），那么很有必要设计出一套比较合理可持续更新和维护的语言管理工具;

之前查阅资料，发现ios这边存在着xliff（国际本地化支持标准）的可支持，而在android这边发现没有办法通用，于是就做了这个工具方便维护；不管后期是开发，还是产品都可以来维护，只需要将这些脚本放在一个通用的git仓库中管理就可以了；

##### 后记

如果你还有什么新的点子，意见，bug（当然希望越少越好）；欢迎你的留言


