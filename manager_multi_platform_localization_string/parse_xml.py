# -*- coding: UTF-8 -*-

import xml.sax
from xml.etree import ElementTree

from xml.dom.minidom import parse
import xml.dom.minidom
from xml.dom.minidom import Node

import re
from optparse import OptionParser

import os

# import sys
# reload(sys) 
# sys.setdefaultencoding('utf-8') 

UNIVERSL_TYPE_TAG = 'universal type strings for different platform'
IOS ='ios'
ANDROID = 'android'

def writeToFile(filepath, ret, tle='a+'):
    f = open(filepath, tle)
    # print ret
    f.write(ret)
    f.close()

def get_lines(filePath):
    f = open(filePath)
    lines = f.readlines()
    f.close()
    return lines

# ios: xml -> strings; strings -> xml
def addElementForParent(dom, parent, name, value, nodeType):
    if nodeType == Node.ELEMENT_NODE:
        item = dom.createElement('string')
        item.setAttribute('name', name.lstrip().rstrip().strip('"'))
        text=dom.createTextNode(value.lstrip().rstrip()[:-2].lstrip('"'))
        item.appendChild(text)
        parent.appendChild(item)
        # print name + ' => ' + value
        # parent.appendChild(dom.createTextNode('\n')) 
    elif nodeType == Node.COMMENT_NODE:
        item = dom.createComment(value)
        parent.appendChild(item)
        # parent.appendChild(dom.createTextNode('\n')) 

def convert_ios_localization_str_to_xml(filepath, sourcepath):
    dom = createIOSXML(filepath)
    f = open(sourcepath, 'w')
    dom.writexml(f,addindent="\t",newl="\n", encoding="utf-8")
    f.close()

def convert_xml_to_ios_localization_str(nodes, sourcepath, tle='a+'):
    for node in nodes:
        if node.nodeType == Node.ELEMENT_NODE:
            if node.tagName == "string":
                if node.hasAttribute("name"):
                    print "title: %s" % node.getAttribute("name")
                    if node.childNodes and len(node.childNodes) > 0:
                        line = '"'+node.getAttribute("name")+'"="'+node.childNodes[0].data+'";\n' 
                        writeToFile(sourcepath, line.encode("utf-8"), tle)
                # print "value: %s" % node.childNodes[0].data
            elif node.tagName == "plurals":
                if node.hasAttribute("name"):
                    name = node.getAttribute("name")
                    for sub in node.getElementsByTagName("item"):
                        if sub.hasAttribute("quantity"):
                            # print "title: %s" % (name + "#" sub.getAttribute("quantity"))
                            line = '"'+name+'#'+sub.getAttribute("quantity")+'"="'+sub.childNodes[0].data+'";\n' 
                            writeToFile(sourcepath, line.encode("utf-8"), tle)
                        # print "value: %s" % sub.childNodes[0].data

        elif node.nodeType == Node.COMMENT_NODE:
            # print "comment: %s" % node.data
            line = '/*' + node.data + '*/\n'
            writeToFile(sourcepath, line.encode("utf-8"), tle) 

def createIOSXML(filepath):
    lines = get_lines(filepath)
    impl = xml.dom.minidom.getDOMImplementation()
    dom = impl.createDocument(None, 'ios_strings', None)
    root = dom.documentElement
    resource = dom.createElement('resources')
    root.setAttribute('filepath', filepath)
    root.appendChild(resource)
    tmp_name = ""
    tmp_value = ""
    for l in lines:
        if re.match(r'^"(.*)"[ ]*=[ ]*"(.*)";$',l):
            l1 = l.split('=')
            addElementForParent(dom, resource, l1[0], l1[1].strip('\n'), Node.ELEMENT_NODE)
            # print l1[1].strip('\n')
            tmp_name = ""
            tmp_value = ""
        elif re.match(r'^"[^"]*"[ ]*=[ ]*"[^"]*";[ ]*//.*$', l):
            l1 = l.split('=')
            l2 = l1[1].split('//')
            addElementForParent(dom, resource, l1[0], l2[0].strip('\n'), Node.ELEMENT_NODE)
            addElementForParent(dom, resource, '', l2[1], Node.COMMENT_NODE)
            tmp_name = ""
            tmp_value = "" 

        # 只是开始，没有结束
        elif re.match(r'"(.*)"[ ]*=[ ]*"([^"]*)',l):
            l1 = l.split('=')
            tmp_name = l1[0]
            tmp_value = l1[1]
        elif re.match(r'^[^=]+";$',l):
            tmp_value = tmp_value + l
            # print tmp_value
            if len(tmp_name) > 0:
                # print tmp_name
                addElementForParent(dom, resource, tmp_name, tmp_value, Node.ELEMENT_NODE)
                tmp_name = ""
                tmp_value = ""
        elif re.match(r'^/\*.*\*/$', l):
            l1 = l[2:-3]
            print l
            addElementForParent(dom, resource, "", l1, Node.COMMENT_NODE)
        elif re.match(r'^/\*.*[^*][^/]$', l):
            tmp_value = l
        elif re.match(r'^[^/][^*].*\*/$', l):
            tmp_value = tmp_value + l
            tmp_value = tmp_value[2:-3]
            print tmp_value
            addElementForParent(dom, resource, "", tmp_value, Node.COMMENT_NODE)
            tmp_value = ""
        elif re.match(r'^[^="]+$',l):
            tmp_value = tmp_value + l
        # print tmp_value

    return dom

def split_ios_xml_to_special_and_universal_part(filepath, universal_type_path=None):
    if not universal_type_path:
        return
    
    impl = xml.dom.minidom.getDOMImplementation()
    dom = impl.createDocument(None, 'ios_strings', None)
    root = dom.documentElement

    universal_type_dom = impl.createDocument(None, 'resources', None)
    univeral_resource = universal_type_dom.documentElement

    print filepath
    DOMTree = xml.dom.minidom.parse(filepath)
    collection = DOMTree.documentElement
    res = collection.getElementsByTagName('resources')[0] 
    lchildren = res.childNodes
    tmp_coll = res.cloneNode(False)
    coll = tmp_coll
    for node in lchildren:
        if node.nodeType == Node.COMMENT_NODE and (node.data).strip() == UNIVERSL_TYPE_TAG:
            print node.data
            coll = univeral_resource
            coll.appendChild(node.cloneNode(True))
        elif node.nodeType == Node.COMMENT_NODE:
            coll.appendChild(node.cloneNode(True))
        elif node.nodeType == Node.ELEMENT_NODE:
            coll.appendChild(node.cloneNode(True))

    root.setAttribute('filepath', collection.getAttribute('filepath'))
    root.appendChild(tmp_coll)
    ret = dom.toprettyxml(newl='',encoding='utf-8')
    writeToFile(filepath, ret, 'w')

    ret = universal_type_dom.toprettyxml(newl='',encoding='utf-8')
    writeToFile(universal_type_path, ret, 'w')
    

def convert_serial_android_xml_to_one_xml(filepaths, sourcepath, universal_type_path=None):
    impl = xml.dom.minidom.getDOMImplementation()
    dom = impl.createDocument(None, 'android_strings', None)
    root = dom.documentElement

    universal_type_dom = impl.createDocument(None, 'universal_strings', None)
    univeral_type_root = universal_type_dom.documentElement
    univeral_resource = universal_type_dom.createElement('resources')
    univeral_type_root.appendChild(univeral_resource)
    for flp in filepaths:
        filedes = dom.createElement('filepath')
        filedes.setAttribute("filepath",flp)
        root.appendChild(filedes)

        DOMTree = xml.dom.minidom.parse(flp)
        collection = DOMTree.documentElement
        tmp_coll = collection.cloneNode(False)
        coll = tmp_coll
        for node in collection.childNodes:
            if node.nodeType == Node.COMMENT_NODE and (node.data).strip() == UNIVERSL_TYPE_TAG:
                coll = univeral_resource
            coll.appendChild(node.cloneNode(True))
        filedes.appendChild(tmp_coll)

    # ret = dom.toprettyxml(newl="",encoding='utf-8')
    ret = dom.toxml(encoding='utf-8')
    writeToFile(sourcepath, ret, 'w')

    if universal_type_path:
        ret = universal_type_dom.toprettyxml(encoding='utf-8')
        writeToFile(universal_type_path, ret, 'w')

def convert_androd_ios_xml_to_final_xml(android_xml_path, ios_xml_path, universal_type_path=None, sourcepath='final_strings.xml'):

    impl = xml.dom.minidom.getDOMImplementation()
    dom = impl.createDocument(None, 'final_strings', None)
    root = dom.documentElement 

    DOMTree = xml.dom.minidom.parse(android_xml_path)
    root1 = DOMTree.documentElement

    iosDom = xml.dom.minidom.parse(ios_xml_path)
    root2 = iosDom.documentElement

    root.appendChild(root1)
    root.appendChild(root2)

    if universal_type_path:
        universal = xml.dom.minidom.parse(universal_type_path)
        universal_dom = dom.createElement('universal_strings')
        universal_dom.appendChild(universal.documentElement)
        root.appendChild(universal_dom)

    # ret = dom.toprettyxml(newl="",encoding='utf-8')
    ret = dom.toxml(encoding ='utf-8')
    writeToFile(sourcepath, ret, 'w') 


def compare_ios_android_universal_xml(android_xml, ios_xml, final_xml=None):
    DOMTree = xml.dom.minidom.parse(android_xml)
    android_res = DOMTree.documentElement

    DOMTree = xml.dom.minidom.parse(ios_xml)
    ios_res = DOMTree.documentElement

    tmp_ch = and_ch = android_res.childNodes
    ios_ch = ios_res.childNodes
    if len(and_ch) < len(ios_ch):
        tmp_ch = ios_ch
    # 如果需要两边每一项都进行比较，可以额外添加每行比较的代码
        return ios_xml
    return android_xml

def combine_ios_android_localization_string_to_final_xml(android_not_universal_xmls, ios_localization_string, android_universal_xml, final_xml_path):
    total_android_xml_path = 'total_android_strings.xml'
    ios_xml_path = 'ios_strings.xml'
    ios_universal_xml_path = 'ios_universal_strings.xml'
    convert_ios_localization_str_to_xml(ios_localization_string, ios_xml_path)
    split_ios_xml_to_special_and_universal_part(ios_xml_path, ios_universal_xml_path)
    convert_serial_android_xml_to_one_xml(android_not_universal_xmls, total_android_xml_path)
    convert_androd_ios_xml_to_final_xml(total_android_xml_path, ios_xml_path, compare_ios_android_universal_xml(android_universal_xml, ios_universal_xml_path), final_xml_path)
    os.remove(total_android_xml_path)
    os.remove(ios_xml_path)
    os.remove(ios_universal_xml_path)

def combine_ios_android_xml_to_final_xml(android_not_universal_xmls, ios_xml_path, android_universal_xml, final_xml_path):
    total_android_xml_path = 'total_android_strings.xml'
    ios_universal_xml_path = 'ios_universal_strings.xml'
    split_ios_xml_to_special_and_universal_part(ios_xml_path, ios_universal_xml_path)
    convert_serial_android_xml_to_one_xml(android_not_universal_xmls, total_android_xml_path)
    convert_androd_ios_xml_to_final_xml(total_android_xml_path, ios_xml_path, compare_ios_android_universal_xml(android_universal_xml, ios_universal_xml_path), final_xml_path)
    os.remove(total_android_xml_path)
    os.remove(ios_universal_xml_path)
    os.remove(ios_xml_path)

def parse_ios_android_combined_xml(filepath, source_type=None):
    DOMTree = xml.dom.minidom.parse(filepath)
    root = DOMTree.documentElement 
    android_strings = None
    if root.getElementsByTagName('android_strings'): 
        android_strings = root.getElementsByTagName('android_strings')[0]
    ios_strings = None
    if root.getElementsByTagName('ios_strings'):
        ios_strings = root.getElementsByTagName('ios_strings')[0]
    universal_strings = None
    if root.getElementsByTagName('universal_strings'):
        universal_strings = root.getElementsByTagName('universal_strings')[0]

    # parse android
    android_file_path = ''
    if (not source_type) or (source_type.lower() == ANDROID):
        files = android_strings.getElementsByTagName('filepath')
        for fln in files:
            if fln.hasAttribute("filepath"): 
                fpath = fln.getAttribute("filepath") 
                res = fln.getElementsByTagName('resources')[0]
                # ret = res.toprettyxml(newl='',encoding='utf-8')
                ret = res.toxml(encoding='utf-8')
                writeToFile(fpath, ret, 'w')  
                print '解析android文件最终生成文件目录：' + fpath
                android_file_path = fpath

    # parse ios
    if (not source_type) or (source_type.lower() == IOS):
        ios_localization_string_path = ios_strings.getAttribute('filepath')
        writeToFile(ios_localization_string_path, '', 'w') 
        res = ios_strings.getElementsByTagName('resources')[0]
        convert_xml_to_ios_localization_str(res.childNodes, ios_localization_string_path)

    if not universal_strings:
        return

    res = universal_strings.getElementsByTagName('resources')[0]
    ret = res.toprettyxml(newl='',encoding='utf-8')

    # parse universal android
    if (not source_type) or (source_type.lower() == ANDROID): 
        if android_file_path.rfind('/') > 0:
            android_file_path = android_file_path[0:android_file_path.rfind('/') + 1] + 'universal_android.xml'
        else:
            android_file_path = 'universal_android.xml'
        writeToFile(android_file_path, ret, 'w')   
        print '解析android文件最终生成文件目录：' + android_file_path

    # parse universal ios
    if (not source_type) or (source_type.lower() == IOS):
        convert_xml_to_ios_localization_str(res.childNodes, ios_localization_string_path)
        print '解析ios文件最终生成文件目录：' + ios_localization_string_path

def update_final_xml_with_updated_android_xml(android_not_universal_xmls, android_universal_xml, final_xml_path):
    if not final_xml_path:
        return
    root = None
    if os.path.exists(final_xml_path):
        DOMTree = xml.dom.minidom.parse(final_xml_path)
        root = DOMTree.documentElement
    else:
        impl = xml.dom.minidom.getDOMImplementation()
        dom = impl.createDocument(None, 'final_strings', None)
        root = dom.documentElement 
    
    total_android_xml_path = 'total_android_strings.xml'
    if android_not_universal_xmls:
        convert_serial_android_xml_to_one_xml(android_not_universal_xmls, total_android_xml_path) 
        android_nodes = root.getElementsByTagName('android_strings')
        if android_nodes:
            root.removeChild(android_nodes[0]) 

        DOMTree = xml.dom.minidom.parse(total_android_xml_path)
        root1 = DOMTree.documentElement
        ios_node = root.getElementsByTagName('ios_strings')[0]
        root.insertBefore(root1, ios_node)

    if android_universal_xml:
        universal = xml.dom.minidom.parse(android_universal_xml)
        root2 = universal.documentElement

        universal_nodes = root.getElementsByTagName('universal_strings')
        if universal_nodes:
            root.removeChild(universal_nodes[0])
        root.appendChild(root2)

    ret = root.toxml(encoding ='utf-8')
    writeToFile(final_xml_path, ret, 'w') 
        
def update_final_xml_with_updated_ios_localization_strings(ios_localization_string, final_xml_path):
    if (not final_xml_path) or (not ios_localization_string):
        return

    root = None
    if os.path.exists(final_xml_path):
        DOMTree = xml.dom.minidom.parse(final_xml_path)
        root = DOMTree.documentElement
    else:
        impl = xml.dom.minidom.getDOMImplementation()
        dom = impl.createDocument(None, 'final_strings', None)
        root = dom.documentElement 

    ios_xml_path = 'ios_strings.xml'
    ios_universal_xml_path = 'ios_universal_strings.xml'
    convert_ios_localization_str_to_xml(ios_localization_string, ios_xml_path)
    split_ios_xml_to_special_and_universal_part(ios_xml_path, ios_universal_xml_path)

    ios_nodes = root.getElementsByTagName('ios_strings')
    if ios_nodes:
        root.removeChild(ios_nodes[0])

    universal_nodes = root.getElementsByTagName('universal_strings')
    if universal_nodes:
        root.removeChild(universal_nodes[0])

    iosDom = xml.dom.minidom.parse(ios_xml_path)
    root1 = iosDom.documentElement

    universal = xml.dom.minidom.parse(ios_universal_xml_path)
    root2 = universal.documentElement

    root.appendChild(root1)
    root.appendChild(root2) 
    ret = root.toxml(encoding ='utf-8')
    writeToFile(final_xml_path, ret, 'w') 

    os.remove(ios_xml_path)
    os.remove(ios_universal_xml_path)



if __name__ == "__main__":
    # writeToFile("",'w')

    optParser = OptionParser()
    optParser.add_option('-t', '--type', type='int', dest='action_type', help='你要采取的动作，\t\t1 -> 合并ios和android的本地化文件，需要传入的参数有android本地化文件，ios本地化文件，通用本地化文件，\teg: python parse_xml.py -t 1 -a strings.xml,toast_string.xml -i localization.strings -u universal.xml -o final_strings.xml; \t\t2 -> 解析合并后的xml文件，最终生成对应的android本地化文件，ios本地化文件，eg: py parse_xml.py -t 2 final_strings.xml;'.decode('utf-8') )
    optParser.add_option('-a', '--android', type='string', dest='an_un_xmls', help='android_not_universal_xmls,不包含universal.xml的其他xml文件路径 eg:strings.xml,toast_string.xml'.decode('utf-8'))
    optParser.add_option('-i', '--ios', type='string', dest='ios_path', help='ios 本地文件路径地址，eg: localization.strings'.decode('utf-8'))
    optParser.add_option('-u', '--universal', type='string', dest='universal_xml', help='android端，适配多平台通用的xml文件地址，eg: universal.xml'.decode('utf-8'))
    optParser.add_option('-o', '--output', type='string', dest='output', default='final_strings.xml', help='最终生成的xml文件地址存放路径，不设置的话，默认会存储在脚本所在目录，文件名为final_strings.xml eg:final_strings.xml'.decode('utf-8'))
    optParser.add_option('-s', '--source', type='string', dest='source_type', help='指定你要操作的一端(ios/android)，如果不指定，两端都会执行'.decode('utf-8'))

    (options, args) = optParser.parse_args()
    # 将 Values instance 转换为 dic
    options = vars(options)
    stop = False

    action_type = 2
    if options['action_type']:
        action_type = int(options['action_type'])
        if action_type != 1 and action_type != 2:
            print '请输入正确支持的操作类型，1；合成最终的xml文件。2；解析最终生成的xml文件。详细信息请输入 py parse_xml.py -h'
            exit(1)

    if action_type == 2:
        if args and args[0]:
            source_type = options['source_type']
            parse_ios_android_combined_xml(args[0], source_type)
            print '解析完成 congratulation !!!!!!'
            exit(0)
        else:
            print 'xml文件错误，如需解析，eg：py parse_xml.py final_strings.xml; 如需合并xml文件，请输入 py parse_xml.py -h 获取更多信息'
            exit(1)

    android_not_universal_xmls=[]
    if options['an_un_xmls']:
        android_not_universal_xmls = options['an_un_xmls'].split(',')
    else:
        stop = True
        
    ios_localization_string=''
    if options['ios_path']:
        ios_localization_string = options['ios_path']
    else:
        stop = True

    android_universal_xml=''
    if options['universal_xml']:
        android_universal_xml = options['universal_xml']
    else:
        stop = True

    final_xml_path='final_strings.xml' 
    if options['output']:
        finalpath = options['output']
        if finalpath.endswith('.xml'):
            final_xml_path = finalpath
        else:
            if finalpath.endswith('/'):
                final_xml_path = finalpath + 'final_strings.xml'
            else:
                final_xml_path = finalpath + '/final_strings.xml' 

    # 更新操作
    source_type = options['source_type'] 
    if source_type:
        if source_type.lower() == ANDROID and len(android_not_universal_xmls) > 0 and len(android_universal_xml) > 0:
            update_final_xml_with_updated_android_xml(android_not_universal_xmls, android_universal_xml, final_xml_path)
            print '更新android端的xml文件成功 !!!!!!'
            exit(0)
        elif source_type.lower() == IOS and len(ios_localization_string) > 0:
            update_final_xml_with_updated_ios_localization_strings(ios_localization_string, final_xml_path)
            print '更新ios端的strings文件成功 !!!!!!'
            exit(0)
            
    if stop:
        print 'please input the android/ios/universal file path, for more infomation please input "py parse_xml.py -h"'
        exit(1)

    combine_ios_android_localization_string_to_final_xml(android_not_universal_xmls,ios_localization_string,android_universal_xml,final_xml_path) 
    
    # python parse_xml.py -t 1 -a ./test_xml/strings.xml,./test_xml/toast_string.xml -i ./test_xml/localization.strings -u ./test_xml/universal_android.xml -o ./test_xml
