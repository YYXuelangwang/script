
ios 开发过程中使用的脚本记录

## create_json_property.py

通过json/dictionary数据快速生成相对应的model，支持object-c和swift

数据可以从json文件中读取，这里你也可以改写成从剪切板中拿到json数据；
从剪切板中拿到数据的代码如下：
```python
    p = os.popen("pbpaste")
    lstr = p.read()
    p.close()
    print lstr
```

执行脚本的时候，会存在交互，需要你输入类名，如果是里面仍然含有dictionary，需要你告诉脚本，你是否需要再创建对应的model；

## ios_quick

安装到你的Alfred后，你可以按照以下步骤来实现相应的快速代码生成（目前只支持object-c）

* 快读生成属性的setter和getter方法

1. 复制你的属性到剪切板中，比如：`@property (nonatomic,strong)UIImageView * appLogoView;`
2. 在Alfred中输入`ios_qp`，对应`quick property complete`
3. 如果直接点击，则生成了`getter`方法到剪切板中；如果输入`ios_qp 1`，则是生成了`setter`方法到剪切板中
4. 你只要复制到对应的地方就可

* 快速生成ui布局对应的masonry代码

1. 复制你写的vsf语法语句，这里你也可以改动我的脚本，如果使用我的脚本，你需要按照我范例中的规则来书写，例如：`{[btn:UIButton|view](l:20,t:30)}{[text:UITextField|view](l:btn|r=8,y:btn=0)}`
2. 在Alfred中输入`ios_qu`，紧接着脚本就会生成代码到剪切板中
3. 你只要复制到对应的地方即可

