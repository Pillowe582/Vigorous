README.md
# Vigorous 衡有锦深！

> ### 注：该Readme为极早期时的版本，尚未更新。此处为一些项目与仓库的基本信息。
> - 这里是后端仓库，直接与[服务器](http://8.141.101.177:8000/)对接。
> - 前端仓库见[这里](https://github.com/Danieltoraji/Vigorous-React-Three-Fiber-Part)（虽然好像还是private）
> - 前端React项目会定期打包并同步到本仓库

这是一个基于 Django 框架的 Web 应用程序，由于目前没有新的idea，暂时先按照3d赛道开发
### 3D赛道具体信息

本次比赛的最佳3d奖将作为单独赛道，需要大家针对以下题目进行开发：

"万物皆可自定义"——基于Web/移动端的轻量化3D模型生成器
核心要求： 选择一个具体的使用场景（如手机壳、键帽、收纳盒等），构建一个轻量化的3D建模工具，允许普通用户通过简单的几何叠加、参数修改或AI生成，快速创作出具有功能性的3D实体。

产品形式可以参考MakerWorld的[花瓶生成器](https://makerworld.com.cn/makerlab/makeMyVase)、[灯罩生成器](https://makerworld.com.cn/makerlab/makeMyLantern)等。


其余最佳类奖项不受影响。
所有的最佳类奖项和一二三等奖可以重复获得。

## 开发相关
- 首先是服务器网站的ip：http://8.141.101.177:8000/
- 建议把源代码 clone 到本地开发。安装各种所需库后，运行 `python manage.py runserver` 即可在本地类似127.0.0.1:8000的地址启动一个服务器，可以预览当前网页。如果本地服务器无法运行，可以尝试`python manage.py migrate`
- 开发建议开一个新branch，如果需要把分支开发的内容挂到服务器上，就把那个分支合并到主分支。每当主分支有commit，github的webhook就会自动让服务器拉取main分支的最新代码并刷新网页（理论如此）。
- 具体的架构和之后的流程都还没想好，咱们集思广益，然后慢慢学罢（虽然只剩一个月就开始决赛了
- https://github.com/Danieltoraji/Vigorous-React-Three-Fiber-Part   这是我们的React前端项目的仓库。里面包含了我们的3D模型生成器的前端代码。

## 简易版本的项目结构
- 首先是根目录下的文件。
  - [manage.py] - Django 项目的管理脚本，用于执行各种开发和部署任务（主要用来migrate和runserver）
  - [requirements.txt] - 项目依赖包列表。当你的开发需要用到新的库，请在这个文件中添加，服务器会自动安装里面提到的库。
- 然后是config目录，这里面装的是项目的主要配置文件。其中settings.py是项目的主要配置文件，其他的文件是辅助配置文件。
- 然后是static目录，这里面装的是项目的静态文件。**我们会在里面存放React前端项目编译之后产生的文件（包括index.html,vite.svg,/assets目录）**。日后有图片等静态文件，也会放在这里。
- 然后是我们的两个主要应用模块：
  - [accounts/] - 用户账户模块，处理用户注册、登录、个人资料等功能
  - [web3d/] - 3D Web 应用模块，主要负责 3D 相关功能的实现
  每个应用内部的结构都是一样的。
  - urls.py负责将应用的URL路由到对应的视图函数或类，交由views.py处理。
  - views.py负责处理具体的业务逻辑，是后端请求的处理中心。这种处理既包括对数据库的读写，也包括渲染制定的HTML模板。于是：
  - models.py负责定义数据库模型。
  - templates/目录负责存放HTML模板文件。

具体的业务逻辑我没想明白。
- 以下内容为ai编写，我也看不懂，要用的时候只能"帮帮我，ai先生"了

## 项目结构

### 项目根目录
- [manage.py] - Django 项目的管理脚本，用于执行各种开发和部署任务（如启动服务器、应用迁移等）
- [README.md] - 项目说明文档
- [pr_request_template.md] - Pull Request 请求模板，用于规范代码提交流程（其实想pr就pr）
- [requirements.txt] - 项目依赖包列表，服务器会自动安装，所以需要新的库可以随便加
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
- [messages.py] - 用户消息处理模块
- [models.py] - 用户数据模型定义
- [tests.py] - 单元测试代码
- [urls.py] - 账户模块的 URL 路由配置
- [views.py] - 用户相关的视图函数或类
- [templates/accounts/] - 账户相关模板文件
  - [login.html] - 用户登录页面
  - [profile.html] - 用户个人资料页面
  - [register.html] - 用户注册页面
- [static/accounts/css/] - 账户模块CSS样式文件
  - [login.css] - 登录页面样式
  - [profile.css] - 个人资料页面样式
  - [register.css] - 注册页面样式

### 3D Web 应用模块 (`web3d/`)
这是项目的核心功能模块，专门处理 3D 相关功能：

- [\_\_init\_\_.py] - Python 包初始化文件
- [admin.py] - Django 管理后台配置
- [apps.py] - 应用配置文件
- [models.py] - 3D相关数据模型定义
- [tests.py] - 单元测试代码
- [urls.py] - 3D 模块的 URL 路由配置
- [views.py] - 视图函数或类，处理请求和响应（目前的主页面就是这个显示的）
- [templates/web3d/] - 3D相关模板文件，用于生成网页内容
  - [editor.html] - 3D编辑器页面模板
  - [home.html] - 3D主页模板
  - [model.html] - 3D模型展示页面模板
- [static/homepage/css/] - 主页CSS样式文件
  - [style.css] - 主页样式文件

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

### 环境要求
- Python 3.6+
- pip 包管理器

### 安装步骤
1. 克隆项目到本地：
   ```bash
   git clone <repository-url>
   cd Vigorous
   ```

2. 创建虚拟环境（推荐）：
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Linux/Mac
   source venv/bin/activate
   ```

3. 安装依赖包：
   ```bash
   pip install Django djangorestframework gunicorn numpy python-decouple
   ```

4. 数据库迁移：
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. 收集静态文件：
   ```bash
   python manage.py collectstatic
   ```

6. 启动开发服务器：
   ```bash
   python manage.py runserver
   ```

7. 访问应用：
   在浏览器中打开 `http://127.0.0.1:8000/`

### 生产部署
- 使用 Gunicorn 作为 WSGI 服务器
- 配置 Webhook 实现自动化部署
- 服务器地址：http://8.141.101.177:8000/

## 技术栈

- 后端：Python + Django
- API支持：djangorestframework
- 生产部署：gunicorn
- 配置管理：python-decouple
- 数学计算：numpy
- 前端：HTML/CSS/JavaScript
- 3D 功能：计划使用 Three.js 或 WebGL 等技术