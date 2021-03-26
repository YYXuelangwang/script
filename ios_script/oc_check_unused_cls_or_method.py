#coding: utf8

import sys
import io
import os
import json
import re

class OCCheck:
    def __init__(self, projectfileName, projectpath):
        self.projectpath = projectpath
        self.ignore_dirs = ["Pods"]
        self.projectfileName = projectfileName
        self.clss = self.get_clss_from_dir(projectpath)

    def get_lines(self, filePath):
        f = open(filePath)
        lines = f.readlines()
        f.close()
        return lines
    
    def get_clss_from_dir(self, dirpath):
        with os.popen("find " + dirpath + " -name '*.h' | xargs grep '@interface.*:'") as p:
            r = p.readlines()
            p.close()
            ret = []
            for line in r:
                if line.find("interface ") > 0:
                    l = line[line.find("interface ") + 9:line.rfind(":")].strip()
                    if l.find("<") > 0:
                        l = l[:l.find("<")].strip()
                    ret.append(l)
            return ret

    def get_instance_method_from_file(self, filepath):
        filename = os.path.basename(filepath)
        lines = self.get_lines(filepath)
        ret = []
        for line in lines:
            if re.match(r'^-[ ]*.*$', line):
                l = line[line.find(")")+1:line.find(":")].strip()
                if len(l) > 0:
                    ret.append(l)
        return filename[:-2], ret
    
    def schedule_cmd(self, _cmd):
        with os.popen(_cmd) as p:
            r = p.readlines()
            p.close()
            return r

    def check_cls_appear_count(self, cl, r):
        count = 0
        hpath = ""
        for line in r:
            if line.find("" + cl + ".m:") > 0:
                continue
            if line.find("//") > 0 or line.startswith("/*") > 0:
                continue
            if line.find("#import ") > 0:
                continue
            if line.find("@interface ") > 0:
                hpath = line.split(":")[0]
                continue
            if line.find("@implementation ") > 0:
                continue
            count = count + 1
            break
        return count, hpath

    def traverse_cls(self):
        ret = []
        for cl in self.clss:
            index = self.clss.index(cl)

            r = self.schedule_cmd('find ' + self.projectpath + ' -type f | xargs grep "' + cl + '"')
            count, hpath = self.check_cls_appear_count(cl, r)
            if count <= 0:
                print "========================================="
                print '' + cl + ' appeared at :'
                print(json.dumps(r, indent=4))
                os.system('cat ' + hpath)
                choise = raw_input('do you want to delete this class: ' + cl + ' ? n/y')
                if choise == 'y':
                    projectfilepath = self.projectpath + '/../' + self.projectfileName + '/project.pbxproj'
                    os.system('sed -i "" "/ ' + cl + '\./d" ' + projectfilepath)
                    os.system('rm ' + hpath)
                    os.system('rm ' + hpath[:-2] + '.m')
                    ret.append(cl)
        return ret

    def traverse_instance_method(self, filename, methods):
        ret = []
        for method in methods:

            r = self.schedule_cmd('find ' + self.projectpath + ' -type f | xargs grep "' + method + '"')
            count = 0
            for line in r:
                if line.find("" + filename + '.h:') > 0:
                    continue
                if line.find("" + filename + '.m:') > 0:
                    continue
                if line.find("" + filename + '.mm:') > 0:
                    continue
                count = count + 1
        
            if count <= 0:
                print "========================================="
                print '' + method + ' appeared at :'
                print(json.dumps(r, indent=4))
                choise = raw_input('do you want to delete this class: ' + method + ' ? [n/y]')
                if choise == 'y':
                    ret.append(method)
        return ret

if __name__ == '__main__':

    # 第一个参数是你的xcodeproj文件名；第二个参数是你工程所在目录
    oc_check = OCCheck("test.xcodeproj","/Users/yinyong/ios/test")
    # 检查项目中没有继续使用的class
    # ret = oc_check.traverse_cls()

    # 检查指定文件中没有继续使用的方法；
    nets = ["UploadError"]
    for n in nets:
        filepath = projectPath + '/request/WBaseNetwork+' + n + '.h'
        filename, methods = oc_check.get_instance_method_from_file(filepath)
        ret = oc_check.traverse_instance_method(filename, methods)
        print(json.dumps(ret, indent=4))
