import os


class FilterFiles:
    def filter_files(self, file_dir: str = None, keywords=None, prefix:list = None, suffix:list = None):
        result = {}
        count = 0
        if file_dir is None:
            p = os.getcwd()
            file_list = os.listdir(p)
        else:
            file_list = os.listdir(file_dir)

        if prefix or suffix or keywords is not None:
            for file_name in file_list:









                for kw in keywords:
                    if file_name.find(kw):
                        file_path = os.path.join(file_dir, file_name)
                        count = count + 1
                        kw = kw + str(count)
                        result.update({kw: file_path})
                    for sf in  suffix:
                        for pf in prefix:

                            elif file_name.find(sf):

                            # elif file_path.endswith(sf):
