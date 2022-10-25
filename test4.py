
import os
pro_dict = {'icon_pack1': '/Users/wangjiping/Downloads/demo/src/res/values/icon_pack.xml', 'appfilter2': '/Users/wangjiping/Downloads/demo/src/res/xml/appfilter.xml', 'appmap3': '/Users/wangjiping/Downloads/demo/src/res/xml/appmap.xml', 'appfilter4': '/Users/wangjiping/Downloads/demo/src/assets/appfilter.xml'}
for k, v in pro_dict.items():
    if "appfilter" in k:
        print(pro_dict[k])

