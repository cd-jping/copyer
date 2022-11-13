import copy
import os

import lxml.etree as lxml_et
import pypinyin

"""
Copyer 1.0.0 初版本
Starrylight

功能：
- pinyinized
    实现将 xml 中的标签属性 修改为 pinyin
- Copyer
    根据输入的目录将 xml 的节点更新追加到目标项目文件夹中对应的 xml 中。
    根据目录中的图标文件，生成所需 xml 追加到目标项目文件夹中对应的 xml 中。
    追加节点会计算数量，以注释的方式更新到xml中。
    更新日志信息，自动累计更新图标数量。
"""

"""
FilterFiles 文件过滤器 
实现了可以根据多个关键词 前缀 或 后缀 匹配文件名；返回一个字典{filename:filepath}
后续可以根据字典直接取对应的文件路径。
"""


class FilterFiles:
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
            print("至少有一个匹配条件！")
            return
        elif prefix is not None and suffix is not None:
            # 同时匹配前缀和后缀过滤，file list 结果作为输入再次匹配第二个条件
            file_list = self.filter_prefix(prefix, file_list)
            file_list = self.filter_suffix(suffix, file_list)
        elif prefix is not None:
            file_list = self.filter_prefix(prefix, file_list)
        elif suffix is not None:
            file_list = self.filter_suffix(suffix, file_list)
        for file_name in file_list:
            file_path = os.path.join(file_dir, file_name)
            count = count + 1
            result.update({file_name: file_path})
        print(f"匹配 {count} 个文件")
        return result

    @staticmethod
    def filter_prefix(prefix: list, file_list: list = None, file_dir=None, with_ext_name=True):
        rs = []
        if file_dir is not None and file_list is not None:
            print("将路径下文件名列表合并")
            p_dir = os.listdir(file_dir)
            file_list = file_list.append(p_dir)
        elif file_dir is not None and file_list is None:
            file_list = os.listdir(file_dir)
        for item in file_list:
            for pf in prefix:
                if item.startswith(pf):
                    if with_ext_name is False:
                        item = os.path.splitext(item)[0]
                    rs.append(item)
        return rs

    @staticmethod
    def filter_suffix(suffix: list, file_list: list = None, file_dir=None, with_ext_name: bool = True):
        rs = []
        if file_dir is not None and file_list is not None:
            print("将路径下文件名列表合并")
            p_dir = os.listdir(file_dir)
            file_list = file_list.append(p_dir)
        elif file_dir is not None and file_list is None:
            file_list = os.listdir(file_dir)
        for item in file_list:
            for sf in suffix:
                if item.endswith(sf):
                    if with_ext_name is False:
                        item = os.path.splitext(item)[0]
                    rs.append(item)
        return rs


# 修改文件名为pinyin
def rename_file(file_list: list, file_dir: str):
    chinese_list = {}
    english_list = []
    for f_name in file_list:
        if bool(is_chinese(f_name)):
            # 转换成Pinyin
            py = pypinyin.slug(f_name, separator="")
            # 修改png文件名
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
        # 遍历字典的元素，将每项元素的key和value分拆组成字符串
        for k, v in chinese_list.items():
            file.write(str(k) + '\t\t' + str(v) + '\n')
        for eng in english_list:
            file.write(str(eng) + '\n')
        file.close()
        print("TXT File Exported")


# 判断是否包含中文
def is_chinese(string):
    check_str = string
    for ch in check_str:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
    return False


# 修改xml里面的中文；并且忽略注释中的中文名称
def pinyinized_xml(result_dict: dict, find_name: str, find_node: str, find_property: str):
    for key in result_dict.keys():
        # 根据filter_name 的值 来判断key 是否匹配 筛选出来所需要处理的xml
        if find_name in key:
            xml_tree = lxml_et.parse(result_dict.get(key))
            xml_root = xml_tree.getroot()
            count = 0
            for item in xml_root.findall(find_node):
                v = item.get(find_property)
                if bool(is_chinese(v)):
                    py = pypinyin.slug(v, separator="")
                    item.set(find_property, py)
                    count = count + 1
            print(f"{count} changes from {key}")
            xml_tree.write(result_dict.get(key), encoding="utf-8", xml_declaration=True)


def move_xml_info(req_xml_dir: dict, project_xml_dir: dict, pnglist: list, req_name: list, appfilter_num: int):
    # 判断是否已经适配过这个文件夹
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
        # 根据filter_name 的值 来判断key 是否匹配 筛选出来所需要处理的xml
        if "appfilter" in req_key:
            req_xml_tree = lxml_et.parse(req_xml_dir.get(req_key))
            req_xml_root = req_xml_tree.getroot()
            # 删除多余的无用标签
            del_list = ["iconback", "iconmask", "iconupon", "scale"]
            for i in del_list:
                if req_xml_root.find(i) is not None:
                    req_xml_root.remove(req_xml_root.find(i))
            req_xml_root_bak = copy.copy(req_xml_root)
            for pro_key in project_xml_dir.keys():
                if "appfilter" in pro_key:
                    pro_xml_tree = lxml_et.parse(project_xml_dir.get(pro_key))
                    pro_xml_root = pro_xml_tree.getroot()
                    num = len(req_xml_root.findall("item"))
                    # iter 迭代器 在xml文件结构中可以按深度迭代（应该是嵌套深度）正好只有这个方法可以把第一层 root 标签过滤掉。
                    for item in req_xml_root_bak.iter("resources"):
                        pro_xml_root.extend(item)
                    comments = lxml_et.Comment(f"⬆ {req_key} updated, {num} ⬆")
                    comments.tail = "\n"
                    pro_xml_root.append(comments)
                    pro_xml_tree.write(project_xml_dir.get(pro_key), encoding="utf-8", xml_declaration=True)
                    print(f"appfilter 已经处理 {req_key}")
                req_xml_root_bak = copy.copy(req_xml_root)
        if "appmap" in req_key:
            req_xml_tree = lxml_et.parse(req_xml_dir.get(req_key))
            req_xml_root = req_xml_tree.getroot()
            req_xml_root_bak = copy.copy(req_xml_root)
            for pro_key in project_xml_dir.keys():
                if "appmap" in pro_key:
                    pro_xml_tree = lxml_et.parse(project_xml_dir.get(pro_key))
                    pro_xml_root = pro_xml_tree.getroot()
                    num = len(req_xml_root.findall("item"))
                    for item in req_xml_root_bak.iter("appmap"):
                        pro_xml_root.extend(item)
                    comments = lxml_et.Comment(f"⬆ {req_key} updated, {num} ⬆")
                    comments.tail = "\n"
                    pro_xml_root.append(comments)
                    pro_xml_tree.write(project_xml_dir.get(pro_key), encoding="utf-8", xml_declaration=True)
                    print(f"appmap 已经处理 {req_key}")
                req_xml_root_bak = copy.copy(req_xml_root)
        if "theme_resources" in req_key:
            req_xml_tree = lxml_et.parse(req_xml_dir.get(req_key))
            req_xml_root = req_xml_tree.getroot()
            del_list = ["Label", "Wallpaper", "LockScreenWallpaper", "ThemePreview", "ThemePreviewWork",
                        "ThemePreviewMenu", "DockMenuAppIcon"]
            for i in del_list:
                if req_xml_root.find(i) is not None:
                    req_xml_root.remove(req_xml_root.find(i))
            req_xml_root_bak = copy.copy(req_xml_root)
            for pro_key in project_xml_dir.keys():
                if "theme_resources" in pro_key:
                    pro_xml_tree = lxml_et.parse(project_xml_dir.get(pro_key))
                    pro_xml_root = pro_xml_tree.getroot()
                    num = len(req_xml_root.findall("AppIcon"))
                    for item in req_xml_root_bak.iter("Theme"):
                        pro_xml_root.extend(item)
                    comments = lxml_et.Comment(f"⬆ {req_key} updated, {num} ⬆")
                    comments.tail = "\n"
                    pro_xml_root.append(comments)
                    pro_xml_tree.write(project_xml_dir.get(pro_key), encoding="utf-8", xml_declaration=True)
                    print(f"theme_res 已经处理 {req_key}")
                req_xml_root_bak = copy.copy(req_xml_root)
    # 根据 png 生成 drawable 和 icon_pack 节点并追加到 目标路径
    for pro_key in project_xml_dir.keys():
        # icon_pack 资源生成
        if "icon_pack" in pro_key:
            icon_pack_tree = lxml_et.parse(project_xml_dir.get(pro_key),
                                           parser=lxml_et.XMLParser(encoding="utf-8", remove_blank_text=True))
            icon_pack_root = icon_pack_tree.getroot()
            if icon_pack_root.find("./string-array/[@name='Adaptation']") is None:
                tar_tag = lxml_et.Element("string-array", name="Adaptation")
                icon_pack_root.append(tar_tag)
            else:
                tar_tag = icon_pack_root.find("./string-array/[@name='Adaptation']")
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
            if drawable_root.find("./category/[@title='All ICONS']") is None:
                tar_tag = lxml_et.Element("category", title="All ICONS")
                drawable_root.append(tar_tag)
            else:
                tar_tag = drawable_root.find("./category/[@title='All ICONS']")
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
        # 从 req 文件夹获取原始的png数量加上 log 中记录的图标数量
        if "changelog" in pro_key:
            changelog_tree = lxml_et.parse(project_xml_dir.get(pro_key))
            changelog_root = changelog_tree.getroot()
            if changelog_root.findall("string-array") is None:
                if changelog_root.find("./item/[@number]") is None:
                    tar_tag = lxml_et.Element("item", number="0")
                    changelog_root.append(tar_tag)
                else:
                    tar_tag = changelog_root.find("./item/[@number]")
                xml_number = tar_tag.get("number")
                number = appfilter_num + int(xml_number)
                tar_tag.set("number", str(number))
                tar_tag.set("text",
                            f"Current Update {appfilter_num} Icons, {number} Icons Updated!\\n"
                            f"当前更新 {appfilter_num} 个图标, {number} 个图标已适配!")
            else:
                if changelog_root.find("./string-array/item/[@number]") is None:
                    tar_tag = lxml_et.Element("item", number="0")
                    changelog_root.append(tar_tag)
                else:
                    tar_tag = changelog_root.find("./string-array/item/[@number]")
                xml_number = tar_tag.get("number")
                number = appfilter_num + int(xml_number)
                tar_tag.set("number", str(number))
                tar_tag.text = f"Current Update {appfilter_num} Icons, {number} Icons Updated!\\n当前更新 {appfilter_num} 个图标, {number} 个图标已适配!"


            changelog_tree.write(project_xml_dir.get(pro_key), encoding="utf-8", xml_declaration=True,
                                 pretty_print=True)
            print(f"changelog 已经处理 {pro_key}")


# 这个findfile会找出子目录所匹配的指定文件
def find_file(project_dir: str, find_name: list):
    find_xml = {}
    count = 0
    for root, dirs, files in os.walk(project_dir):
        for file in files:
            for f_name in find_name:
                if f_name in file:
                    count = count + 1
                    file_name = os.path.splitext(file)[0]
                    file_name = file_name + str(count)
                    file_path = os.path.join(root, file)
                    find_xml.update({file_name: file_path})
    return find_xml


# 接收用户输入的路径，cur_dir可以允许使用当前路径处理（仅限pinyinized）
def user_input(tipinf: str, cur_dir: bool = False):
    # 提示信息
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
            if os.name == 'nt':  # 如果当前系统为WINDOWS
                os.system('cls')  # 执行cls清屏命令
            else:
                os.system('clear')  # 其它linux等系统执行clear命令
            req_icon_dir = user_input(tipinf="请输入 req_icon 文件夹路径(如在 req_icon 文件夹 按 Enter)\nq:退出\n",
                                      cur_dir=True)
            req_dir_dict = ff.filter_files(file_dir=req_icon_dir, prefix=["appfilter", "appmap", "theme_resources"],
                                           suffix=[".xml"])
            pinyinized_xml(result_dict=req_dir_dict, find_name="appfilter", find_node="item", find_property="drawable")
            pinyinized_xml(result_dict=req_dir_dict, find_name="appmap", find_node="item", find_property="name")
            pinyinized_xml(result_dict=req_dir_dict, find_name="theme_resources", find_node="AppIcon",
                           find_property="image")
            png_list = ff.filter_suffix(suffix=[".png"], file_dir=req_icon_dir)
            rename_file(file_list=png_list, file_dir=req_icon_dir)
        case "2":
            if os.name == 'nt':  # 如果当前系统为WINDOWS
                os.system('cls')  # 执行cls清屏命令
            else:
                os.system('clear')  # 其它linux等系统执行clear命令
            req_icon_dir = user_input(tipinf="请输入 req_icon 文件夹路径\nq:退出\n")
            req_xml_dict = ff.filter_files(file_dir=req_icon_dir, prefix=["appfilter", "appmap", "theme_resources"],
                                           suffix=[".xml"])
            png_number = ff.filter_suffix(suffix=[".png"], file_dir=req_icon_dir)
            icon_number = len(png_number)
            req_name = list(req_xml_dict.keys())
            project_dir = user_input(tipinf="请输入项目文件夹路径\nq:退出\n")
            project_xml_dict = find_file(project_dir=project_dir,
                                         find_name=["appfilter", "appmap", "theme_resources", "drawable", "icon_pack",
                                                    "changelog"])
            png_dir = user_input(tipinf="请输入 已制作图标 文件夹路径\nq:退出\n")
            png_list = ff.filter_suffix(suffix=[".png"], file_dir=png_dir, with_ext_name=False)
            move_xml_info(req_xml_dict, project_xml_dir=project_xml_dict, appfilter_num=icon_number, req_name=req_name,
                          pnglist=png_list)
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
tip = "拷贝文件夹路径快捷键\nmacOS:\toption + command + c\nWindows:\tshift + RightClick\n"
input_number = input(menulist)
ff = FilterFiles()
menu_number(input_number)
