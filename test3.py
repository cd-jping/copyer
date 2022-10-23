import xml.dom.minidom as minidom

file = "/Users/wangjiping/PycharmProjects/copyer/IconRequest-20221001_122347/appfilter_20220922_115417.xml"

xml = open(file, "r", encoding="utf-8")
# line_list = xml.readlines()
# for line_item in line_list:
if "working" in xml:
    print("yes")
    # print(line_item)
# print(line_list)
