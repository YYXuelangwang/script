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

## manager_multi_plat_local_string2

将android的xml和ios的strings文件整理到一起，成为最终的csv文件，支持逆向解析

支持功能：
1. 将英文的ios本地化文件Localizabel.strings和英文的android本地化文件android.xml，解析合并成csv文件；
2. 更新英文ios本地化文件/英文android本地化文件中，新增/修改的部分到csv文件中；
3. 从csv文件中解析出来各平台需要的本地化文件（包括：英文，繁体，俄语）
