README.md
# Vigorous 衡有锦深！

这是一个基于 Django 框架的 Web 应用程序，由于目前没有新的idea，暂时先按照3d赛道开发
### 3D赛道具体信息

本次比赛的最佳3d奖将作为单独赛道，需要大家针对以下题目进行开发：

"万物皆可自定义"——基于Web/移动端的轻量化3D模型生成器
核心要求： 选择一个具体的使用场景（如手机壳、键帽、收纳盒等），构建一个轻量化的3D建模工具，允许普通用户通过简单的几何叠加、参数修改或AI生成，快速创作出具有功能性的3D实体。

产品形式可以参考MakerWorld的花瓶生成器（https://makerworld.com.cn/makerlab/makeMyVase）、灯罩生成器（https://makerworld.com.cn/makerlab/makeMyLantern）等。


其余最佳类奖项不受影响。
所有的最佳类奖项和一二三等奖可以重复获得。

## 开发相关
- 首先是服务器网站的ip：http://8.141.101.177:8000/
- 建议把源代码 clone 到本地开发。安装各种所需库后，运行 `python manage.py runserver` 即可在本地类似127.0.0.1:8000的地址启动一个服务器，可以预览当前网页
- 开发建议开一个新branch，如果需要把分支开发的内容挂到服务器上，就把那个分支合并到主分支。每当主分支有commit，github的webhook就会自动让服务器拉取main分支的最新代码并刷新网页（理论如此）。
- 具体的架构和之后的流程都还没想好，咱们集思广益，然后慢慢学罢（虽然只剩一个月就开始决赛了
- 以下内容为ai编写，我也看不懂，要用的时候只能"帮帮我，ai先生"了

## 项目结构

### 项目根目录
- [manage.py] - Django 项目的管理脚本，用于执行各种开发和部署任务（如启动服务器、应用迁移等）
- [README.md] - 项目说明文档
- [pr_request_template.md] - Pull Request 请求模板，用于规范代码提交流程（其实想pr就pr）

### 主应用目录 (`config/`)
主 Django 配置应用，包含核心配置文件：

- [\_\_init\_\_.py] - Python 包初始化文件
- [asgi.py] - ASGI 配置文件，用于异步 Web 服务
- [settings.py] - 项目的主要设置和配置文件
- [urls.py] - 项目 URL 路由配置
- [wsgi.py] - WSGI 配置文件，用于部署到生产环境

### 用户账户模块 (`accounts/`)
用户管理系统模块：

- [\_\_init\_\_.py] - Python 包初始化文件
- [admin.py] - Django 管理后台配置
- [apps.py] - 应用配置文件
- [models.py] - 用户数据模型定义
- [tests.py] - 单元测试代码
- [views.py] - 用户相关的视图函数或类
- [migrations/] - 数据库迁移文件目录
  - [\_\_init\_\_.py] - 迁移包初始化文件

### 3D Web 应用模块 (`web3d/`)
这是项目的核心功能模块，专门处理 3D 相关功能：

- [\_\_init\_\_.py] - Python 包初始化文件
- [migrations/] - 数据库迁移文件目录
  - [0001_initial.py] - 初始化迁移文件
  - [\_\_init\_\_.py] - 迁移包初始化文件
- [templates/web3d/] - 3D相关模板文件，用于生成网页内容
  - [editor.html] - 3D编辑器页面模板
  - [home.html] - 3D主页模板
- [admin.py] - Django 管理后台配置
- [apps.py] - 应用配置文件
- [models.py] - 3D相关数据模型定义
- [tests.py] - 单元测试代码
- [urls.py] - 3D 模块的 URL 路由配置
- [views.py] - 视图函数或类，处理请求和响应（目前的主页面就是这个显示的）

### 静态文件目录 (`staticfiles/`)
存放所有静态资源文件（这个似乎会由服务器自动生成，暂时不用动）

#### 管理后台静态文件 (`staticfiles/admin/`)
- CSS 样式文件 (`css/`) - 包含 Django 管理后台的各种样式表
  - [autocomplete.css] - 自动完成组件样式
  - [base.css] - 基础样式
  - [changelists.css] - 变更列表样式
  - [dark_mode.css] - 暗色模式样式
  - [dashboard.css] - 仪表盘样式
  - [forms.css] - 表单样式
  - [login.css] - 登录页面样式
  - [nav_sidebar.css] - 导航侧边栏样式
  - [responsive.css] - 响应式布局样式
  - [rtl.css] - 右到左语言支持样式
  - [widgets.css] - 小部件样式
  - 等其他样式文件

- 图片文件 (`img/`) - 存放管理后台使用的图片资源
- JavaScript 文件 (`js/`) - 存放管理后台的 JavaScript 功能脚本
  - [admin/] - 管理后台专用 JS 脚本
  - 其他通用 JS 脚本，如 [autocomplete.js]、[actions.js] 等

### 项目文档文件
- [pr_request_template.md] - Pull Request 请求模板，用于规范代码提交流程（其实想pr就pr）

## 功能特点

此项目专注于提供 3D 建模解决方案，可能包括 3D 渲染、WebGL 支持、3D 模型展示、简单的在线3D建模等功能。通过 [web3d] 应用来实现核心 3D 功能，并使用 Django 提供稳定的后端支持。

## 安装与运行

1. 确保已安装 Python 和 Django
2. 使用 [manage.py] 进行项目初始化和管理

## 技术栈

- 后端：Python + Django
- 前端：HTML/CSS/JavaScript
- 3D 功能：可能使用 Three.js 或 WebGL 等技术