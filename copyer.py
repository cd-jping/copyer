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
import xml.dom.minidom


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
    def filter_prefix(prefix: list, file_list: list = None, file_dir=None):
        rs = []
        # if file_dir and file_list is None:
        #     p = os.getcwd()
        #     file_list = os.listdir(p)
        # if file_list and file_dir is not None:
        #     print("file_dir 和 rs_list 只能有一个来源")
        #     return
        if file_dir is not None and file_list is not None:
            print("将路径下文件名列表合并")
            p_dir = os.listdir(file_dir)
            file_list = file_list.append(p_dir)
        elif file_dir is not None and file_list is None:
            file_list = os.listdir(file_dir)
        # if file_list is not None:
        for item in file_list:
            for pf in prefix:
                if item.startswith(pf):
                    rs.append(item)

        return rs

    # @staticmethod
    @staticmethod
    def filter_suffix(suffix: list, file_list: list = None, file_dir=None):
        rs = []
        # if file_dir and file_list is None:
        #     p = os.getcwd()
        #     file_list = os.listdir(p)
        # if file_list and file_dir is not None:
        #     print("file_dir 和 rs_list 只能有一个来源")
        #     return
        if file_dir is not None and file_list is not None:
            print("将路径下文件名列表合并")
            p_dir = os.listdir(file_dir)
            file_list = file_list.append(p_dir)
        elif file_dir is not None and file_list is None:
            file_list = os.listdir(file_dir)
        # if file_list is not None:
        for item in file_list:
            for sf in suffix:
                if item.endswith(sf):
                    rs.append(item)
        return rs


# 获得路径
# icon_req_dir = input("输入请求包路径：\n")
# ff = FilterFiles()


def edit_xml(result_dict: dict, find_name: str, find_node: str, find_property: str):
    match_list = []
    for key in result_dict.keys():
        # 根据filter_name 的值 来判断key 是否匹配 筛选出来所需要处理的xml
        if find_name in key:
            # match_list.append(result_dict.get(key))
            # for xml_file in match_list:
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
            print(f" {count} changes from {key}")
            xml_tree.write(result_dict.get(key), encoding="utf-8", xml_declaration=True)
        # print(key)
    print(match_list)

    return match_list


# def edit_xml(xml_file_list: list, find_node: str, chang_property: str):
#     for xml_file in xml_file_list:
#         xml_tree = et.parse(xml_file)
#         xml_root = xml_tree.getroot()
#         count = 0
#         for item in xml_root.findall(find_node):
#             v = item.get(chang_property)
#             if bool(is_chinese(v)):
#                 py = get_pinyin(v)
#                 item.set(chang_property, py)
#                 count = count + 1
#                 # print(item)
#         print(f" {count} changes from {xml_file} ")
#         xml_tree.write(xml_file, encoding="utf-8", xml_declaration=True)


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


def rename_file(file_list: list, file_dir: str):
    chinese_list = {}
    english_list = []
    for f_name in file_list:
        # f_name = os.path.splitext(f_name)[0]
        if bool(is_chinese(f_name)):
            # 转换成Pinyin
            py = get_pinyin(f_name)

            # 修改实际文件名
            py_file_name = os.path.join(file_dir, py)
            or_file_name = os.path.join(file_dir, f_name)
            os.rename(or_file_name, py_file_name)
            # 存入一个字典（同时保留原文件名）{"中文"： "zhongwen"}
            f_name = os.path.splitext(f_name)[0]
            py = os.path.splitext(py)[0]
            chinese_list.update({f_name: py})
        else:
            f_name = os.path.splitext(f_name)[0]
            english_list.append(f_name)
    if len(chinese_list) == 0:
        print("No File Changed!")
    else:
        print(str(len(chinese_list)) + " files")
        txt_name = os.path.join(png_dir, "Changed.txt")
        file = open(txt_name, 'w', encoding='utf-8')
        # 遍历字典的元素，将每项元素的key和value分拆组成字符串，注意添加分隔符和换行符
        for k, v in chinese_list.items():
            file.write(str(k) + '\t\t' + str(v) + '\n')
        for eng in english_list:
            file.write(str(eng) + '\n')
        file.close()
        print("TXT File Exported")


def create_drawable(file_list: list):
    # 创建文档在内存中
    xml_drawable = xml.dom.minidom.Document()
    # 创建元素
    resources = xml_drawable.createElement('resources')
    # 将元素添加的文档中
    xml_drawable.appendChild(resources)

    for i in file_list:
        item = xml_drawable.createElement('item')
        # 把列表中的文件名插入”drawable“属性中
        item.setAttribute('drawable', str(i))
        resources.appendChild(item)

    fp = open('drawable.xml', 'w', encoding='utf-8')

    xml_drawable.writexml(fp, indent='\t', addindent='\t', newl='\n', encoding='utf-8')
    print("Drawable-XML File Exported")


def create_icon_pack(file_list):
    # 创建文档在内存中
    xml_icon_pack = xml.dom.minidom.Document()
    # 创建元素
    resources = xml_icon_pack.createElement('resources')
    # 将元素添加的文档中
    xml_icon_pack.appendChild(resources)
    for i in file_list:
        item = xml_icon_pack.createElement('item')
        item.appendChild(xml_icon_pack.createTextNode(str(i)))
        resources.appendChild(item)

    fp = open('icon_pack.xml', 'w', encoding='utf-8')
    xml_icon_pack.writexml(fp, indent='\t', addindent='\t', newl='\n', encoding='utf-8')
    print("ICON_PACK-XML File Exported")


xml_file_dir = "/Users/WangChunsheng/PycharmProjects/copyer/IconRequest-20221001_122347"
xml_file_dir2 = r"C:\Users\YOWH\PycharmProjects\copyer\IconRequest-20221001_122347"

rdict = {"appfilter_12331": "string1", "avpfilter_2331": "strin3234g1", "appfilter_123431": "3424", }
# read_xml(rdict, "filter")
ff = FilterFiles()
# rs_list = ff.filter_files(xml_file_dir2, prefix=["app", "theme"], suffix=[".xml"])
# appmaplist = read_xml(rs_list, "appmap", "item", "name")
# rename_xml(appmaplist,"item","name")

png_dir = "/Users/WangChunsheng/PycharmProjects/copyer/IconRequest-20221001_122347"
png_list = ff.filter_suffix(suffix=[".png"], file_list=None,
                            file_dir="/Users/WangChunsheng/PycharmProjects/copyer/IconRequest-20221001_122347")
print(png_list)
rename_file(png_list, file_dir=png_dir)
xml_dict = ff.filter_files(xml_file_dir, prefix=["appfilter", "appmap", "theme_resources"], suffix=[".xml"])
edit_xml(xml_dict, "appmap", "item", "name")

# project_dir = input("输入包含替换资源的项目文件夹\n")
# name = "appfilter"

route = input('请输入要查找的路径：')
name = input('请输入要查找的文件：')


def find_file(project_dir: str, find_name: str):
    file_list = os.listdir(project_dir)
    for file in file_list:
        file_path = os.path.join(project_dir, file)
        if os.path.isfile(file_path):
            if find_name in file:
                print(file_path)
                # break
        else:
            find_file(file_path, find_name)


# find_file(route, name)
# 处理 目标路径
# 获得1⃣️设计图标路径
# 生成xml信息在目标路径 （拷贝的方法需要修改
#   - 先 解析 目标文件
#   - 增加 节点数据
#   - 更新 保存文件
