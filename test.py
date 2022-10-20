
import lxml.etree as et

file = "/Users/wangjiping/PycharmProjects/copyer/IconRequest-20221001_122347/appfilter_20221001_122347.xml"
xml_tree = et.parse(file)
xml_root = xml_tree.getroot()
xml_root.
print(xml_root)