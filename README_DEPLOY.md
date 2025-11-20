# 🚀 部署指南 / Deployment Guide

## 📋 部署到 Streamlit Community Cloud

### 前置要求：
1. GitHub 账号
2. Streamlit Community Cloud 账号（使用GitHub登录）

---

## 🔧 部署步骤

### Step 1: 初始化 Git 仓库

在项目目录中运行：

```bash
cd /Users/qrebecca/china_investment_tracker

# 初始化 git
git init

# 添加所有文件
git add .

# 第一次提交
git commit -m "Initial commit: China Investment Tracker Streamlit App"
```

### Step 2: 创建 GitHub 仓库

1. 访问 https://github.com/new
2. 创建新仓库，例如：`china-investment-tracker`
3. **不要**勾选 "Initialize with README"
4. 点击 "Create repository"

### Step 3: 推送到 GitHub

复制GitHub提供的命令，例如：

```bash
# 添加远程仓库（替换为你的GitHub用户名）
git remote add origin https://github.com/YOUR_USERNAME/china-investment-tracker.git

# 推送到main分支
git branch -M main
git push -u origin main
```

### Step 4: 部署到 Streamlit Cloud

1. 访问 https://share.streamlit.io/
2. 使用GitHub账号登录
3. 点击 "New app"
4. 选择：
   - **Repository**: `YOUR_USERNAME/china-investment-tracker`
   - **Branch**: `main`
   - **Main file path**: `app.py`
5. 点击 "Deploy!"

等待几分钟，你的应用就会部署完成！🎉

---

## 🌐 访问应用

部署完成后，你会得到一个公开的URL，类似：
```
https://YOUR_USERNAME-china-investment-tracker-app-xxxxxx.streamlit.app
```

任何人都可以通过这个链接访问，无需登录！

---

## 🔄 更新应用

当你修改代码后，只需要：

```bash
git add .
git commit -m "Update: 描述你的更改"
git push
```

Streamlit Cloud 会自动检测到更改并重新部署！

---

## ⚙️ 常见问题

### 1. 数据文件太大？
如果CSV文件很大（>100MB），考虑：
- 使用 Git LFS (Large File Storage)
- 或从外部URL加载数据

### 2. 应用加载慢？
- 添加 `@st.cache_data` 装饰器（已添加）
- 优化数据加载逻辑

### 3. 隐私设置？
- 在 Streamlit Cloud 设置中可以设置应用为私有
- 或添加密码保护

---

## 📞 支持

- Streamlit 文档: https://docs.streamlit.io/
- Streamlit Cloud 文档: https://docs.streamlit.io/streamlit-community-cloud
- 社区论坛: https://discuss.streamlit.io/




