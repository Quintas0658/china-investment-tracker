#!/bin/bash

# Belt and Road Investment Tracker - Git初始化脚本
echo "🚀 开始初始化Git仓库..."

# 进入项目目录
cd /Users/qrebecca/china_investment_tracker

# 检查是否已经初始化
if [ -d ".git" ]; then
    echo "⚠️  Git仓库已存在！"
    echo "📊 当前状态："
    git status
    exit 0
fi

# 初始化git
echo "📦 初始化Git仓库..."
git init

# 检查git配置
if ! git config user.name > /dev/null 2>&1; then
    echo ""
    echo "⚙️  需要配置Git用户信息"
    echo "请输入你的名字："
    read username
    git config user.name "$username"
    echo "请输入你的邮箱："
    read useremail
    git config user.email "$useremail"
fi

# 添加所有文件
echo "📝 添加文件..."
git add .

# 第一次提交
echo "💾 提交文件..."
git commit -m "Initial commit: Belt and Road Investment Tracker"

echo ""
echo "✅ Git仓库初始化完成！"
echo ""
echo "📋 下一步："
echo "1. 在GitHub创建新仓库: https://github.com/new"
echo "   - 仓库名建议: china-investment-tracker"
echo "   - 不要勾选任何初始化选项"
echo ""
echo "2. 创建后，运行以下命令（替换YOUR_USERNAME为你的GitHub用户名）："
echo "   git remote add origin https://github.com/YOUR_USERNAME/china-investment-tracker.git"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "3. 推送成功后，访问 https://share.streamlit.io/ 部署应用"
echo ""
echo "📖 详细步骤请查看: DEPLOYMENT_STEPS_CN.md"
echo ""

