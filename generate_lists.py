import csv

# 读取数据
with open('china_investment_tracker.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    data = list(reader)

# 定义关键词
industry_keywords = {
    '集成电路': ['semiconductor', 'chip', 'ic ', 'integrated circuit', 'wafer', 'foundry', 'chipmaker'],
    '生物医药': ['pharma', 'biotech', 'drug', 'medicine', 'healthcare', 'medical', 'hospital', 'clinic', 'vaccine', 'therapeutic'],
    '人工智能': ['ai', 'artificial intelligence', 'machine learning', 'deep learning', 'software'],
    '新能源汽车': ['electric vehicle', 'ev ', 'battery', 'auto', 'automotive', 'car', 'vehicle', 'byd'],
    '矿产资源': ['mining', 'mineral', 'copper', 'lithium', 'iron ore', 'cobalt', 'nickel', 'zinc', 'gold', 'silver', 'coal', 'metal']
}

def classify_and_explain(row):
    text = (str(row.get('Sector', '')) + ' ' + 
            str(row.get('Subsector', '')) + ' ' + 
            str(row.get('Partner/Target', '')) + ' ' + 
            str(row.get('Investor', ''))).lower()
    
    matches = {}
    for industry, keywords in industry_keywords.items():
        for keyword in keywords:
            if keyword in text:
                matches[industry] = keyword
                break
    return matches

# 为每个行业生成CSV
for industry in industry_keywords.keys():
    filename = f'项目清单_{industry}.csv'
    
    with open(filename, 'w', encoding='utf-8-sig', newline='') as f:
        fieldnames = ['Year', 'Month', 'Investor', 'Amount_USD_Million', 'Partner_Target', 
                     'Country', 'Region', 'Sector', 'Subsector', 'BRI', 'Matched_Keyword']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        
        # 收集该行业的所有项目
        projects = []
        for row in data:
            matches = classify_and_explain(row)
            if industry in matches:
                try:
                    amount = float(row['Millions'].replace('$', '').replace(',', '').strip())
                except:
                    amount = 0
                
                projects.append({
                    'Year': row['Year'],
                    'Month': row['Month'],
                    'Investor': row['Investor'],
                    'Amount_USD_Million': amount,
                    'Partner_Target': row['Partner/Target'],
                    'Country': row['Country'],
                    'Region': row['Region'],
                    'Sector': row['Sector'],
                    'Subsector': row['Subsector'],
                    'BRI': row['BRI'],
                    'Matched_Keyword': matches[industry]
                })
        
        # 按金额排序
        projects.sort(key=lambda x: x['Amount_USD_Million'], reverse=True)
        
        # 写入文件
        for project in projects:
            writer.writerow(project)
    
    print(f"✅ {industry}: {len(projects)} 个项目 → {filename}")

print("\n✅ 所有CSV文件已生成！")
