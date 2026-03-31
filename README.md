### 爬虫的基本流程
1. 构建请求信息(url、method、headers、params、data)
2. 发起HTTP/HTTPS请求，获取HTTP/HTTPS响应
3. 解析响应，分析响应数据的数据结构或者页面结构
   - 提取数据
   - 提取请求的地址
4. 对数据进行存储/对新的请求地址重复前面的步骤

![scrapy流程图](docs/source/scrapy流程图.png)
