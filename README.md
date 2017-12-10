# handWrite_face_recog
## model1
圈词手写体识别，使用tensorflow构建一个简单的手写体识别Deep Convolutional Network。
字体训练集来自[CASIA Online and Offline Chinese Handwriting Databases](http://www.nlpr.ia.ac.cn/databases/handwriting/Download.html),由模式识别国家重点实验室共享，需要的两个文件分别是，HWDB1.1trn_gnt，[HWDB1.1tst_gnt](http://www.nlpr.ia.ac.cn/databases/download/feature_data/HWDB1.1tst_gnt.zip)，其中HWDB1.1trn_gnt训练集或许是有点问题，下载时要[part1](http://www.nlpr.ia.ac.cn/databases/Download/feature_data/HWDB1.1trn_gnt_P1.zip)与[part2](http://www.nlpr.ia.ac.cn/databases/Download/feature_data/HWDB1.1trn_gnt_P2.zip)部分分开下，单独下载HWDB1.1trn_gnt下载不下来
项目代码参考与[小石头的码疯窝](https://zhuanlan.zhihu.com/p/24698483?refer=burness-DL),训练了一天时间跑了大致1W多的数据集训练出的模型参数.
## model2
输入图片直接进行手写体的识别，缺点，只能进行单个词的识别功能，输入图片的细节处理没有做的很好。
## model
人脸识别课堂点名功能，主要功能通过调用百度人脸识别的api接口调用相关功能，[API接口地址](https://ai.baidu.com/docs#/Face-API/top),[pythonSDK文档](https://ai.baidu.com/docs#/Face-Python-SDK/top),主要调用功能，人脸注册，人脸识别。
