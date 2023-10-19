# 一些接口整理

## blog.html

### 1. 竞赛列表：数据库
* 竞赛名
* 竞赛简介
* 竞赛详情页的url：跳转时传递 id (需要是加密的 / 安全的传递方法)

### 2. 搜索栏：POST表单
* 基于关键词 / 分类标签

### 3. 新建竞赛：POST表单
* 竞赛名：name
* 来源网站：url
* 相关图片：inputfile
* 参赛人数：number
* 竞赛类别：radio1/2/3
* 报名开始时间：start_regi
* 报名截止时间：end_regi
* 竞赛开始时间：start_compt
* 竞赛简介：intro

## blog-single.html

### 1. 竞赛主页
- [ ] 竞赛信息：数据库
* 竞赛名：name
* 来源网站：url
* 相关图片：inputfile
* 参赛人数：number
* 竞赛类别：radio1/2/3
* 报名开始时间：start_regi
* 报名截止时间：end_regi
* 竞赛开始时间：start_compt
* 竞赛简介：intro

- [ ] 讨论区：已发布的讨论 / 提交讨论：POST表单
* 讨论内容
* 发布时间
* 用户主页

### 2. 组队大厅
- [ ] 队伍列表：数据库
- [ ] 加入队伍：？
- [ ] 搜索栏：POST表单


### 3. 我的团队：数据库

