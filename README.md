# simpledu
## 基于Flask开发框架，开发了一个具有在线浏览课程文档、教学视频和直播功能的教育网站
* 基于Scrapy爬虫框架，爬取了实验楼网站的部分课程信息，完成了部分课程内容的采集
* 基于video.js实现了视频的在线点播；基于flv.js实现了视频直播功能
* 基于WebSockets和redis的pubsub系统实现了直播中实时聊天、新连接提醒和后台发送系统消息功能
* 基于Nginix+Gunicorn完成了项目部署
