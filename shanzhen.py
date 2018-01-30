#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 以下结果在 scrapy sell 中运行
#  scrapy shell 'https://www.tensorflow.org/api_docs/' (在scrapy 项目目录下执行）
import json
rlist = response.xpath('//*[@id="gc-wrapper"]/div[2]/nav[1]/ul/li[2]/ul[1]/li')
treemap = {}
for i in rlist:
    # 获取 tf 一级标签

    firstt = i.xpath('./span/text()').extract()
    if firstt:
        firstt = firstt
    else:
        firstt = ["Overview r1"]
    # 获取二级标签
    secondt = i.xpath('./ul/li/a/text()').extract()
    secondta = i.xpath('./ul/li/a/@href').extract()
    if secondt:
        secondt = secondt
        secondta = secondta
    else:
        secondt = "Null"
        secondta = "Null"

    keyvalue = dict(zip(secondt, secondta))

    treemap[firstt[0]] = keyvalue


# 字典写入以json的格式保存到文件
jsObj = json.dumps(treemap)
fileObject = open('json_File.json', 'w')
fileObject.write(jsObj)
fileObject.close()