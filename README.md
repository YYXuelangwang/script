# script
script which auto manage your work

## manager_reference_of_xcodeproj.rb

使用ruby来自动管理文件在xcodeproj/xcodeworkspace中的删除（删除引用）和添加

需要先安装xcodeproj
```
$ gem install xcodeproj
```
参考资源路径：
1. [使用代码为xcode工程添加文件](https://draveness.me/bei-xcodeproj-keng-de-zhe-ji-tian)
2. [CocoaPods/Xcodeproj](https://github.com/CocoaPods/Xcodeproj)
3. [CocoaPods/Xcodeproj_API](https://www.rubydoc.info/gems/xcodeproj/Xcodeproj/Project/Object/AbstractBuildPhase#)

## ios_script

该文件下存储了在写ios代码中，因为重复工作比较多，所以问了节省部分时间，就写了这些脚本方便自己提升普通工作的开发效率；
能实现的功能如下（脚本都是使用python来实现）：
* 通过json/dictionary快速生成相对应的model
* 复制属性，快速生成setter和getter方法
* 通过自己定义的vsf语法(例如：`{[btn:UIButton|view](l:20,t:30)}{[text:UITextField|view](l:btn|r=8,y:btn=0)}`)，生成对应的oc代码(masonry)来实现ui布局

## manager_multi_plat_local_string2

将android的xml和ios的strings文件整理到一起，成为最终的csv文件，支持逆向解析

支持功能：
1. 将英文的ios本地化文件Localizabel.strings和英文的android本地化文件android.xml，解析合并成csv文件；
2. 更新英文ios本地化文件/英文android本地化文件中，新增/修改的部分到csv文件中；
3. 从csv文件中解析出来各平台需要的本地化文件（包括：英文，繁体，俄语）