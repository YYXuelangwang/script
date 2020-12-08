# -*- coding: UTF-8 -*-

import os

# 配置文件路径地址
config={
    'android_not_universal_xmls':'./project/strings.xml,./project/toast_string.xml',
    'android_universal_xml':'',
    'ios_localization_string':'./project/en.lproj/Localizable.strings',
    'final_xml_path':'final_strings.xml',
}

def writeToFile(filepath, ret, tle='a+'):
    f = open(filepath, tle)
    # print ret
    f.write(ret)
    f.close()

if __name__ == "__main__":
    writeToFile('update_final_xml_ios.shell', 'python parse_xml.py -t 1 -i ' + config['ios_localization_string'] + ' -s ios', 'w')
    writeToFile('update_final_xmls_android.bash', 'python parse_xml.py -t 1 -a ' + config['android_not_universal_xmls'] + ' -u ' + config['android_universal_xml'] + ' -s android', 'w')
    writeToFile('parse_ios_strings.shell', 'python parse_xml.py -s ios '+config['final_xml_path'], 'w')
    writeToFile('parse_android_xmls.bash', 'python parse_xml.py -s android '+config['final_xml_path'], 'w')
    os.system('chmod 774 update_final_xml_ios.shell update_final_xmls_android.bash parse_ios_strings.shell parse_android_xmls.bash')
