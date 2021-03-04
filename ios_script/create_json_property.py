#coding=utf8
import json
import io
import sys

# 拿到配置信息
def getConfig():
    # fconfig = open("./config.json")
    fconfig = open("/Users/yinyong/Work_New/qfun/create_json_property.json")
    config = json.loads(fconfig.read())
    print json.dumps(config)
    fconfig.close()
    return config

def save_file_to_swift(ret):
    f = open("/Users/yinyong/Work_New/qfun/tmp_mode.swift", 'w')
    # f.writelines(ret)
    f.write(ret)
    f.close()

def save_file_to_oc(ret):
    f = open("/Users/yinyong/Work_New/qfun/tmp_mode.h", 'w')
    # f.writelines(ret)
    f.write(ret)
    f.close()

def defineClassName():
    h=raw_input('please input new class name to continue\n') #获取用户输入
    newClassName = h
    return newClassName

def createNewClass(key):
    h=raw_input('please input whether need to create new class for ' + key + ' ?(1:yes, 0:no)')
    return int(h) == 1

def travelJsonToSwift(dic, space):
    className = defineClassName()
    # className = 'Jenkins'
    ret = space + "struct " + className + " : JsonToModel{\n"
    ll = ""
    for key, value in dic.items():
        print type(value)
        if type(value) == dict:
            if createNewClass(key):
                lt = travelJsonToSwift(value, space + '    ')
                skey = lt.keys()[0]
                ret += space + lt[skey]
                ret += space + '    let ' + key + ' :' + skey + '?\n'
                ll += "" + key + ':' + skey + '.modelWithJson(json["' + key + '"]),'
            else:
                ret += space + '    let ' + key + ' :[String:Any]?\n'
                ll += "" + key + ':json["' + key + '"].dictionaryObject,'
        elif type(value) == list:
            ret += space + '    let ' + key + ':[Any]?\n'
            ll += "" + key + ':json["' + key + '"].arrayObject,'
        elif type(value) == str or type(value) == unicode:
            ret += space + '    let ' + key + ':String?\n'
            ll += "" + key + ':json["' + key + '"].stringValue,'
        elif type(value) == int:
            ret += space + '    let ' + key + ':Int?\n'
            ll += "" + key + ':json["' + key + '"].intValue,'
        else:
            ret += ''

    ret += space + '    static func modelWithJson(_ json: JSON) -> ' + className + ' {\n'
    ret += space + '        return ' + className + '(' + ll[0:-1] + ')\n'
    ret += space + '    }\n'
    ret += space + '}\n'
    print ret
    return {className : ret}

def travelJsonToSwift2(dic, space):
    className = defineClassName()
    # className = 'Jenkins'
    ret = space + "class " + className + " : JsonToModel{\n"
    ll = ""
    for key, value in dic.items():
        print type(value)
        if type(value) == dict:
            if createNewClass(key):
                lt = travelJsonToSwift2(value, space + '    ')
                skey = lt.keys()[0]
                ret += space + lt[skey]
                ret += space + '    @objc dynamic var  ' + key + ' :' + skey + '?\n'
                ll += "" + key + ':' + skey + '.modelWithJson(json["' + key + '"]),'
            else:
                ret += space + '    @objc dynamic var  ' + key + ' = ""\n'
                ll += "" + 'json["' + key + '"].stringValue,'
        elif type(value) == list:
            ret += space + '    @objc dynamic var  ' + key + ' = ""\n'
            ll += ""  + 'json["' + key + '"].stringValue,'
        elif type(value) == str or type(value) == unicode:
            ret += space + '    @objc dynamic var  ' + key + ' = ""\n'
            ll += "" + 'json["' + key + '"].stringValue,'
        elif type(value) == int:
            ret += space + '    @objc dynamic var  ' + key + ' = 0\n'
            ll += "" + 'json["' + key + '"].intValue,'
        else:
            ret += ''

    ret += space + '    static func modelWithJson(_ json: JSON) -> ' + className + ' {\n'
    ret += space + '        return ' + className + '(value:[' + ll[0:-1] + '])\n'
    ret += space + '    }\n'
    ret += space + '}\n'
    print ret
    return {className : ret}

oc_dic = {}
def travelJsonToOC(dic, space):
    className = defineClassName()
    # className = 'Jenkins'
    ret = "@interface " + className + " : NSObject \n"
    for key, value in dic.items():
        print type(value)
        if type(value) == dict:
            if createNewClass(key):
                lt = travelJsonToOC(value, space + '    ')
                skey = lt.keys()[0]
                ret += '@property (nonatomic, strong) '+skey+' * ' + key + ';\n'
            else:
                ret += '@property (nonatomic, strong) NSDictionary * ' + key + ';\n'
        elif type(value) == list:
            ret += '@property (nonatomic, strong) NSArray * ' + key + ';\n'
        elif type(value) == str or type(value) == unicode:
            ret += '@property (nonatomic, strong) NSString * '+key+';\n'
        elif type(value) == int:
            ret += '@property (nonatomic, assign) NSInteger '+key +';\n'
        else:
            ret += ''
    ret += '@end\n'
    # print ret
    sdic = {className : ret}
    for k,v in sdic.items():
        oc_dic[k] = v
    return sdic 



if __name__ == "__main__":
    config = getConfig()
    # lc = travelJsonToSwift(config, "")    
    lc = travelJsonToSwift2(config, "")    
    skey = lc.keys()[0] 
    value = lc[skey]
    save_file_to_swift(value)

    # store_str = ""
    # travelJsonToOC(config, "")
    # for (key, value) in oc_dic.items():
    #     store_str += value
    # save_file_to_oc(store_str)
    # print store_str

