# 读取文件夹 主要是获取当中的xml文件 并解析 然后在将读取到内容 添加到 目标路径的 xml 文件当中（xml里面要加注释标记更新）
"""
图标包请求文件夹
"""
import os

# import os

print("Mac 复制路径快捷键 option + command + c\nWindows 复制路径 shift + 鼠标右键")


# icon_req_dir = input("输入图标请求文件夹路径\n")
# icon_cre_dir = input("输入已制作图标文件夹\n")
# target_dir = input("输入项目文件夹\n")
#

# 过滤所需要的文件类型并返回一个list


# def filter_files_type(path=None, ext_type=""):
#     global file_name
#     result_list = []
#     if path is None:
#         path = os.getcwd()
#         print(path)
#     file_list = os.listdir(path)
#     for file_name in file_list:
#         if not file_name.endswith(ext_type):
#             continue
#     return result_list.append(file_name)
#

class FilterFiles:
    def __init__(self, file_dir: str):
        self.file_dir = file_dir

    # @staticmethod
    # def filter_type(self, ext_type):
    #     result_list = []
    #     file_list = os.listdir(self.file_dir)
    #     for file_name in file_list:
    #         if file_name.endswith(ext_type):
    #             result_list.append(file_name)
    #     return result_list

    def filter_prefix(self, inputlist: list = None, prefix: tuple = None):
        result_list = []
        if inputlist != None:
            file_list = inputlist
        else:
            file_list = os.listdir(self.file_dir)
        # 遍历文件列表
        for file_name in file_list:
            # 遍历 关键词
            for pf in prefix:
                if file_name.startswith(pf):
                    result_list.append(file_name)
        return result_list

    def filter_suffix(self, inputlist: tuple = None, suffix: tuple = None):
        result_list = []
        if inputlist != None:
            file_list = inputlist
            print("fei kong")
        else:
            file_list = os.listdir(self.file_dir)
        # 遍历文件列表
        for file_name in file_list:
            # 遍历 关键词
            for sf in suffix:
                if file_name.endswith(sf):
                    result_list.append(file_name)
        return result_list

    # def filter_filename(self, keyword=None , prefix: tuple = None, suffix: tuple = None):
    #     result_list = []
    #     file_list = os.listdir(self.file_dir)
    #     # if prefix and suffix is None:

    #     if prefix != None:
    #         for p in prefix:
    #             if file_name.startwish(p):
    #                 result_list.append(file_name)
    #     if keyword != None:
    #         file_name.find(keyword):
    #         result_list.append(file_name)

    #     for file_name in file_list:

    #         if file_name.find(keyword)!= -1:
    #             result_list.append(file_name)
    #     return result_list


# /Users/wangjiping/PycharmProjects/copyer
# path = "jjhkjhk"
ff = FilterFiles(r"/Users/wangjiping/PycharmProjects/copyer")

# print(FilterFiles)
# xml_filter.__int__("/Users/wangjiping/PycharmProjects/copyer")

print(ff.filter_suffix(suffix=[".py"]))
