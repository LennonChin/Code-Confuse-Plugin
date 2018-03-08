#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import re
import uuid
import sys
import getopt
from datetime import datetime


class ConfuseBiz(object):
    # save configs
    @staticmethod
    def save_configs(configs):
        ConfuseBiz.configs = configs

    # 扫描某个目录，返回以特定后缀结尾的所有文件
    @staticmethod
    def scan_path(input_dirs, exclusive_dirs, suffixs):
        filelist = []
        for input_dir in input_dirs:
            log_info("Start scanning system direction {0}".format(input_dir), 0, True)
            if not os.path.isdir(input_dir):
                exit(-1)
            for filename in os.listdir(input_dir):
                if os.path.isdir(os.path.join(input_dir, filename)):
                    if exclusive_dirs:
                        for exclusive_dir in exclusive_dirs:
                            if os.path.join(input_dir, filename) == os.path.realpath(exclusive_dir):
                                log_info('Skipping system direction {0}'.format(os.path.join(input_dir, filename)), 2,
                                         True)
                                continue
                            else:
                                filelist.extend(
                                    ConfuseBiz.scan_path([os.path.join(input_dir, filename)], exclusive_dirs, suffixs))
                    else:
                        filelist.extend(
                            ConfuseBiz.scan_path([os.path.join(input_dir, filename)], exclusive_dirs, suffixs))
                else:
                    if suffixs:
                        re_str = '.*\.[' + ''.join(suffixs) + ']$'
                    pattern_suffix = re.compile(r'' + re_str)
                    matches = re.match(pattern_suffix, filename)
                    if matches:
                        filelist.append((input_dir, filename))
        return filelist

    @staticmethod
    def pre_format_file(file_path):
        if os.path.exists(file_path) and os.path.isfile(file_path):
            file = open(file_path, 'r', encoding='utf-8', errors='ignore')
            try:
                file_content = file.read()
            except Exception as e:
                try:
                    file = open(file_path, 'r', encoding='ascii', errors='ignore')
                    file_content = file.read()
                except Exception as e:
                    try:
                        file = open(file_path, 'r', encoding='ISO-8859-1', errors='ignore')
                        file_content = file.read()
                    except Exception as e:
                        try:
                            file = open(file_path, 'r', encoding='gbk', errors='ignore')
                            file_content = file.read()
                        except Exception as e:
                            try:
                                file = open(file_path, 'r', encoding='Windows-1252', errors='ignore')
                                file_content = file.read()
                            except Exception as e:
                                log_file('no compatible encoding with ascii, utf-8, ISO-8859-1, gbk and Windows-1252, please have a self-check. {0}'.e, 3, True)
                            finally:
                                file.close()
                        finally:
                            file.close()
                    finally:
                        file.close()
                finally:
                    file.close()
            finally:
                file.close()

            # 去除注释
            file_content = ConfuseBiz.filter_useless_chars(file_content)

            # 去除空白行
            cleaned_lines = ConfuseBiz.clean_blank_lines(file_content)
            return cleaned_lines
        else:
            return []

    @staticmethod
    def clean_blank_lines(file_content):
        lines = file_content.split('\n')
        cleaned_lines = []
        for line in lines:
            if len(line.strip()) != 0:
                cleaned_lines.append(line)

        return cleaned_lines

    # 过滤无用字符
    @staticmethod
    def filter_useless_chars(file_content):
        # 移除单行注释和多行注释
        def _remove_comments(string):
            pattern = r"(\".*?\"|\'.*?\')|(/\*.*?\*/|//[^\r\n]*$)"
            regex = re.compile(pattern, re.MULTILINE | re.DOTALL)

            def _replacer(match):
                if match.group(2) is not None:
                    return ""
                else:
                    return match.group(1)

            return regex.sub(_replacer, string)

        file_str = _remove_comments(file_content)
        return file_str

    # 生成唯一的字符串
    @staticmethod
    def confuse_text(text):
        seeds = 'abcdefghijklmnopqrst'
        uid = str(uuid.uuid3(uuid.NAMESPACE_DNS, text))
        uid = "".join(uid.split('-'))
        result = ""
        for c in uid:
            try:
                num = int(c)
                result += seeds[num]
            except Exception as e:
                result += c
        return result.upper()

    # 生成混淆文件
    @staticmethod
    def create_confuse_file(output_file, confused_dict):
        log_info("Start creating confuse file, file fullpath is {0}".format(os.path.realpath(output_file)), 2, True)
        f = open(output_file, 'wb')
        f.write(bytes('#define NEED_CONFUSE 1\n', encoding='utf-8'))
        f.write(bytes('#if NEED_CONFUSE\n', encoding='utf-8'))
        f.write(bytes('// create time at {0}\n'.format(datetime.now()), encoding='utf-8'))
        for (key, value) in confused_dict.items():
            f.write(bytes('#define {0} {1}\n'.format(key, value), encoding='utf-8'))
        f.write(bytes('#endif', encoding='utf-8'))
        f.close()
        log_info("Complete create confuse file", 2, True)


class DealUserFile(object):
    def __init__(self, input_dirs, exclusive_dirs):
        self.input_dirs = input_dirs
        self.exclusive_dirs = exclusive_dirs

    # 挑选需要关键字
    def parse_user_identifiers(self):
        user_file_paths = ConfuseBiz.scan_path(self.input_dirs, self.exclusive_dirs, ['h', 'm'])

        user_identifiers = []
        for file_path, filename in user_file_paths:
            identifier_array = self.__parse_user_file_content(file_path, filename)
            if len(identifier_array):
                user_identifiers += identifier_array

        # 对字典去重
        return sorted(list(set(user_identifiers)))

    # 挑选用户文件中的关键字
    def __parse_user_file_content(self, file_path, filename):
        file_local = os.path.join(file_path, filename)
        file_lines = ConfuseBiz.pre_format_file(file_local)
        # 读取文件行
        identifier_array = []
        # 一行一行的读取文件
        log_info("Start extracting confusing identifiers {0} ".format(file_local), 0, True)
        for line in file_lines:
            # 去除后面的注释
            search_comment_index = line.find('//')
            if search_comment_index != -1:
                line = line[:search_comment_index - 1]
            # 单行注释、宏定义内容不用管
            if line.startswith('#'):
                continue
            # xib连线不用管
            if 'IBAction' in line:
                continue
            # init开头的方法不用管
            if 'init' in line:
                continue
            # 方法名
            if '+' in line or '-' in line:
                # 判断参数个数
                parameter_pattern = re.compile(r'.*?(\(.*?\)).*?')
                if len(re.findall(parameter_pattern, line)) <= 1:
                    pattern_search = re.compile(r'[)\s+](\w+):?.*?')
                else:
                    pattern_search = re.compile(r'[)\s+](\w+):.*?')
                matches = re.findall(pattern_search, line)
                if matches:
                    for match in matches:
                        # set、get、_开头的方法不用管
                        if re.match(r'^set|^get|^_', match):
                            continue
                        # 去除中文
                        zh_pattern = re.compile(u'[\u4e00-\u9fa5]+')
                        if zh_pattern.search(match):
                            continue
                        # 去除纯数字
                        if match.isdigit():
                            continue
                        identifier_array.append(match)
        return identifier_array


class DealSystemIdentifiers(object):
    """
    整理系统关键字
    """

    def __init__(self, system_file_dirs):
        self.system_file_dirs = system_file_dirs

    def parse_system_identifiers(self):
        system_file_paths = ConfuseBiz.scan_path(self.system_file_dirs, None, ['h'])
        system_identifiers = []
        for file_path, filename in system_file_paths:
            identifier_array = self.__parse_system_file_content(file_path, filename)
            if len(identifier_array):
                system_identifiers += identifier_array

        # 对字典去重并排序
        return sorted(list(set(system_identifiers)))

    # 挑选系统文件中的关键字
    def __parse_system_file_content(self, file_path, filename):
        file_local = os.path.join(file_path, filename)
        file_lines = ConfuseBiz.pre_format_file(file_local)
        identifier_array = []
        # 读取文件行
        pattern_split = re.compile(r'\W')
        pattern_clean = re.compile(r'[\s+\W*\d+]')
        log_info("Start extracting system identifiers {0} ".format(file_local), 0, True)
        for line in file_lines:
            matches = re.split(pattern_split, line)
            if len(matches):
                # 遍历结果集，去除无用结果
                for res in matches:
                    # 去除None
                    if not res:
                        continue
                    # 去除空白字符，非单词字符，b\，纯数字
                    if not re.match(pattern_clean, str(res)):
                        identifier_array.append(str(res))
        return identifier_array


class DealCleanIdentifers(object):
    """
    整理需要清除的关键字
    """

    def __init__(self, clean_file_dirs):
        self.clean_file_dirs = clean_file_dirs

    def parse_clean_identifiers(self):
        clean_file_paths = ConfuseBiz.scan_path(self.clean_file_dirs, None, ['h', 'm'])
        clean_identifiers = []
        for file_path, filename in clean_file_paths:
            identifier_array = self.__parse_clean_file_content(file_path, filename)
            if len(identifier_array):
                clean_identifiers += identifier_array

        # 对字典去重并排序
        return sorted(list(set(clean_identifiers)))

    # 挑选需要排除的文件中的关键字
    def __parse_clean_file_content(self, file_path, filename):
        file_local = os.path.join(file_path, filename)
        file_lines = ConfuseBiz.pre_format_file(file_local)
        # 读取文件行
        identifier_array = []
        for line in file_lines:
            # @property
            if line.startswith('@property'):
                pattern_search = re.compile(r'[\s+|*](\w*);$')
                matches = re.findall(pattern_search, line)
                if matches:
                    identifier_array += matches
            # 以_开头的变量名
            if '_' in line:
                pattern_search = re.compile(r'.*?_(\w*)[. =\)].*')
                matches = re.findall(pattern_search, line)
                if matches:
                    identifier_array += matches
            # void (^block)(void);
            if '^' in line:
                pattern_search = re.compile(r'\(\^(\w*)\).*')
                matches = re.findall(pattern_search, line)
                if matches:
                    identifier_array += matches
            # 方法名
            if '+' in line or '-' in line:
                # 判断参数个数
                parameter_pattern = re.compile(r'.*?(\(.*?\)).*?')
                if len(re.findall(parameter_pattern, line)) <= 1:
                    # 检测'- (NSInteger)tableView {'
                    pattern_search = re.compile(r'[)\s+](\w+):?.*?')
                else:
                    pattern_search = re.compile(r'[)\s+](\w+):.*?')
                matches = re.findall(pattern_search, line)
                if matches:
                    for match in matches:
                        # set、get、_开头的方法不用管
                        if re.match(r'^set|^get|^_', match):
                            continue
                        # 去除中文
                        zh_pattern = re.compile(u'[\u4e00-\u9fa5]+')
                        if zh_pattern.search(match):
                            continue
                        # 去除纯数字
                        if match.isdigit():
                            continue
                        identifier_array.append(match)
        return identifier_array


# 打印方法
log_file = None


def log_info(info, level=1, to_log_file=False):
    """
    打印到控制台
    0 不打印
    1 info
    2 warning
    3 error
    """
    print_infos = info
    if level == 1:
        print(print_infos)
    elif level == 2:
        print('\033[0;32m{0}\033[0m'.format(print_infos))
    elif level == 3:
        print('\033[0;31m╔═════════════════════════════════ ERROR ═════════════════════════════════╗\033[0m')
        print('\033[0;31m║\033[0m')
        print('\033[0;31m║ {0}\033[0m'.format(print_infos))
        print('\033[0;31m║\033[0m')
        print('\033[0;31m╚═════════════════════════════════════════════════════════════════════════╝\033[0m')
    if to_log_file:
        # 写入文件
        log_file.write('{0}\n'.format(print_infos))


def usage():
    help_info = """
-i\t必须，项目需要处理的主要文件所在的目录
-s\t可选，配置系统Framework文件的目录，一般用于做排除字典，避免替换系统关键字
-e\t可选，用于存放不扫描处理的文件的目录，比如Swift文件目录
-c\t可选，用于存放排除关键字的文件的目录，例如Pods下的目录，或者静态库（头文件修改后会出错）
-o\t必须，输出文件的目录，用于输出关键字、日志以及最后生成的混淆头文件的目录

Example:

python3 Confuse.py \
-i /Users/LennonChin/Desktop/Code-Confuse-Plugin/Demo/Confuse_Demo/Confuse_Demo/ \
-s /Users/LennonChin/Desktop/Code-Confuse-Plugin/Demo/System_Frameworks_iOS11 \
-e /Users/LennonChin/Desktop/Code-Confuse-Plugin/Demo/Confuse_Demo/Confuse_Demo/Swift/ \
-c /Users/LennonChin/Desktop/Code-Confuse-Plugin/Demo/Confuse_Demo/Confuse_Demo/OtherSDK \
-o /Users/LennonChin/Desktop/Code-Confuse-Plugin/Demo/
"""
    print(help_info)


if __name__ == '__main__':

    # 获取参数
    options, args = getopt.getopt(sys.argv[1:], "hi:s:e:c:o:")
    input_dirs = None  # 项目需要处理的主要文件所在的目录
    system_dirs = None  # 配置系统Framework文件的目录，一般用于做排除字典，避免替换系统关键字
    exclusive_dirs = None  # 用于存放不扫描处理的文件的目录，比如Swift文件目录
    clean_dirs = None  # 用于存放排除关键字的文件的目录，例如Pods下的目录，或者静态库（头文件修改后会出错）
    output_dir = None  # 输出文件的目录，用于输出关键字、日志以及最后生成的混淆头文件的目录

    for option, value in options:
        if option == "-i":
            input_dirs = value.split(',')
        elif option == "-s":
            system_dirs = value.split(',')
        elif option == "-e":
            exclusive_dirs = value.split(',')
        elif option == "-c":
            clean_dirs = value.split(',')
        elif option == "-o":
            output_dir = value
        elif option == "-h":
            usage()
            sys.exit()

    # 判断参数是否正确
    if not input_dirs:
        log_info("Reason: Exit in reason 请输入需要处理文件的目录。可使用-h参数查看帮助", 3, False)
        sys.exit()
    if not output_dir:
        log_info('Reason: Exit in reason 请输入输出文件的目录。可使用-h参数查看帮助', 3, False)
        sys.exit()

    # 保存配置信息
    configs = {
        'input_dirs': input_dirs,
        'system_dirs': system_dirs,
        'exclusive_dirs': exclusive_dirs,
        'clean_dirs': clean_dirs,
        'output_dir': output_dir
    }
    ConfuseBiz.save_configs(configs)

    # 初始化日志打印文件
    log_file = open(os.path.join(output_dir, 'confuse_log.log'), 'w')

    # 获取系统文件关键字并写入文件
    log_info("Start scanning System identifiers...", 2, True)
    system_identifiers = DealSystemIdentifiers(system_dirs).parse_system_identifiers()
    log_info("Complete scan System identifiers...", 2, True)

    log_info("Start writing System identifiers into Dict File, File fullpath is {0}".format(
        os.path.join(output_dir, 'system_identifiers.data')), 1, True)
    system_identifiers_record_file = open(os.path.join(output_dir, 'system_identifiers.data'), 'wb')
    for item in system_identifiers:
        system_identifiers_record_file.write(bytes(item, encoding='utf-8'))
        system_identifiers_record_file.write(bytes('\n', encoding='utf-8'))
    # 关闭文件读写
    system_identifiers_record_file.close()
    log_info("Complete write System identifiers into Dict File", 1, True)

    # 遍历排除关键字的文件目录，提取关键字，并写入文件
    log_info("Start scanning assign Clean identifiers...", 2, True)
    clean_identifiers = DealCleanIdentifers(clean_dirs).parse_clean_identifiers()
    log_info("Start writing Clean identifiers into Dict File, File fullpath is {0}".format(
        os.path.join(output_dir, 'clean_identifiers.data')), 1, True)
    clean_identifiers_record_file = open(os.path.join(output_dir, 'clean_identifiers.data'), 'wb')
    for item in clean_identifiers:
        clean_identifiers_record_file.write(bytes(item, encoding='utf-8'))
        clean_identifiers_record_file.write(bytes('\n', encoding='utf-8'))
    # 关闭文件读写
    clean_identifiers_record_file.close()
    log_info("Complete write Clean identifiers into Dict File", 1, True)

    # 遍历用户指定目录，提取关键字，主要提取方法名
    log_info("Start scanning assign need deal files' identifiers...", 2, True)
    user_identifiers = DealUserFile(input_dirs, exclusive_dirs).parse_user_identifiers()

    # 将系统关键字去除
    log_info("Start excluding system identifiers...", 2, True)
    system_intersect_identifiers = list(set(system_identifiers).intersection(set(user_identifiers)))
    diff_identifiers = list(set(user_identifiers).difference(set(system_intersect_identifiers)))
    # 将排除目录的关键字去除
    log_info("Start excluding clean identifiers...", 2, True)
    clean_intersect_identifiers = list(set(clean_identifiers).intersection(set(user_identifiers)))
    diff_identifiers = list(set(diff_identifiers).difference(set(clean_intersect_identifiers)))
    # 重新去重排序
    diff_identifiers = sorted(list(set(diff_identifiers)))

    # 写入文件
    log_info("Start writing need deal files' identifiers into Dict File, File fullpath is {0}".format(
        os.path.join(output_dir, 'user_identifiers.data')), 2, True)
    user_identifiers_file = open(os.path.join(output_dir, 'user_identifiers.data'), 'wb')
    for item in diff_identifiers:
        user_identifiers_file.write(bytes(item, encoding='utf-8'))
        user_identifiers_file.write(bytes('\n', encoding='utf-8'))
    user_identifiers_file.close()
    log_info("Complete write need deal files' identifiers into Dict File", 1, True)

    # 生成混淆文件
    confused_dict = {}
    for item in diff_identifiers:
        confused_dict[item] = ConfuseBiz.confuse_text(item)
    ConfuseBiz.create_confuse_file(os.path.join(output_dir, 'Confuse.h'), confused_dict)
    log_info("You can browse run logs in file {0}".format(os.path.join(output_dir, 'confuse_log.log')), 1, True)
    log_file.close()
