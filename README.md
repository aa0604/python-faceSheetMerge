# python-faceSheetMerge
python面单配货单生成合并（多线程）

### 功能说明
通过socket通信服务去发送、执行合并pdf的任务

### 流程说明
1、客户端向服务端发送订单数据
2、服务端接收到数据后，将数据json格式化后用redis保存
3、服务端向python的socket（socket在同一服务端）发送redis的key
4、socket接收到这个key之后通过这个key读取redis保存的数据
5、遍历数据，根据数据生成配货单的pdf，然后合并面单pdf
6、socket通知服务端完成打印，返回文件名


### 安装插件
```
pip install PyPDF2
pip install pdfrw
pip install pdfkit
```

### 安装wkhtmltopdf
分为linux 和 windows的安装，请自行百度wkhtmltopdf这两个系统的安装。
windows下安装到c盘的默认位置，否则需要自行修改源码里的位置
config = pdfkit.configuration(wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe")

### 发送的数据示例
键名都是有用的，就不一一翻译了，都是有用的，其中code是订单号
```json
{"data":{"VS1911-1898":{"code":"VS1911-1898","print_url":"download\/20191107163829179106098250.pdf","tracking_number":"179106098250","distribution":[{"code":"ELEA117K14","name":"iJust 3 Kit(WR VERSION) Black Silver 7.5ml","unit_price":27.79,"qutqty":1}]},"VS1911-1897":{"code":"VS1911-1897","print_url":"download\/20191107163829179106095306.pdf","tracking_number":"179106095306","distribution":[{"code":"MAVA027K01","name":"Myvapors MyTri Full kit Black","unit_price":17.31,"qutqty":1}]}}}
```