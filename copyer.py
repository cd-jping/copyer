"""
修改 xml 和 png 中的中文字

拷贝 xml 内容 到目标路径
- 源 xml 内容添加 项目路径
- 生成 png2mxl
    - png2xml xml 内容添加到目标路径
    - 拷贝 png 到 目标路径

"""
import os
import lxml.etree as lxml_et
import pypinyin
import xml.dom.minidom


class FilterFiles:
    # @staticmethod
    # def __init__(self):
    #     self.file_dir = None
    def filter_files(self, file_dir, prefix: list = None, suffix: list = None):
        result = {}
        count = 0
        # 判断目录，没有则获取当前目录
        if file_dir is None:
            p = os.getcwd()
            file_list = os.listdir(p)
        else:
            file_list = os.listdir(file_dir)
        # 匹配条件判断
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
    def filter_prefix(prefix: list, file_list: list = None, file_dir=None, with_ext_name=True):
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
                    if with_ext_name is False:
                        item = os.path.splitext(item)[0]
                    rs.append(item)

        return rs

    # @staticmethod
    @staticmethod
    def filter_suffix(suffix: list, file_list: list = None, file_dir=None, with_ext_name: bool = True):
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
                    if with_ext_name is False:
                        item = os.path.splitext(item)[0]
                    rs.append(item)
        return rs


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


# 修改文件名为pinyin
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
            # 存入一部字典（同时保留原文件名）{"中文"： "zhongwen"}
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
        txt_name = os.path.join(file_dir, "Changed.txt")
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


def pinyinized_xml(result_dict: dict, find_name: str, find_node: str, find_property: str):
    for key in result_dict.keys():
        # 根据filter_name 的值 来判断key 是否匹配 筛选出来所需要处理的xml
        if find_name in key:
            # match_list.append(result_dict.get(key))
            # for xml_file in match_list:
            xml_tree = lxml_et.parse(result_dict.get(key))
            xml_root = xml_tree.getroot()
            count = 0
            for item in xml_root.findall(find_node):
                v = item.get(find_property)
                if bool(is_chinese(v)):
                    py = get_pinyin(v)
                    item.set(find_property, py)
                    count = count + 1
            print(f"{count} changes from {key}")
            xml_tree.write(result_dict.get(key), encoding="utf-8", xml_declaration=True)


def move_xml_info(req_xml_dir: dict, project_xml_dir: dict, pnglist: list, req_name: list, appfilter_num: int):
    for pro_key in project_xml_dir.keys():
        if "appfilter" in pro_key:
            xml_filter = open(project_xml_dir.get(pro_key), "r", encoding="utf-8")
            line_list = xml_filter.readlines()
            for line_item in line_list:
                for i in req_name:
                    if i in line_item:
                        print(f"{req_name} 已适配")
                        return
    # 追加xml节点信息
    for req_key in req_xml_dir.keys():
        print(req_key)
        # 根据filter_name 的值 来判断key 是否匹配 筛选出来所需要处理的xml
        if "appfilter" in req_key:
            print(req_xml_dir.get(req_key))
            req_xml_tree = lxml_et.parse(req_xml_dir.get(req_key))
            req_xml_root = req_xml_tree.getroot()
            print(req_xml_root.tag)
            del_list = ["iconback", "iconmask", "iconupon", "scale"]
            print("get tree")
            for i in del_list:
                if req_xml_root.find(i) is not None:
                    req_xml_root.remove(req_xml_root.find(i))
                    print(f"shanchu jiedian {req_xml_root.find(i)}")
            # req_xml_tree.write(req_xml_dir.get(req_key), encoding="utf-8", xml_declaration=True)
            print("hhh" + str(project_xml_dir.keys()))
            for pro_key in project_xml_dir.keys():
                print(pro_key)
                if "appfilter" in pro_key:
                    print("appfilter from project")
                    pro_xml_tree = lxml_et.parse(project_xml_dir.get(pro_key))
                    pro_xml_root = pro_xml_tree.getroot()
                    num = len(req_xml_root.findall("item"))
                    for item in req_xml_root.iter("appfilter"):
                        pro_xml_root.extend(item)
                    comments = lxml_et.Comment(f"⬆ {req_key} updated, {num} ⬆")
                    comments.tail = "\n"
                    pro_xml_root.append(comments)
                    pro_xml_tree.write(project_xml_dir.get(pro_key), encoding="utf-8", xml_declaration=True)
                    print(f"appfilter 已经处理 {req_key}")

        if "appmap" in req_key:
            req_xml_tree = lxml_et.parse(req_xml_dir.get(req_key))
            req_xml_root = req_xml_tree.getroot()
            # del_list = ["iconback", "iconmask", "iconupon", "scale"]
            # for i in del_list:
            #     req_xml_root.remove(req_xml_root.find(i))
            for pro_key in project_xml_dir.keys():
                if "appmap" in pro_key:
                    pro_xml_tree = lxml_et.parse(project_xml_dir.get(pro_key))
                    pro_xml_root = pro_xml_tree.getroot()
                    num = len(req_xml_root.findall("item"))
                    for item in req_xml_root.iter("appmap"):
                        pro_xml_root.extend(item)
                    comments = lxml_et.Comment(f"⬆ {req_key} updated, {num} ⬆")
                    comments.tail = "\n"
                    pro_xml_root.append(comments)
                    pro_xml_tree.write(project_xml_dir.get(pro_key), encoding="utf-8", xml_declaration=True)
                    print(f"appmap 已经处理 {req_key}")
        if "theme_resources" in req_key:
            req_xml_tree = lxml_et.parse(req_xml_dir.get(req_key))
            req_xml_root = req_xml_tree.getroot()
            del_list = ["Label", "Wallpaper", "LockScreenWallpaper", "ThemePreview", "ThemePreviewWork",
                        "ThemePreviewMenu", "DockMenuAppIcon"]
            for i in del_list:
                req_xml_root.remove(req_xml_root.find(i))
            for pro_key in project_xml_dir.keys():
                if "theme_resources" in pro_key:
                    pro_xml_tree = lxml_et.parse(project_xml_dir.get(pro_key))
                    pro_xml_root = pro_xml_tree.getroot()
                    num = len(req_xml_root.findall("AppIcon"))
                    for item in req_xml_root.iter("Theme"):
                        pro_xml_root.extend(item)
                    comments = lxml_et.Comment(f"⬆ {req_key} updated, {num} ⬆")
                    comments.tail = "\n"
                    pro_xml_root.append(comments)
                    pro_xml_tree.write(project_xml_dir.get(pro_key), encoding="utf-8", xml_declaration=True)
                    print(f"theme_res 已经处理 {req_key}")

    # 根据 png 生成 drawable 和 icon_pack 节点并追加到 目标路径
    for pro_key in project_xml_dir.keys():
        # icon_pack 资源生成
        if "icon_pack" in pro_key:
            icon_pack_tree = lxml_et.parse(project_xml_dir.get(pro_key),
                                           parser=lxml_et.XMLParser(encoding="utf-8", remove_blank_text=True))
            icon_pack_root = icon_pack_tree.getroot()
            if icon_pack_root.find("./starry-array/[@name='Adaptation']") is None:
                tar_tag = lxml_et.Element("starry-array", name="Adaptation")
            else:
                tar_tag = icon_pack_root.find("./starry-array/[@name='Adaptation']")
            num = len(pnglist)
            for png_name in pnglist:
                item = lxml_et.Element("item")
                item.text = png_name
                tar_tag.insert(0, item)
            comments = lxml_et.Comment(f"⬇ {num} icons updated ⬇")
            tar_tag.insert(0, comments)
            icon_pack_tree.write(project_xml_dir.get(pro_key), encoding="utf-8", xml_declaration=True,
                                 pretty_print=True)
            print(f"icon_pack 已经处理 {pro_key}")

        # drawable 资源生成
        if "drawable" in pro_key:
            # resources
            drawable_tree = lxml_et.parse(project_xml_dir.get(pro_key),
                                          parser=lxml_et.XMLParser(encoding="utf-8", remove_blank_text=True))
            drawable_root = drawable_tree.getroot()
            if drawable_root.find("./category/[@title='System ICONS']") is None:
                tar_tag = lxml_et.Element("category", name="System ICONS")
                drawable_root.append(tar_tag)
            else:
                tar_tag = drawable_root.find("./category/[@title='System ICONS']")
            num = len(pnglist)
            for png_name in pnglist:
                item = lxml_et.Element("item")
                item.set("drawable", png_name)
                tar_tag.addnext(item)
            comments = lxml_et.Comment(f"⬇ {num} icons updated ⬇")
            tar_tag.addnext(comments)
            drawable_tree.write(project_xml_dir.get(pro_key), encoding="utf-8", xml_declaration=True,
                                pretty_print=True)
            print(f"drawable 已经处理 {pro_key}")
        # project 路径里面 统计app filter 的总item数量 减去上次的数字
        if "changelog" in pro_key:
            # resources
            changelog_tree = lxml_et.parse(project_xml_dir.get(pro_key))
            changelog_root = changelog_tree.getroot()
            if changelog_root.find("./item/[@number]") is None:
                tar_tag = lxml_et.Element("item", number="0")
                changelog_root.append(tar_tag)
            else:
                tar_tag = changelog_root.find("./item/[@number]")
            xml_number = tar_tag.get("number")
            number = appfilter_num + int(xml_number)
            tar_tag.set("number", str(number))
            tar_tag.set("text", f"{number} icons updated!\n{number} 个图标已适配!")
            changelog_tree.write(project_xml_dir.get(pro_key), encoding="utf-8", xml_declaration=True,
                                 pretty_print=True)
            print(f"changelog 已经处理 {pro_key}")
        # 复制 png 资源（考虑覆盖问题）


def find_file(project_dir: str, find_name: list):
    find_xml = {}
    count = 0
    for root, dirs, files in os.walk(project_dir):
        for file in files:
            for f_name in find_name:
                if f_name in file:
                    count = count + 1
                    file = file + str(count)
                    file_path = os.path.join(root, file)
                    find_xml.update({file: file_path})
    return find_xml

    # find_xml = {}
    # count = 0
    # file_list = os.listdir(project_dir)
    # for file in file_list:
    #     file_path = os.path.join(project_dir, file)
    #     if os.path.isfile(file_path):
    #         for name in find_name:
    #             if name in file:
    #                 count = count + 1
    #                 file = file + str(count)
    #                 find_xml.update({file: file_path})
    #                 print(find_xml)
    #                 print(count)
    #                 # print(file_path)
    #
    #     else:
    #         find_file(file_path, find_name)
    #
    # print(find_xml)
    # return find_xml


# xml_file_dir = "/Users/wangjiping/PycharmProjects/copyer/IconRequest-20221001_122347"
# xml_file_dir3 = "/Users/WangChunsheng/PycharmProjects/copyer/IconRequest-20221001_122347"
# xml_file_dir2 = r"C:\Users\YOWH\PycharmProjects\copyer\IconRequest-20221001_122347"

# rdict = {"appfilter_12331": "string1", "avpfilter_2331": "strin3234g1", "appfilter_123431": "3424", }
# read_xml(rdict, "filter")

# rs_list = ff.filter_files(xml_file_dir2, prefix=["app", "theme"], suffix=[".xml"])
# appmaplist = read_xml(rs_list, "appmap", "item", "name")
# rename_xml(appmaplist,"item","name")

# png_dir = "/Users/WangChunsheng/PycharmProjects/copyer/IconRequest-20221001_122347"
# png_dir2 = "/Users/wangjiping/PycharmProjects/copyer/IconRequest-20221001_122347"
# png_list = ff.filter_suffix(suffix=[".png"], file_list=None,
#                             file_dir=png_dir2, with_ext_name=False)
#
# print(png_list)

# rename_file(png_list, file_dir=png_dir)
# xml_dict = ff.filter_files(xml_file_dir, prefix=["appfilter", "appmap", "theme_resources"], suffix=[".xml"])
# print(xml_dict)
# pinyinized_xml(xml_dict, "theme", "AppIcon", "image")

# project_dir = input("输入包含替换资源的项目文件夹\n")
# name = "appfilter"
# move_xml_info(xml_dict)


# route = input('请输入要查找的路径：')
# name = input('请输入要查找的文件：')


"""
从 xml dict 里面 找 对应文件 比如 appmap 
再 project xml dict 里面找 对应文件 appmap 文件

"""


# 判断文件夹名称 是否拷贝过 在目标文件注释里面
# 第一步获取列表时候 保存一个变量 用于后续比对
#
# 读取请求文件夹路径中的xml 读取节点
# 读取目标文件夹 xml 读取节点
#         统计一下item条数
#     固定条件读取和对应匹配
#         appfilter
#         drawable
#         appmap
#         theme_res
#         icon_pack
#         changlog item 图标适配个数
#
# 添加原节点到目标节点上
# 添加注释信息 带有时间的文件夹名（其他必要信息）
#  project_dir: dict, png_list, req_name: str,

def user_input(tipinf: str, cur_dir: bool = False):
    str_input = input(tipinf)

    if str_input == "q":
        exit()
        return
    if cur_dir is True:
        if str_input == "":
            str_input = os.getcwd()
            return str_input
        elif bool(os.path.isdir(str_input)) is False:
            print("文件夹目录有误")
            user_input(tipinf, cur_dir=True)
    else:
        if str_input == "" or bool(os.path.isdir(str_input)) is False:
            print("文件夹目录有误")
            user_input(tipinf)
    return str_input


def menu_number(input_str: str):
    match input_str:
        case "1":
            req_icon_dir = user_input(tipinf="请输入 req_icon 文件夹路径(如在 req_icon 文件夹 按 Enter)\nq:退出\n",
                                      cur_dir=True)
            req_dir_dict = ff.filter_files(file_dir=req_icon_dir, prefix=["appfilter", "appmap", "theme_resources"],
                                           suffix=[".xml"])
            pinyinized_xml(result_dict=req_dir_dict, find_name="appfilter", find_node="item", find_property="drawable")
            pinyinized_xml(result_dict=req_dir_dict, find_name="appmap", find_node="item", find_property="name")
            pinyinized_xml(result_dict=req_dir_dict, find_name="theme_resources", find_node="AppIcon",
                           find_property="image")
        case "2":
            req_icon_dir = user_input(tipinf="请输入 req_icon 文件夹路径\nq:退出\n")

            req_xml_dict = ff.filter_files(file_dir=req_icon_dir, prefix=["appfilter", "appmap", "theme_resources"],
                                           suffix=[".xml"])
            png_number = ff.filter_suffix(suffix=[".png"], file_dir=req_icon_dir)
            icon_number = len(png_number)
            req_name = list(req_xml_dict.keys())
            project_dir = user_input(tipinf="请输入项目文件夹路径\nq:退出\n")
            # if project_dir == "q":
            #     menu_number("q")
            print("p xml ")
            project_xml_dict = find_file(project_dir,
                                         find_name=["appfilter", "appmap", "theme_resources", "drawable", "icon_pack"])

            # reqname 改成list；
            # get pngicondir
            png_dir = user_input(tipinf="请输入 已制作图标 文件夹路径\nq:退出\n")
            # if req_icon_dir == "q":
            #     menu_number("q")
            png_list = ff.filter_suffix(suffix=[".png"], file_dir=png_dir, with_ext_name=False)
            print(png_list)
            move_xml_info(req_xml_dict, project_xml_dir=project_xml_dict, appfilter_num=icon_number, req_name=req_name,
                          pnglist=png_list)

            # print("2")
        case "q" | "Q":
            print("exit")
            exit()
        case _:
            if os.name == 'nt':  # 如果当前系统为WINDOWS
                os.system('cls')  # 执行cls清屏命令
            else:
                os.system('clear')  # 其它linux等系统执行clear命令
            print(menulist)
            menu_number(input("请输入序号\n"))


menulist = """
"1": "重命名为中文名称为 pinyin"
"2": "拷贝 XML 信息到项目文件夹"
----------------------------
"Q": "退出 copyer"
"""

# ff = FilterFiles()
tip = "拷贝文件夹路径快捷键\nmacOS:\toption + command + c\nWindows:\tshift + RightClick\n"
print(tip)
# input_number = input(menulist)
ff = FilterFiles()
# menu_number(input_number)


# req_icon_dir = user_input(tipinf="请输入 req_icon 文件夹路径\nq:退出\n")
req_icon_dir = "/Users/wangjiping/Downloads/IconRequest-20221001_122347"

req_xml_dict = ff.filter_files(file_dir=req_icon_dir, prefix=["appfilter", "appmap", "theme_resources"],
                               suffix=[".xml"])
png_number = ff.filter_suffix(suffix=[".png"], file_dir=req_icon_dir)
icon_number = len(png_number)
req_name = list(req_xml_dict.keys())
# project_dir = user_input(tipinf="请输入项目文件夹路径\nq:退出\n")
project_dir = "/Users/wangjiping/Downloads/demo"
# if project_dir == "q":
#     menu_number("q")
print("p xml ")
project_xml_dict = find_file(project_dir=project_dir,
                             find_name=["appfilter", "appmap", "theme_resources", "drawable", "icon_pack"])
print(project_xml_dict)
# reqname 改成list；
# get pngicondir
# png_dir = user_input(tipinf="请输入 已制作图标 文件夹路径\nq:退出\n")
png_dir = "/Users/wangjiping/Downloads/IconRequest-20221001_122347"
# if req_icon_dir == "q":
#     menu_number("q")
png_list = ff.filter_suffix(suffix=[".png"], file_dir=png_dir, with_ext_name=False)
print(png_list)
move_xml_info(req_xml_dict, project_xml_dir=project_xml_dict, appfilter_num=icon_number, req_name=req_name,
              pnglist=png_list)
