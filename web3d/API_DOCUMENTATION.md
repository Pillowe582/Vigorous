# Vigorous 3D API Documentation

## 概述

本文档详细介绍了 Vigorous 项目的 RESTful API 接口，基于 Django REST Framework 构建，为前端 React 应用提供完整的数据交互能力。

**若有冲突，以群里发的word为准**

## 认证方式

所有 API 接口都需要用户认证，使用 Django 的 Session Authentication。

### 请求头示例
```javascript
{
  'Content-Type': 'application/json',
  'X-CSRFToken': 'your_csrf_token_here'
}
```

## API 端点概览

### 1. 项目管理 (Projects)
- **Base URL**: `/api/projects/`
- **权限**: 仅限认证用户访问自己的项目

#### 获取项目列表
```http
GET /api/projects/
```

**查询参数**:
- `status`: 项目状态筛选 (`editable`, `protected`, `archived`)
- `search`: 搜索项目名称或描述
- `ordering`: 排序字段 (`created_at`, `edited_at`, `name`)

**响应示例**:
```json
[
  {
    "id": 1,
    "name": "我的第一个3D项目",
    "description": "这是一个测试项目",
    "status": "editable",
    "feature": {"shape": "square", "size": 10},
    "project_tags": ["测试", "demo"],
    "created_at": "2024-01-01T10:00:00Z",
    "edited_at": "2024-01-01T10:00:00Z",
    "pieces": [
      {
        "id": 1,
        "name": "立方体",
        "parts": {"geometry": "cube"},
        "feature": {"shape": "square", "size": 5}
      }
    ]
  }
]
```

#### 创建项目
```http
POST /api/projects/
```

**请求体**:
```json
{
  "name": "新项目名称",
  "description": "项目描述",
  "status": "editable",
  "feature": {"shape": "square", "size": 10},
  "project_tags": ["标签1", "标签2"]
}
```

#### 获取项目详情及棋子
```http
GET /api/projects/{id}/
GET /api/projects/{id}/pieces/
```

### 2. 棋子管理 (Pieces)
- **Base URL**: `/api/pieces/`
- **权限**: 仅限认证用户访问自己的棋子

#### 获取棋子列表
```http
GET /api/pieces/
```

**查询参数**:
- `project_id`: 按项目筛选
- `type`: 按类型筛选
- `search`: 搜索名称或描述
- `ordering`: 排序字段

#### 创建棋子
```http
POST /api/pieces/
```

**请求体**:
```json
{
  "name": "新棋子",
  "description": "棋子描述",
  "parts": {"geometry": "sphere", "parameters": {}},
  "feature": {"shape": "circle", "size": 8},
  "piece_tags": ["球体"],
  "project_id": 1,
  "preset": null
}
```

### 3. 纹理管理 (Textures)
- **Base URL**: `/api/textures/`
- **权限**: 仅限认证用户访问自己的纹理

#### 上传纹理
```http
POST /api/textures/upload/
```

**表单数据**:
```
name: 纹理名称
file: 纹理文件
texture_tags: ["标签1", "标签2"]
source: "upload"
composition: {}
```

#### 获取纹理列表
```http
GET /api/textures/
```

### 4. 预设管理 (Presets)
- **Base URL**: `/api/presets/`
- **权限**: 仅限认证用户访问自己的预设

#### 复制预设为棋子
```http
POST /api/presets/{id}/duplicate/
```

**请求体**:
```json
{
  "project_id": 1
}
```

## 响应格式

### 成功响应
```json
{
  "id": 1,
  "name": "资源名称",
  "...": "其他字段"
}
```

### 列表响应
```json
{
  "count": 10,
  "next": "下一页URL",
  "previous": "上一页URL",
  "results": [...]
}
```

### 错误响应
```json
{
  "detail": "错误信息"
}
```

或字段验证错误：
```json
{
  "field_name": ["错误信息1", "错误信息2"]
}
```

## 状态码说明

- `200 OK`: 请求成功
- `201 Created`: 资源创建成功
- `204 No Content`: 删除成功
- `400 Bad Request`: 请求参数错误
- `401 Unauthorized`: 未认证
- `403 Forbidden`: 权限不足
- `404 Not Found`: 资源不存在

## 前端集成示例

### JavaScript/Fetch 示例
```javascript
// 获取项目列表
async function getProjects() {
  const response = await fetch('/api/projects/', {
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCookie('csrftoken')
    },
    credentials: 'same-origin'
  });
  return await response.json();
}

// 创建新项目
async function createProject(projectData) {
  const response = await fetch('/api/projects/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCookie('csrftoken')
    },
    credentials: 'same-origin',
    body: JSON.stringify(projectData)
  });
  return await response.json();
}

// 辅助函数获取CSRF token
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
```

### React Hook 示例
```javascript
import { useState, useEffect } from 'react';

function useProjects() {
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchProjects();
  }, []);

  const fetchProjects = async () => {
    try {
      const response = await fetch('/api/projects/');
      const data = await response.json();
      setProjects(data);
    } catch (error) {
      console.error('获取项目失败:', error);
    } finally {
      setLoading(false);
    }
  };

  const createProject = async (projectData) => {
    const response = await fetch('/api/projects/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken')
      },
      credentials: 'same-origin',
      body: JSON.stringify(projectData)
    });
    const newProject = await response.json();
    setProjects(prev => [...prev, newProject]);
    return newProject;
  };

  return { projects, loading, createProject };
}
```

## 注意事项

1. **认证**: 所有请求必须在用户登录状态下进行
2. **CSRF保护**: POST/PUT/PATCH/DELETE 请求需要包含 CSRF token
3. **数据所有权**: 用户只能访问和操作自己创建的资源
4. **文件上传**: 纹理上传使用 multipart/form-data 格式
5. **分页**: 列表接口默认每页显示 20 条记录
6. **排序**: 支持多种字段排序，使用 `-` 前缀表示降序

## 错误处理

建议在前端实现统一的错误处理机制：

```javascript
const handleApiError = async (response) => {
  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.detail || '请求失败');
  }
  return response;
};
```