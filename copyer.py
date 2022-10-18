"""
修改 xml 和 png 中的中文字

拷贝 xml 内容 到目标路径
- 源 xml 内容添加 项目路径
- 生成 png2mxl
    - png2xml xml 内容添加到目标路径
    - 拷贝 png 到 目标路径

"""
import os


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


# xml_file_dir = os.getcwd()
xml_file_dir = "/Users/wangjiping/PycharmProjects/copyer/IconRequest-20221001_122347"
xml_path = FilterFiles()
xp = xml_path.filter_files(xml_file_dir, prefix=["app"], suffix=[".xml"])
da = xml_path.filter_files(xml_file_dir, suffix=[".png"])
print(f"{xp}\n {type(xp)}")
print(da)
# xml_path.filter_files(xml_file_dir, prefix=["cop"], suffix=[".py"])

# 获得路径
icon_req_dir = input("输入请求包路径：\n")
ff = FilterFiles()


def rename_xml(result_dict: dict):

    print(result_dict)
