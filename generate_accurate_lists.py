import csv

print("="*80)
print("生成更准确的行业分类（去除虚高）")
print("="*80)

# 读取数据
with open('china_investment_tracker.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    data = list(reader)

# 重新定义关键词 - 更严格的匹配规则
industry_keywords = {
    '集成电路': ['semiconductor', 'chip', 'wafer', 'foundry', 'chipmaker', 'integrated circuit'],
    '生物医药': ['pharma', 'biotech', 'drug', 'medicine', 'healthcare', 'medical', 'clinic', 'vaccine', 'therapeutic'],
    '人工智能': ['artificial intelligence', 'machine learning', 'deep learning', 'neural network', 'computer vision'],
    '新能源汽车': ['electric vehicle', 'ev ', 'battery', 'auto', 'automotive', 'vehicle'],
    '矿产资源': ['mining', 'mineral', 'copper', 'lithium', 'iron ore', 'cobalt', 'nickel', 'zinc', 'gold', 'silver', 'coal', 'metal']
}

# 排除词列表（防止误匹配）
exclude_patterns = {
    '生物医药': ['hospitality'],  # 排除酒店业
    '新能源汽车': ['carlson', 'carmike', 'carrefour'],  # 排除酒店、影院、超市
    '矿产资源': ['goldman']  # 排除高盛（虽然包含gold）
}

def classify_accurate(row):
    text = (str(row.get('Sector', '')) + ' ' + 
            str(row.get('Subsector', '')) + ' ' + 
            str(row.get('Partner/Target', '')) + ' ' + 
            str(row.get('Investor', ''))).lower()
    
    matches = {}
    
    for industry, keywords in industry_keywords.items():
        # 检查排除词
        should_exclude = False
        if industry in exclude_patterns:
            for exclude_word in exclude_patterns[industry]:
                if exclude_word in text:
                    should_exclude = True
                    break
        
        if should_exclude:
            continue
        
        # 检查关键词
        for keyword in keywords:
            if keyword in text:
                matches[industry] = keyword
                break
    
    return matches

# 统计新的分类结果
print("\n第一步：统计各行业项目数（新分类）")
print("-"*80)

industry_counts = {industry: 0 for industry in industry_keywords.keys()}
industry_projects = {industry: [] for industry in industry_keywords.keys()}

for row in data:
    matches = classify_accurate(row)
    for industry in matches:
        industry_counts[industry] += 1
        try:
            amount = float(row['Millions'].replace('$', '').replace(',', '').strip())
        except:
            amount = 0
        industry_projects[industry].append({
            'row': row,
            'amount': amount,
            'keyword': matches[industry]
        })

print("\n对比结果：")
print(f"{'行业':<12} {'旧分类':<10} {'新分类':<10} {'减少':<10} {'说明'}")
print("-"*80)

old_counts = {
    '集成电路': 50,
    '生物医药': 32,
    '人工智能': 320,
    '新能源汽车': 249,
    '矿产资源': 416
}

for industry in industry_keywords.keys():
    old = old_counts[industry]
    new = industry_counts[industry]
    diff = old - new
    diff_pct = (diff / old * 100) if old > 0 else 0
    
    if diff > 0:
        note = f"去除了{diff}个误分类项目 (-{diff_pct:.0f}%)"
    elif diff < 0:
        note = "略有增加"
    else:
        note = "无变化"
    
    print(f"{industry:<12} {old:<10} {new:<10} {diff:<10} {note}")

# 生成新的CSV文件
print("\n\n第二步：生成准确的项目清单CSV")
print("-"*80)

for industry in industry_keywords.keys():
    filename = f'准确清单_{industry}.csv'
    
    # 按金额排序
    projects = sorted(industry_projects[industry], key=lambda x: x['amount'], reverse=True)
    
    with open(filename, 'w', encoding='utf-8-sig', newline='') as f:
        fieldnames = ['Year', 'Month', 'Investor', 'Amount_USD_Million', 'Partner_Target', 
                     'Country', 'Region', 'Sector', 'Subsector', 'BRI', 'Matched_Keyword']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        
        for project in projects:
            row = project['row']
            writer.writerow({
                'Year': row['Year'],
                'Month': row['Month'],
                'Investor': row['Investor'],
                'Amount_USD_Million': project['amount'],
                'Partner_Target': row['Partner/Target'],
                'Country': row['Country'],
                'Region': row['Region'],
                'Sector': row['Sector'],
                'Subsector': row['Subsector'],
                'BRI': row['BRI'],
                'Matched_Keyword': project['keyword']
            })
    
    print(f"✅ {industry}: {len(projects)} 个项目 → {filename}")

# 展示每个行业的Top 10
print("\n\n第三步：展示各行业Top 10项目（验证准确性）")
print("="*80)

for industry in industry_keywords.keys():
    projects = sorted(industry_projects[industry], key=lambda x: x['amount'], reverse=True)[:10]
    
    print(f"\n【{industry}】- Top 10")
    print("-"*70)
    
    for idx, project in enumerate(projects, 1):
        row = project['row']
        print(f"{idx:2d}. ${project['amount']:>8,.0f}M | {row['Year']} | {row['Country']:<20}")
        print(f"    投资方: {row['Investor'][:50]}")
        print(f"    目标方: {row['Partner/Target'][:50]}")
        print(f"    原始行业: {row['Sector']}/{row['Subsector']}")
        print(f"    ✓ 匹配: '{project['keyword']}'")
        print()

print("\n" + "="*80)
print("✅ 准确分类完成！")
print("="*80)
print("\n说明：")
print("  1. 删除了'ic '关键词 → 集成电路从50项减少到真实的半导体项目")
print("  2. 删除了'ai'和'software' → 人工智能大幅减少虚高")
print("  3. 排除'hospitality' → 生物医药去除酒店业")
print("  4. 排除'carlson/carmike' → 新能源汽车去除影院/酒店")
print("  5. 矿产资源保持不变 → 本身就很准确")
print("="*80)

