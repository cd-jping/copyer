import os

find_xml = {}
count = 0
find_name = ["app", "icon_pack"]
for root, dirs, files in os.walk("/Users/WangChunsheng/Downloads/demo"):
    for file in files:
        for f_name in find_name:
            if f_name in file:
                count = count + 1
                # file = os.path.splitext(file)[0]
                # file = file + str(count)
                file_name = file
                file_name = os.path.splitext(file)[0]
                file_name = file_name + str(count)
                file_path = os.path.join(root, file)
                find_xml.update({file_name: file_path})
print(find_xml)
