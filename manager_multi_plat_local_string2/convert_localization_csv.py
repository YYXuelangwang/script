# -*- coding: UTF-8 -*-

from xml.dom.minidom import parse
import xml.dom.minidom
from xml.dom.minidom import Node

import re
from optparse import OptionParser

import os

import collections
import copy

import csv

import json

ANDROID = "android"
VALUE = "value"
IOS = "ios"

def get_lines(filePath):
    f = open(filePath)
    lines = f.readlines()
    f.close()
    return lines

def read_ios_localization(path):
    lines = get_lines(path)
    ret = {}
    ret = collections.OrderedDict() 
    # num = 0
    pass_lines = []
    for l in lines:
        if l.find("=") > 0:
            # 1523
            # num = num + 1
            index = lines.index(l)

            if index in pass_lines:
                continue

            if l.startswith('//"'):
                continue

            l1 = l.split("=",1)
            key = l1[0].strip().strip('"') 
            value = l1[1]
            lastIndex = index
            loop = True
            if key == "message.toolBar.inputPlaceHolder":
                print 'break'
            while loop:
                loop = (not re.match(r'[ ]*"[\s\S]*[^\\]";[\s\S]*', value)) and (not re.match(r'[ ]*"";[\s\S]*', value))
                if loop:
                    lastIndex = lastIndex + 1
                    if lastIndex >= len(lines):
                        print 'the line index out of lines for read ios localization'
                        print 'key: %s\n value: %s\n' % (key, value)
                        loop = False
                    else:
                        value = value + lines[lastIndex]
                        pass_lines.append(lastIndex)
            
            l2 = value.split(";//",1)
            if len(l2) > 1:
                value = l2[0].strip('\n').strip()[:-1].lstrip('"')
            else:
                value = l2[0].strip('\n').strip()[:-2].lstrip('"') 
            # if key in ret.keys():
            #     print key
            #     num = num + 1
            if key.find("|") > 0:
                print "can't set key contain '|', your key: %s" % key
                exit(1)
            ret[l1[0].strip().strip('"')] = value
    # 34
    # print num
    return ret

def read_android_special_localization(path):
    lines = get_lines(path)
    ret = {}
    ret = collections.OrderedDict() 
    # 不处理的行
    pass_line = []
    for l in lines:
        if l.find('&') > 0:
            index = tag_index = lines.index(l)

            if index in pass_line:
                continue

            tag_line = l
            loop = True
            parse_continue = False
            while loop:
                loop = (not re.match(r'^[ ]*(?=(<[ ]*string|<[ ]*string-array|<[ ]*plurals|<[ ]*array))[\s\S]*$', tag_line)) and (not re.match(r'^\t*(?=(<[ ]*string|<[ ]*string-array|<[ ]*plurals|<[ ]*array))[\s\S]*$', tag_line))
                if loop:
                    tag_index = tag_index - 1
                    if tag_index <= 0:
                        loop = False
                        print 'something happend, the head lines contain "&"'
                        parse_continue = True
                        print l
                    else:
                        tag_line = lines[tag_index]
            
            if parse_continue:
                continue

            total_line = ""
            if tag_index == index:
                total_line = l
            else:
                for i in range(tag_index, index + 1):
                    total_line = total_line + lines[i]

            loop = True
            last_index = index
            while loop:
                loop = (not re.match(r"^[ ]*<[ ]*(\w+) [\s\S]*</\1>(\r)*\n$", total_line)) and (not re.match(r"^\t*<[ ]*(\w+) [\s\S]*</\1>(\r)*\n$", total_line)) 
                if loop:
                    if last_index + 1 < len(lines):
                        last_index = last_index + 1
                        pass_line.append(last_index)
                        total_line = total_line + lines[last_index]
                    else:
                        loop = False
                        print 'has get the end of file'
                        parse_continue = True
                        print l

            if re.match(r'^[ ]*<[ ]*string [\s\S]*$', total_line) or re.match(r'^\t*<[ ]*string [\s\S]*$', total_line):
                key = 'string|' + total_line.split('"', 2)[1]
                value = l[total_line.find('>') + 1:total_line.rfind('<')]
                ret[key] = value
            else:
                print "you have a special type , we haven't support\n %s" % total_line
        
    return ret

def read_android_localization(path):
    DOMTree = xml.dom.minidom.parse(path)
    root = DOMTree.documentElement
    # resource = root.getElementsByTagName('resources')[0]
    nodes = root.childNodes
    ret = {}
    ret = collections.OrderedDict()
    for node in nodes:
        if node.nodeType == Node.ELEMENT_NODE:
            if node.tagName == "string":
                if node.hasAttribute("name"):
                    # print "title: %s" % node.getAttribute("name")
                    if node.childNodes and len(node.childNodes) > 0:
                        key = node.getAttribute("name")
                        if len(node.childNodes) == 1:
                            subNode = node.childNodes[0]
                            # if subNode.nodeType == Node.TEXT_NODE:
                            #     key1 = "string" + "|" + key 
                            #     ret[key1] = (node.childNodes[0].data).encode('utf-8')
                            # elif subNode.nodeType == Node.ELEMENT_NODE:
                            #     if subNode.tagName == "Data":
                            #         for sNode in subNode.childNodes:
                            #             if sNode.nodeType == Node.CDATA_SECTION_NODE:
                            #                 key1 = "string" + "|" + key
                            #                 ret[key1] = ("Data" + "|" + sNode.nodeValue).encode('utf-8')
                                    
                            #             elif sNode.nodeType != Node.TEXT_NODE and sNode.nodeType != Node.COMMENT_NODE:
                            #                 print "title: %s can't analysis, the content not support" % key 
                            #     else:
                            #         # print "title: %s can't analysis, the content not support" % key 
                            #         key1 = "string" + "|" + key
                            #         line = subNode.toxml()
                            #         ret[key1] = line.encode('utf-8')
                                
                            # else:
                            #     print "title: %s can't analysis, the content shoud just be text node" % key
                            
                            line = subNode.toxml()
                            key1 = "string" + "|" + key
                            ret[key1] = line.encode('utf-8') 
                        else:
                            line = ""
                            for subNode in node.childNodes:
                                line = line + subNode.toxml()
                                # if subNode.nodeType == Node.ELEMENT_NODE:
                                #     if subNode.tagName == "Data":
                                #         for sNode in subNode.childNodes:
                                #             if sNode.nodeType == Node.CDATA_SECTION_NODE:
                                #                 key1 = "string" + "|" + key
                                #                 ret[key1] = ("Data" + "|" + sNode.nodeValue).encode('utf-8')
                                        
                                #             elif sNode.nodeType != Node.TEXT_NODE and sNode.nodeType != Node.COMMENT_NODE:
                                #                 print "title: %s can't analysis, the content not support" % key 
                                #     else:
                                #         print "title: %s can't analysis, the content not support" % key
                                # elif subNode.nodeType == Node.TEXT_NODE:
                                #     print subNode.data
                                #     pass
                            key1 = "string" + "|" + key
                            ret[key1] = line.encode('utf-8')
                        # line = '"'+node.getAttribute("name")+'" = "'+node.childNodes[0].data+'";\n' 
            elif node.tagName == "plurals":
                if node.hasAttribute("name"):
                    key = "plurals" + "|" + node.getAttribute("name")
                    for sub in node.getElementsByTagName("item"):
                        if sub.hasAttribute("quantity"):
                            key1 = key + "|" + sub.getAttribute("quantity")
                            ret[key1] = (sub.childNodes[0].data).encode('utf-8')
            elif node.tagName == "string-array":
                if node.hasAttribute("name"):
                    key = "string-array" + "|" + node.getAttribute("name")
                    index = 0
                    for sub in node.getElementsByTagName("item"):
                        key1 = key + "|" + str(index)
                        ret[key1] = (sub.childNodes[0].data).encode('utf-8')
                        index = index + 1
            elif node.tagName == "array":
                if node.hasAttribute("name"):
                    key = "array" + "|" + node.getAttribute("name")
                    index = 0
                    for sub in node.getElementsByTagName("item"):
                        key1 = key + "|" + str(index)
                        ret[key1] = (sub.childNodes[0].data).encode('utf-8')
                        index = index + 1 
    
    # 获取转义字符标志的词典
    special_dic = read_android_special_localization(path)
    for k, v in special_dic.items():
        if k in ret.keys():
            ret[k] = v

    return ret

def mix_ios_android_dic(ios_dic, android_dic):
    ret = []
    # 以android为基准
    for k, v in android_dic.items():
        dic = {
            ANDROID:k,
            VALUE:v,
            IOS:"",
        }
        loop = True
        ios_key = ""
        while loop:
            if v in ios_dic.values():
                k1 = list(ios_dic.keys())[list(ios_dic.values()).index(v)]
                ios_key = ios_key + k1 + "|"
                ios_dic.pop(k1)
            else:
                loop = False            
        if len(ios_key) > 0:
            ios_key = ios_key[:-1]
            # print ios_key
            dic[IOS] = ios_key
        ret.append(dic)

    not_mult_values = []
    for k, v in ios_dic.items():
        if not v in not_mult_values:
            not_mult_values.append(v)
    for v in not_mult_values:
        loop = True
        ios_key = ""
        while loop:
            if v in ios_dic.values():
                k1 = list(ios_dic.keys())[list(ios_dic.values()).index(v)]
                ios_key = ios_key + k1 + "|"
                ios_dic.pop(k1)
            else:
                loop = False            
        if len(ios_key) > 0:
            ios_key = ios_key[:-1]
            # print ios_key
            dic = {
                ANDROID:"",
                VALUE:v,
                IOS:ios_key,
            } 
            ret.append(dic) 
    for k, v in ios_dic.items():
        dic = {
            ANDROID:"",
            VALUE:v,
            IOS:k,
        } 
        ret.append(dic)
    
    return ret

SPECIAL_FILE_CODE = "\xef\xbb\xbf"
ANDROID_KEY = "android_key"
IOS_KEY = "ios_key"
EN_VALUE = "en_value"
CN_VALUE = "cn_value"
RU_VALUE = "ru_value"
def write_to_csv(path, ret_list, first=None):
    f = open(path, 'w')
    csvWrite = csv.DictWriter(f, [ANDROID_KEY, IOS_KEY, EN_VALUE, CN_VALUE, RU_VALUE])
    csvWrite.writeheader()
    for dic in ret_list:
        if first:
            writeDic = {
                ANDROID_KEY:dic[ANDROID],
                IOS_KEY:dic[IOS],
                EN_VALUE:(dic[VALUE])
            }
            # print writeDic
            csvWrite.writerow(writeDic)
        else:
            csvWrite.writerow(dic)
    f.close()

def read_csv(path):

    # 检查文件是否是特殊编码开头
    lines = get_lines(path)
    startLine = lines[0]
    if startLine.startswith(SPECIAL_FILE_CODE):
        f = open(path, 'w')
        lines[0] = startLine.split(SPECIAL_FILE_CODE, 1)[1]
        f.writelines(lines)
        f.close()

    f = open(path, 'r')
    csvReader = csv.DictReader(f)
    # 底层会调用拿到header
    lDic = csvReader.next()
    # lDic = csvReader.next()
    ret = []
    loop = True
    while loop:
        ret.append(lDic)
        try:
            lDic = csvReader.next()
        except StopIteration:
            loop = False
    f.close()
    return ret

def update_android_dic(ret_list, android_dic, lang=EN_VALUE):
    for dic in ret_list:
        k = dic[ANDROID_KEY]
        v = dic[lang]
        if k and len(k) > 0:
            if k in android_dic.keys():
                dic[lang] = android_dic[k]
                newValue = android_dic.pop(k)
                if dic[IOS_KEY] and len(dic[IOS_KEY]) > 0 and v != newValue:
                    print "pay attention: you changed the universal value for ios/android key:%s \n oldValue:%s \n newValue:%s" % (k, v, newValue)
        else:
            if lang == EN_VALUE and (v in android_dic.values()):
                android_key = list(android_dic.keys())[list(android_dic.values()).index(v)]
                dic[ANDROID_KEY] = android_key
                android_dic.pop(android_key) 

    for k, v in android_dic.items():
        dic = {
            IOS_KEY:"",
            lang:v,
            ANDROID_KEY:k,
        } 
        ret_list.append(dic) 

    return ret_list

def update_ios_dic(ret_list, ios_dic, lang=EN_VALUE):
    # split_list = []
    split_dic = {}
    for dic in ret_list:
        k = dic[IOS_KEY]
        v = dic[lang]
        if k and len(k) > 0:
            klist = k.split("|")
            if len(klist) == 1:
                if k in ios_dic.keys():
                    if v == ios_dic[k]:
                        ios_dic.pop(k)
                    else:
                        if len(dic[ANDROID_KEY]) > 0:
                            tmp_dic = {}
                            for k1,v1 in dic.items():
                                tmp_dic[k1] = v1
                            tmp_dic[ANDROID_KEY] = ""
                            tmp_dic[lang] = ios_dic.pop(k)
                            # split_list.append(tmp_dic)
                            split_dic[k] = tmp_dic
                            dic[IOS_KEY] = ""
                            if dic[ANDROID_KEY] and len(dic[ANDROID_KEY]) > 0:
                                print "pay attention: you changed the universal value for ios/android key:%s \n oldValue:%s \n newValue:%s" % (k, v, tmp_dic[lang])
                        else:
                            dic[lang] = ios_dic.pop(k)
                elif k in split_dic.keys():
                    print "repetition attention: you find a repeat key:%s \n oldValue:%s \n newValue:%s" % (k, v, split_dic[k])
                    tmpdic = split_dic.pop(k)
                    dic[lang] = tmpdic[lang]
                        
            else:
                nklist = klist[:]
                split_keys = []
                for skey in klist:
                    if skey in ios_dic.keys():
                        if v == ios_dic[skey]:
                            ios_dic.pop(skey)
                        else:
                            nklist.remove(skey)
                            split_keys.append(skey)
                if len(nklist) != len(klist):
                    ios_key = ""
                    for skey in nklist:
                        ios_key = ios_key + skey + "|"
                    if len(ios_key) > 0:
                        ios_key = ios_key[:-1]
                    dic[IOS_KEY] = ios_key
                    # 需要挪取出来的key
                    ios_key = ""
                    tmp_dic = {}
                    for k1,v1 in dic.items():
                        tmp_dic[k1] = v1
                    tmp_dic[ANDROID_KEY] = ""
                    tmp_dic[IOS_KEY] = ""
                    tmp_dic[lang] = ""
                    for k1 in split_keys:
                        if tmp_dic[lang] == "":
                            tmp_dic[lang] = ios_dic[k1]
                        if tmp_dic[lang] == ios_dic[k1]:
                            ios_key = ios_key + k1 + "|"
                            ios_dic.pop(k1)
                        else:
                            if ios_key.endswith('|'):
                                ios_key = ios_key[:-1]
                                tmp_dic[IOS_KEY] = ios_key
                                # split_list.append(copy.deepcopy(tmp_dic))
                                split_dic[ios_key] = copy.deepcopy(tmp_dic)
                            ios_key = k1 + "|"
                            tmp_dic[IOS_KEY] = ""
                            tmp_dic[lang] = ios_dic.pop(k1)
                    if ios_key.endswith('|'):
                        ios_key = ios_key[:-1]
                        tmp_dic[IOS_KEY] = ios_key
                        # split_list.append(copy.deepcopy(tmp_dic)) 
                        split_dic[ios_key] = copy.deepcopy(tmp_dic)
        else:
            if lang == EN_VALUE and (v in ios_dic.values()):
                ios_key = list(ios_dic.keys())[list(ios_dic.values()).index(v)]
                dic[IOS_KEY] = ios_key
                ios_dic.pop(ios_key)

    for k, v in ios_dic.items():
        dic = {
            IOS_KEY:k,
            lang:v,
            ANDROID_KEY:"",
        } 
        ret_list.append(dic) 

    # 添加裁剪出来的键值对
    ret_list.extend(split_dic.values())
    return ret_list

def update_csv(csv_path, ios_path=None, android_path=None):
    ret_list = read_csv(csv_path)
    if android_path and os.path.exists(android_path):
        android_dic = read_android_localization(android_path)
        ret_list = update_android_dic(ret_list, android_dic)
    if ios_path and os.path.exists(ios_path):
        ios_dic = read_ios_localization(ios_path)
        ret_list = update_ios_dic(ret_list, ios_dic)
    write_to_csv(csv_path, ret_list)

def update_csv_other_lang(csv_path, lang=EN_VALUE, ios_path=None, android_path=None):
    ret_list = read_csv(csv_path)
    if android_path and os.path.exists(android_path):
        android_dic = read_android_localization(android_path)
        ret_list = update_android_dic(ret_list, android_dic, lang)
    if ios_path and os.path.exists(ios_path):
        ios_dic = read_ios_localization(ios_path)
        ret_list = update_ios_dic(ret_list, ios_dic, lang)
    write_to_csv(csv_path, ret_list)

def create_first_csv(csv_path, ios_path, android_path):
    if (not ios_path) or (not os.path.exists(ios_path)):
        print "first create csv, you should specify the ios localization path"
        exit(1)

    if (not android_path) or (not os.path.exists(android_path)):
        print "first create csv, you should specify the android xml path"
        exit(1)

    ios_dic = read_ios_localization(ios_path)
    android_dic = read_android_localization(android_path)
    ret = mix_ios_android_dic(ios_dic, android_dic)
    write_to_csv(csv_path, ret, first=True)
        
def convert_csv_to_ios_localization(csv_path, ios_path, lang):
    ret_list = read_csv(csv_path)
    ret = []
    for dic in ret_list:
        k = dic[IOS_KEY]
        v = dic[lang]
        if k and len(k) > 0 and v and len(v) > 0:
            klist = k.split("|")
            if len(klist) == 1:
                if v and len(v) > 0:
                    line = '"' + k + '" = "' + v + '";\n'
                    ret.append(line)
            else:
                for skey in klist:
                    line = '"' + skey + '" = "' + v + '":\n'
                    ret.append(line)
    
    f = open(ios_path, 'w')
    f.writelines(ret)
    f.close()

def convert_csv_to_ios_ordered_localization(csv_path, ios_path, lang, source_ios_path):
    if (not source_ios_path) or (not os.path.exists(source_ios_path)):
        convert_csv_to_ios_localization(csv_path, ios_path, lang)
        return
    ret_list = read_csv(csv_path)
    ordered_dic = read_ios_localization(source_ios_path)
    for dic in ret_list:
        k = dic[IOS_KEY]
        v = dic[lang]
        if k and len(k) > 0 and v and len(v) > 0:
            klist = k.split("|")
            if len(klist) == 1:
                if v and len(v) > 0:
                    ordered_dic[k] = v
            else:
                for skey in klist:
                    ordered_dic[skey] = v

    ret = []
    for k, v in ordered_dic.items():
        line = '"' + k + '" = "' + v + '";\n'
        ret.append(line)

    f = open(ios_path, 'w')
    f.writelines(ret)
    f.close()
    


def addElementForParent(dom, parent, name, value, nodeType):
    if nodeType == Node.ELEMENT_NODE:
        item = dom.createElement('string')
        item.setAttribute('name', name)

        if value.count('<') > 0 and value.count('>') > 0:
            value = value.strip('\n').strip()
            index = value.find('<')
            first = value[0:index]
            content = value[index:]
            if len(first) > 1:
                text = dom.createTextNode(first)
                item.appendChild(text)
            index = content.rfind('>')
            last = content[index + 1:]
            content = content[0:index+1]
            print name
            # if name == "contact_us_text":
            #     print "break"
            #     return
            try:
                DOMTree = xml.dom.minidom.parseString(content.decode('utf-8'))
                root = DOMTree.documentElement
                # nodes = root.childNodes
                # for node in nodes:
                #     item.appendChild(node)
                item.appendChild(root)
            except:
                text = dom.createTextNode(content)
                item.appendChild(text)

            if len(last) > 0:
                text = dom.createTextNode(last)
                item.appendChild(text)
        else:
            text=dom.createTextNode(value)
            item.appendChild(text)

        # text=dom.createTextNode(value)
        # item.appendChild(text)

        parent.appendChild(item)
        # print name + ' => ' + value
        # parent.appendChild(dom.createTextNode('\n')) 
    elif nodeType == Node.CDATA_SECTION_NODE:
        item = dom.createElement('string')
        item.setAttribute('name', name) 
        subItem = dom.createElement('Data')
        cadata = dom.createCDATASection(value)
        subItem.appendChild(cadata)
        item.appendChild(subItem)
        parent.appendChild(item)
        
    elif nodeType == Node.COMMENT_NODE:
        item = dom.createComment(value)
        parent.appendChild(item)
        # parent.appendChild(dom.createTextNode('\n')) 

def convert_csv_to_android_xml(csv_path, android_path, lang):
    impl = xml.dom.minidom.getDOMImplementation()
    dom = impl.createDocument(None, "resources", None)
    root = dom.documentElement

    ret_list = read_csv(csv_path)
    for dic in ret_list:
        k = dic[ANDROID_KEY]
        v = dic[lang]
        if k and len(k) > 0 and v and len(v) > 0:
            if k.startswith("string|"):
                if not v.startswith("Data|"):
                    addElementForParent(dom, root, k.split("|", 1)[1], v, Node.ELEMENT_NODE)
                else:
                    addElementForParent(dom, root, k.split("|", 1)[1], v.split("|", 1)[1], Node.CDATA_SECTION_NODE)
            elif k.startswith("plurals|"):
                klist = k.split("|")
                key = klist[1]
                plist = root.getElementsByTagName("plurals")
                find = False
                for plu in plist:
                    pkey = plu.getAttribute("name")
                    if pkey == key:
                        find = True
                        item = dom.createElement('item')
                        item.setAttribute('quantity', klist[2])
                        text=dom.createTextNode(v)
                        item.appendChild(text)
                        plu.appendChild(item)
                if not find:
                    plu = dom.createElement('plurals')
                    plu.setAttribute('name', key)
                    item = dom.createElement('item')
                    item.setAttribute('quantity', klist[2])
                    text=dom.createTextNode(v)
                    item.appendChild(text)
                    plu.appendChild(item)
                    root.appendChild(plu)
            elif k.startswith("string-array|"):
                klist = k.split("|")
                key = klist[1]
                alist = root.getElementsByTagName("string-array")
                find = False
                for arr in alist:
                    akey = arr.getAttribute("name")
                    if akey == key:
                        find = True
                        item = dom.createElement('item')
                        text=dom.createTextNode(v)
                        item.appendChild(text)
                        arr.appendChild(item) 
                if not find:
                    arr = dom.createElement("string-array")
                    arr.setAttribute("name", key)
                    item = dom.createElement('item')
                    text=dom.createTextNode(v)
                    item.appendChild(text)
                    arr.appendChild(item)  
                    root.appendChild(arr)
            elif k.startswith("array|"):
                klist = k.split("|")
                key = klist[1]
                alist = root.getElementsByTagName("array")
                find = False
                for arr in alist:
                    akey = arr.getAttribute("name")
                    if akey == key:
                        find = True
                        item = dom.createElement('item')
                        text=dom.createTextNode(v)
                        item.appendChild(text)
                        arr.appendChild(item) 
                if not find:
                    arr = dom.createElement("array")
                    arr.setAttribute("name", key)
                    item = dom.createElement('item')
                    text=dom.createTextNode(v)
                    item.appendChild(text)
                    arr.appendChild(item)  
                    root.appendChild(arr)
    
    f = open(android_path, "w")
    dom.writexml(f,addindent="\t",newl="\n", encoding="utf-8")
    f.close()

    # 需要进行一次转码，因为写入的时候，xml将所有的'&'符号，进行了转码，这里再转回去
    lines = get_lines(android_path)
    new_lines = []
    for l in lines:
        ll = l
        if l.find('&amp;') > 0:
            ll = l.replace('&amp;', '&')
        if ll.find('&lt;') > 0 or ll.find('&gt;') > 0:
            ll = ll.replace('&lt;', '<')
            ll = ll.replace('&gt;', '>')
            ll = ll.replace('&quot;', '"')
        
        new_lines.append(ll)

    f = open(android_path, 'w')
    f.writelines(new_lines)
    f.close()
                
def convert_csv_to_android_ordered_xml(csv_path, android_path, lang, ordered_dic, source_android_path):

    impl = xml.dom.minidom.getDOMImplementation()
    dom = impl.createDocument(None, "resources", None)
    root = dom.documentElement

    ret_list = read_csv(csv_path)
    for dic in ret_list:
        k = dic[ANDROID_KEY]
        v = dic[lang]
        ordered_dic[k] = v
    for k, v in ordered_dic.items():
        if k and len(k) > 0 and v and len(v) > 0:
            if k.startswith("string|"):
                if not v.startswith("Data|"):
                    addElementForParent(dom, root, k.split("|", 1)[1], v, Node.ELEMENT_NODE)
                else:
                    addElementForParent(dom, root, k.split("|", 1)[1], v.split("|", 1)[1], Node.CDATA_SECTION_NODE)
            elif k.startswith("plurals|"):
                klist = k.split("|")
                key = klist[1]
                plist = root.getElementsByTagName("plurals")
                find = False
                for plu in plist:
                    pkey = plu.getAttribute("name")
                    if pkey == key:
                        find = True
                        item = dom.createElement('item')
                        item.setAttribute('quantity', klist[2])
                        text=dom.createTextNode(v)
                        item.appendChild(text)
                        plu.appendChild(item)
                if not find:
                    plu = dom.createElement('plurals')
                    plu.setAttribute('name', key)
                    item = dom.createElement('item')
                    item.setAttribute('quantity', klist[2])
                    text=dom.createTextNode(v)
                    item.appendChild(text)
                    plu.appendChild(item)
                    root.appendChild(plu)
            elif k.startswith("string-array|"):
                klist = k.split("|")
                key = klist[1]
                alist = root.getElementsByTagName("string-array")
                find = False
                for arr in alist:
                    akey = arr.getAttribute("name")
                    if akey == key:
                        find = True
                        item = dom.createElement('item')
                        text=dom.createTextNode(v)
                        item.appendChild(text)
                        arr.appendChild(item) 
                if not find:
                    arr = dom.createElement("string-array")
                    arr.setAttribute("name", key)
                    item = dom.createElement('item')
                    text=dom.createTextNode(v)
                    item.appendChild(text)
                    arr.appendChild(item)  
                    root.appendChild(arr)
            elif k.startswith("array|"):
                klist = k.split("|")
                key = klist[1]
                alist = root.getElementsByTagName("array")
                find = False
                for arr in alist:
                    akey = arr.getAttribute("name")
                    if akey == key:
                        find = True
                        item = dom.createElement('item')
                        text=dom.createTextNode(v)
                        item.appendChild(text)
                        arr.appendChild(item) 
                if not find:
                    arr = dom.createElement("array")
                    arr.setAttribute("name", key)
                    item = dom.createElement('item')
                    text=dom.createTextNode(v)
                    item.appendChild(text)
                    arr.appendChild(item)  
                    root.appendChild(arr)
    
    f = open(android_path, "w")
    dom.writexml(f,addindent="\t",newl="\n", encoding="utf-8")
    f.close()

    # 需要进行一次转码，因为写入的时候，xml将所有的'&'符号，进行了转码，这里再转回去
    lines = get_lines(android_path)
    new_lines = []
    for l in lines:
        ll = l
        if l.find('&amp;') > 0:
            ll = l.replace('&amp;', '&')
        if ll.find('&lt;') > 0 or ll.find('&gt;') > 0:
            ll = ll.replace('&lt;', '<')
            ll = ll.replace('&gt;', '>')
            ll = ll.replace('&quot;', '"')
        
        new_lines.append(ll)

    f = open(android_path, 'w')
    f.writelines(new_lines)
    f.close() 

def convert_csv_to_xls(csv_path, xls_path):
    import pandas as pd
    csv = pd.read_csv(csv_path, encoding='utf-8')
    csv.to_excel(xls_path, sheet_name="data")

def convert_xls_to_csv(xls_path, csv_path):
    import pandas as pd
    data_xls = pd.read_excel(xls_path)
    data_xls.to_csv(csv_path, encoding='utf-8')

def check_two_ios_localization_file(ios_path, ios_second_path, ret_path):
    ori_dic = read_ios_localization(ios_path)
    cn_dic = read_ios_localization(ios_second_path)
    ret = []
    for k, v in ori_dic.items():
        if not k in cn_dic.keys():
            line = '"' + k + '" = "' + v + '";\n'
            ret.append(line) 

    f = open(ret_path, 'w')
    f.writelines(ret)
    f.close() 

def recursion_opt_list(ll, index, func):
    for i in range(index, len(ll)):
        if index >= len(ll):
            return
        dic = ll[i]
        if len(dic[EN_VALUE]) == 0:
            func(ll, i)
            break

def delete_invalid_dic(ll, index):
    print ll[index]
    v = raw_input('do you want to delete the dic ? [y/n]')
    if v == "y":
        ll.pop(index)
        recursion_opt_list(ll, index, delete_invalid_dic)
    else:
        recursion_opt_list(ll, index+1, delete_invalid_dic) 
                

if __name__ == "__main__":

    optParser = OptionParser()
    optParser.add_option('-t', '--type', type='int', dest='action_type', help='你要采取的动作，默认是update更新csv；如果需要解析，传2，eg: python convert_localization_csv.py -t 2'.decode('utf-8'))
    optParser.add_option('-u', '--update_type', type='string', dest='update_type', help='你要更新的类型，传ios/android，默认是all，eg: python convert_localization_csv.py -t 1 -u ios'.decode('utf-8'))
    (options, args) = optParser.parse_args()
    # 将 Values instance 转换为 dic
    options = vars(options)

    action_type = 1
    if options['action_type']:
        action_type = int(options['action_type'])
        if action_type != 2 and action_type != 1:
            print '请输入正确支持的操作类型，1：更新csv；2：解析csv'
            exit(1)

    update_type = "all"
    if options['update_type']:
        update_type = options['update_type']

# /Users/Shared/Jenkins/ClientPublic/pokio_multi_lang
    # 配置你的路径，最好是相对路径，也可以拷贝到当前脚本目录下
    ios_path = '../client_ios2/Pokio/en.lproj/Localizable.strings'    
    # ios_path = "none"
    android_path = 'strings_en.xml'
    # android_path = "none"
    csv_path = 'result.csv'

    # update_type = "ios"
    # ret = mix_ios_android_dic({"a":"abc", "b":"abc", "c":"abc"},{"m":"abc"})
    # read_android_special_localization(android_path)

    # ios_cn_path = '../client_ios2/Pokio/zh-Hant.lproj/Localizable.strings'   
    # check_two_ios_localization_file(ios_path, ios_cn_path, 'new_increase_data.strings')
    # ios_path = 'new_increase_data.strings'
    # read_ios_localization(ios_path)
    # convert_csv_to_xls(csv_path, 'text.xlsx')
    # convert_xls_to_csv('text.xlsx', csv_path)

    # tmpList = read_csv(csv_path)
    # recursion_opt_list(tmpList, 0, delete_invalid_dic)
    # write_to_csv(csv_path, tmpList)
    # ios_path = 'Localizable_en.strings'
    # exit(1)

    if action_type == 1:
        if not os.path.exists(csv_path):
            create_first_csv(csv_path, ios_path, android_path)
        else:
            # if update_type == "ios":
            #     android_path = "none"
            # if update_type == "android":
            #     ios_path = "none"
            # update_csv(csv_path, ios_path, android_path) 
            l = [EN_VALUE, CN_VALUE]
            for lang in l:
                ios_path = '../input/' + 'localization_ios_' + lang + '.strings'
                android_path = '../input/' + 'android_string_' + lang + '.xml' 
                if update_type == "ios":
                    android_path = "none"
                if update_type == "android":
                    ios_path = "none" 
                print update_type
                update_csv_other_lang(csv_path, lang, ios_path, android_path)

    elif action_type == 2:
        l = [EN_VALUE, CN_VALUE]
        ordered_dic = read_android_localization(android_path)
        for lang in l:
            convert_csv_to_android_ordered_xml(csv_path, 'android_string_' + lang + '.xml', lang, copy.deepcopy(ordered_dic), android_path)
            # convert_csv_to_ios_localization(csv_path, 'localization_ios_' + lang + '.strings', lang)
            convert_csv_to_ios_ordered_localization(csv_path, 'localization_ios_' + lang + '.strings', lang, ios_path)
            # convert_csv_to_android_xml(csv_path, 'android_string_' + lang + '.xml', lang)

    # 不对外开放，更新其他语言翻译，需要确认你的文件是否正确
    elif action_type == 3:
        android_path = 'strings_cn.xml'
        # android_path = 'none'
        ios_path = 'Localizable_cn.strings'
        # ios_path = 'none'
        update_csv_other_lang(csv_path, CN_VALUE, ios_path, android_path)

