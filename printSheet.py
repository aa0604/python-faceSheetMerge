# -*- coding:utf-8*-
# 利用PyPDF2模块合并同一文件夹下的所有PDF文件
# 只需修改存放PDF文件的文件夹变量：file_dir 和 输出文件名变量: outfile

import os
from PyPDF2 import PdfFileReader, PdfFileWriter
import time

import pdfkit

import sys
import redis
import json
import platform

reload(sys)  # Python2.5 初始化后会删除 sys.setdefaultencoding 这个方法，我们需要重新载入
sys.setdefaultencoding('utf-8')

outputPages = 0
output = PdfFileWriter()


class printSheet:

    # 使用os模块的walk函数，搜索出指定目录下的全部PDF文件
    # 获取同一目录下的所有PDF文件的绝对路径
    def getFileName(self, filedir):
        file_list = [os.path.join(root, filespath) \
                     for root, dirs, files in os.walk(filedir) \
                     for filespath in files \
                     if str(filespath).endswith('pdf')
                     ]
        return file_list if file_list else []


    def addPage(self, pdf_file):
        global outputPages
        # 读取源PDF文件
        # print('addPage', pdf_file)
        input = PdfFileReader(open(pdf_file, "rb"))
        # 获得源PDF文件中页面总数
        pageCount = input.getNumPages()
        outputPages += pageCount
        # print("页数：%d" % pageCount)

        # 分别将page添加到输出output中
        for iPage in range(pageCount):
            output.addPage(input.getPage(iPage))

    def createPdf(self, content, to_file, width, height):
        '将字符串生成pdf文件'
        # （需下载wkhtmltox）将程序路径传入config对象
        if (platform.system() == 'Windows'):
            config = pdfkit.configuration(wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe")
        else:
            config = pdfkit.configuration(wkhtmltopdf=r"/usr/local/bin/wkhtmltopdf")
        # 生成pdf文件，to_file为文件路径
        options = {
            'page-size': 'Letter',
            'page-width': width,
            'page-height': height,
            'margin-top': '0.05in',
            'margin-left': '0in',
            'margin-right': '0in',
            'margin-bottom': '0.25in',
            'encoding': "UTF-8",

            'no-outline': None,
            'outline-depth': 10,
        }
        html = '<html><head><meta charset="UTF-8"></head><bordy><div style="align: center; margin: 50px auto;"><p>%s</p></div></body></html>' % content
        if not os.path.exists(os.path.dirname(to_file)):
            os.makedirs(os.path.dirname(to_file))
        pdfkit.from_string(html, to_file, options, configuration=config)

    # 创建配货单
    def createDistributionContent(self, list, tracking_number):
        html = '<div style="text-align: right">%s</div>' % tracking_number
        if tracking_number:
            html += '<table  border="1" class="bordersolid textcenter" cellspacing="0" cellpadding="0" style="width:100%;"><tbody>' \
                    '<tr><td style="width:80px;word-break:break-all;">Item</td><td style="width:30px;">Description</td><td style="width:36px;">Price</td><td style="width:26px;">Qty</td></tr>'

        for v in list:
            html += u'<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % (
                v[u'code'], v[u'name'], v[u'unit_price'],
                v[u'qutqty'])

        html += '</tbody></table>'
        return html

    # 主函数
    def create(self, cacheKey):
        global output
        output = PdfFileWriter()
        time1 = time.time()
        file_dir = os.getcwd() + '/../public/'  # 存放PDF的原文件夹

        # 获取转递过来的参数
        red = redis.Redis(host='127.0.0.1', port=6379, db=0)
        temp = red.get(cacheKey)
        if (temp):

            content = json.loads(temp)
            data = content[u'data']
            set = content[u'set']
            width = set[u'width']
            height = set[u'height']

            for k in data:
                print(k)
                continue
                self.addPage(file_dir + data[k][u'print_url'])
                content = self.createDistributionContent(data[k][u'distribution'], data[k][u'tracking_number'])

                filename = file_dir + 'download/temp/distribution-' + data[k][u'code'] + '.pdf'
                self.createPdf(content, filename, width, height)
                self.addPage(filename)

            return;
            # mergePDF(file_dir, outfile)

            # 写入到目标PDF文件
            outfile = file_dir + 'download/' + cacheKey + '.pdf'  # 输出的PDF文件的名称
            outputStream = open(outfile, "wb")
            output.write(outputStream)
            outputStream.close()
            time2 = time.time()
            print('总共耗时：%s s.' % (time2 - time1))
            print('download/' + cacheKey + '.pdf')
            print("ok")
            return 'download/' + cacheKey + '.pdf'
        else :
            print('没有数据')


# print(os.getcwd())


# PS = printSheet();
# result = PS.create('d429f42743dba7e631d637cae0d6e394')
