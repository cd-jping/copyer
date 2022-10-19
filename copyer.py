"""
修改 xml 和 png 中的中文字

拷贝 xml 内容 到目标路径
- 源 xml 内容添加 项目路径
- 生成 png2mxl
    - png2xml xml 内容添加到目标路径
    - 拷贝 png 到 目标路径

"""
import os
import lxml.etree as et
import pypinyin


class FilterFiles:
    # @staticmethod
    # def __init__(self):
    #     self.file_dir = None
    def filter_files(self, file_dir, prefix: list = None, suffix: list = None):
        result = {}
        count = 0
        if file_dir is None:
            p = os.getcwd()
            file_list = os.listdir(p)
        else:
            file_list = os.listdir(file_dir)
            # print(file_list)
        if prefix is None and suffix is None:
            print(" error!  ")
            return
        elif prefix is not None and suffix is not None:
            file_list = self.filter_prefix(prefix, file_list)
            file_list = self.filter_suffix(suffix, file_list)
        elif prefix is not None:
            file_list = self.filter_prefix(prefix, file_list)
        elif suffix is not None:
            file_list = self.filter_suffix(suffix, file_list)

        for file_name in file_list:
            file_path = os.path.join(file_dir, file_name)
            count = count + 1
            # file_name = file_name + "_" + str(count)
            result.update({file_name: file_path})
        print(f"get {count} files")
        return result

    # @staticmethod
    @staticmethod
    def filter_prefix(prefix: list, file_list: list, file_dir=None):
        rs = []
        # if file_dir and file_list is None:
        #     p = os.getcwd()
        #     file_list = os.listdir(p)
        # if file_list and file_dir is not None:
        #     print("file_dir 和 rs_list 只能有一个来源")
        #     return
        if file_dir and file_list is not None:
            print("将路径下文件名列表合并")
            p_dir = os.listdir(file_dir)
            file_list = file_list.append(p_dir)
        if file_list is not None:
            for item in file_list:
                for pf in prefix:
                    if item.startswith(pf):
                        rs.append(item)

        return rs

    # @staticmethod
    @staticmethod
    def filter_suffix(suffix: list, file_list: list, file_dir=None):
        rs = []
        # if file_dir and file_list is None:
        #     p = os.getcwd()
        #     file_list = os.listdir(p)
        # if file_list and file_dir is not None:
        #     print("file_dir 和 rs_list 只能有一个来源")
        #     return
        if file_dir and file_list is not None:
            print("将路径下文件名列表合并")
            p_dir = os.listdir(file_dir)
            file_list = file_list.append(p_dir)
        if file_list is not None:
            for item in file_list:
                for sf in suffix:
                    if item.endswith(sf):
                        rs.append(item)
        return rs


# 获得路径
# icon_req_dir = input("输入请求包路径：\n")
# ff = FilterFiles()


def read_xml(result_dict: dict, find_name: str, find_node: str, find_property: str):
    matcg_list = []
    for key in result_dict.keys():
        # 根据filter_name 的值 来判断key 是否匹配 筛选出来所需要处理的xml
        if find_name in key:
            # matcg_list.append(result_dict.get(key))
            # for xml_file in matcg_list:
                xml_tree = et.parse(result_dict.get(key))
                xml_root = xml_tree.getroot()
                count = 0
                for item in xml_root.findall(find_node):
                    v = item.get(find_property)
                    if bool(is_chinese(v)):
                        py = get_pinyin(v)
                        item.set(find_property, py)
                        count = count + 1
                        # print(item)
                print(f" {count} changes from xml_file ")
                xml_tree.write(result_dict.get(key), encoding="utf-8", xml_declaration=True)
            # print(key)
    print(matcg_list)

    return matcg_list


def rename_xml(xml_file_list: list, find_node: str, chang_property: str):
    for xml_file in xml_file_list:
        xml_tree = et.parse(xml_file)
        xml_root = xml_tree.getroot()
        count = 0
        for item in xml_root.findall(find_node):
            v = item.get(chang_property)
            if bool(is_chinese(v)):
                py = get_pinyin(v)
                item.set(chang_property, py)
                count = count + 1
                # print(item)
        print(f" {count} changes from {xml_file} ")
        xml_tree.write(xml_file, encoding="utf-8", xml_declaration=True)


# 判断是否包含中文
def is_chinese(string):
    check_str = string
    for ch in check_str:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
    return False


# 转换为Pinyin的方法
def get_pinyin(string):
    pinyin = pypinyin.slug(string, separator="")
    return pinyin


xml_file_dir = "/Users/wangjiping/PycharmProjects/copyer/IconRequest-20221001_122347"
xml_file_dir2 = r"C:\Users\YOWH\PycharmProjects\copyer\IconRequest-20221001_122347"

rdict = {"appfilter_12331": "string1", "avpfilter_2331": "strin3234g1", "appfilter_123431": "3424", }
# read_xml(rdict, "filter")
ff = FilterFiles()
rs_list = ff.filter_files(xml_file_dir2,prefix=["app","theme"],suffix=".xml")
appmaplist = read_xml(rs_list,"appmap","item","name")
# rename_xml(appmaplist,"item","name")