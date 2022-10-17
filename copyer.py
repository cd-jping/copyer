"""
修改 xml 和 png 中的中文字

拷贝 xml 内容 到目标路径
- 源 xml 内容添加 项目路径
- 生成 png2mxl
    - png2xml xml 内容添加到目标路径
    - 拷贝 png 到 目标路径

"""
import os




class FilesFilter:


    def filter_files(self, file_dir: str = None, prefix: list = None, suffix: list = None, keywords=None):

        result = {}
        count = 0
        if file_dir is None:
            p = os.getcwd()
            file_list = os.listdir(p)
        else:
            file_list = os.listdir(file_dir)

        if prefix and suffix and keywords is None:
            print("无意义过滤，prefix，suffix，keywords 至少输入一个参数！")
        elif prefix and suffix is not None:

        elif keywords is not None:
            self.filter_keyword(file_list)
        elif prefix is not None:
            self.filter_prfix(prefix)
        elif suffix is not None:
            self.filter_sufix(file_list)

    # @staticmethod
    def filter_sufix(self, file_list, suffix=None, file_dir=None):
        result = {}
        for file_name in file_list:
            for sf in suffix:
                if file_name.endswith(sf):
                    file_path = os.path.join(file_dir, file_name)
                    count = count + 1
                    sf = sf + str(count)
                    result.update({sf: file_path})
        return result

    @staticmethod
    def filter_prefix(file_dir: str = None, prefix: list = None):
        result = {}
        count = 0
        if file_dir is None:
            p = os.getcwd()
            file_list = os.listdir(p)
        else:
            file_list = os.listdir(file_dir)
        if prefix is not None:
            for file_name in file_list:
                for pf in prefix:
                    if file_name.startswith(pf):
                        file_path = os.path.join(file_dir, file_name)
                        count = count + 1
                        pf = pf + str(count)
                        result.update({pf: file_path})
            return result
        elif prefix is None:
            for file_name in file_list:
                file_path = os.path.join(file_dir, file_name)
                count = count + 1
                file_path = file_path + str(count)
                result.update({file_name: file_path})
            return result

    @staticmethod
    def filter_suffix(file_dir: str = None, suffix: list = None):
        result = {}
        count = 0
        if file_dir is None:
            p = os.getcwd()
            file_list = os.listdir(p)
        else:
            file_list = os.listdir(file_dir)
        if suffix is not None:
            for file_name in file_list:
                for sf in suffix:
                    if file_name.endswith(sf):
                        file_path = os.path.join(file_dir, file_name)
                        count = count + 1
                        sf = sf + str(count)
                        result.update({sf: file_path})
            return result
        elif suffix is None:
            for file_name in file_list:
                file_path = os.path.join(file_dir, file_name)
                count = count + 1
                file_path = file_path + str(count)
                result.update({file_name: file_path})
            return result


ff = FilesFilter()
re_list = ff.filter_prefix("/Users/wangjiping/PycharmProjects/copyer/IconRequest-20221001_122347",
                           prefix=["icon", "app"])
re_list2 = ff.filter_suffix("/Users/wangjiping/PycharmProjects/copyer/IconRequest-20221001_122347")
# ff.filter_prefix("/Users/wangjiping/PycharmProjects/copyer/IconRequest-20221001_122347", prefix=("app", "lof"))
print(re_list)
print(re_list2)
