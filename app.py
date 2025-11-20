import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# Page configuration
st.set_page_config(
    page_title="China Outbound Investment Analysis | 中国对外投资分析",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Language translations
TRANSLATIONS = {
    'en': {
        'title': '🌍 China Outbound Investment Analysis',
        'subtitle': 'Beijing Belt & Road Enterprise Training - Interactive Dashboard',
        'language': 'Language',
        'filters': '🔍 Filters',
        'select_industries': 'Select Industries',
        'target_industries': 'Target Industries',
        'other_sectors': 'Other Sectors',
        'year_range': 'Select Year Range',
        'filter_country': 'Filter by Country (Optional)',
        'amount_range': 'Investment Amount Range',
        'min_amount': 'Min Amount (Million USD)',
        'max_amount': 'Max Amount (Million USD)',
        'overview': '📊 Overview',
        'total_projects': 'Total Projects',
        'total_investment': 'Total Investment',
        'avg_investment': 'Average Investment',
        'countries': 'Countries',
        'tabs': {
            'trends': '📈 Trends',
            'geographic': '🌍 Geographic',
            'concentration': '🎯 Concentration',
            'explorer': '📋 Data Explorer',
            'insights': '💡 Insights'
        },
        'trends_title': 'Investment Trends Over Time',
        'geographic_title': 'Geographic Distribution',
        'select_industry_map': 'Select Industry for Map',
        'top_destinations': 'Top Destinations',
        'concentration_title': 'Investment Concentration Analysis',
        'hhi_title': 'HHI Index by Industry',
        'top3_title': 'Top 3 Countries Share',
        'data_explorer_title': 'Data Explorer',
        'download_btn': '📥 Download Data as CSV',
        'insights_title': 'Key Insights',
        'investment_summary': 'Investment Summary:',
        'risk_assessment': 'Risk Assessment:',
        'high_risk': '⚠️ High concentration - Significant geopolitical risk',
        'med_risk': '→ Medium concentration - Moderate risk level',
        'low_risk': '✓ Low concentration - Diversified risk',
        'top_5_dest': 'Top 5 Destinations:',
        'industries': {
            'Integrated Circuits': 'Integrated Circuits',
            'Biopharmaceuticals': 'Biopharmaceuticals',
            'New Energy Vehicles': 'New Energy Vehicles',
            'Mineral Resources': 'Mineral Resources'
        },
        'chart_labels': {
            'year': 'Year',
            'investment': 'Investment (Million USD)',
            'projects': 'Number of Projects',
            'country': 'Country',
            'amount': 'Investment (Million USD)',
            'hhi': 'HHI Index',
            'share': 'Share (%)'
        }
    },
    'zh': {
        'title': '🌍 中国对外投资分析',
        'subtitle': '北京市一带一路企业培训 - 交互式数据仪表板',
        'language': '语言',
        'filters': '🔍 筛选器',
        'select_industries': '选择行业',
        'target_industries': '重点行业',
        'other_sectors': '其他行业',
        'year_range': '选择年份范围',
        'filter_country': '按国家筛选（可选）',
        'amount_range': '投资金额范围',
        'min_amount': '最小金额（百万美元）',
        'max_amount': '最大金额（百万美元）',
        'overview': '📊 概览',
        'total_projects': '总项目数',
        'total_investment': '总投资额',
        'avg_investment': '平均投资额',
        'countries': '国家数量',
        'tabs': {
            'trends': '📈 趋势分析',
            'geographic': '🌍 地理分布',
            'concentration': '🎯 集中度分析',
            'explorer': '📋 数据浏览器',
            'insights': '💡 关键洞察'
        },
        'trends_title': '投资趋势（按时间）',
        'geographic_title': '地理分布',
        'select_industry_map': '选择行业查看地图',
        'top_destinations': '主要投资目的地',
        'concentration_title': '投资集中度分析',
        'hhi_title': '各行业HHI指数',
        'top3_title': '前三大国家占比',
        'data_explorer_title': '数据浏览器',
        'download_btn': '📥 下载数据为CSV',
        'insights_title': '关键洞察',
        'investment_summary': '投资概况：',
        'risk_assessment': '风险评估：',
        'high_risk': '⚠️ 高度集中 - 地缘政治风险显著',
        'med_risk': '→ 中度集中 - 风险水平适中',
        'low_risk': '✓ 低度集中 - 风险分散',
        'top_5_dest': '前5大投资目的地：',
        'industries': {
            'Integrated Circuits': '集成电路',
            'Biopharmaceuticals': '生物医药',
            'New Energy Vehicles': '新能源汽车',
            'Mineral Resources': '矿产资源'
        },
        'chart_labels': {
            'year': '年份',
            'investment': '投资额（百万美元）',
            'projects': '项目数',
            'country': '国家',
            'amount': '投资额（百万美元）',
            'hhi': 'HHI指数',
            'share': '占比 (%)'
        }
    }
}

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 1rem 0;
    }
    .sub-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #2c3e50;
        margin-top: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        text-align: center;
    }
    .stDownloadButton {
        margin-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Industry definitions (corrected: coal is energy, not mineral; focus on metal minerals)
INDUSTRY_KEYWORDS = {
    'Integrated Circuits': ['semiconductor', 'chip', 'wafer', 'foundry', 'chipmaker', 'integrated circuit'],
    'Biopharmaceuticals': ['pharma', 'biotech', 'drug', 'medicine', 'healthcare', 'medical', 'clinic', 'vaccine', 'therapeutic'],
    'New Energy Vehicles': ['electric vehicle', 'ev ', 'battery', 'auto', 'automotive', 'vehicle'],
    'Mineral Resources': ['mining', 'mineral', 'copper', 'lithium', 'iron ore', 'cobalt', 'nickel', 'zinc', 'rare earth', 'metal']  # Removed: coal (energy), gold/silver (precious metals)
}

EXCLUDE_PATTERNS = {
    'Biopharmaceuticals': ['hospitality'],
    'New Energy Vehicles': ['carlson', 'carmike', 'carrefour'],
    'Mineral Resources': ['goldman', 'coal']  # Exclude coal (energy sector)
}

@st.cache_data
def load_data():
    """Load and process data"""
    df = pd.read_csv('china_investment_tracker.csv')
    
    # Clean amount
    df['Amount'] = df['Millions'].str.replace('$', '', regex=False).str.replace(',', '').str.strip()
    df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce')
    
    return df

def classify_accurate(row):
    """Classify investment by industry"""
    text = (str(row.get('Sector', '')) + ' ' + 
            str(row.get('Subsector', '')) + ' ' + 
            str(row.get('Partner/Target', '')) + ' ' + 
            str(row.get('Investor', ''))).lower()
    
    matches = []
    
    # Check if it matches any target industry
    for industry, keywords in INDUSTRY_KEYWORDS.items():
        should_exclude = False
        if industry in EXCLUDE_PATTERNS:
            for exclude_word in EXCLUDE_PATTERNS[industry]:
                if exclude_word in text:
                    should_exclude = True
                    break
        
        if should_exclude:
            continue
        
        for keyword in keywords:
            if keyword in text:
                matches.append(industry)
                break
    
    # If no match, use original Sector
    if not matches:
        sector = str(row.get('Sector', 'Other')).strip()
        if sector and sector != 'nan' and sector != '':
            matches.append(sector)
        else:
            matches.append('Other')
    
    return matches

@st.cache_data
def process_data(df):
    """Process and classify data"""
    df['Industries'] = df.apply(classify_accurate, axis=1)
    df_expanded = df.explode('Industries')
    df_expanded = df_expanded[df_expanded['Industries'].notna()].copy()
    
    # Get all unique industries
    all_industries = sorted(df_expanded['Industries'].unique())
    
    return df_expanded, all_industries

def calculate_hhi(country_amounts):
    """Calculate HHI index"""
    total = country_amounts.sum()
    if total == 0:
        return 0
    shares = (country_amounts / total * 100)
    hhi = (shares ** 2).sum()
    return hhi

def get_text(lang, key):
    """Get translated text"""
    keys = key.split('.')
    text = TRANSLATIONS[lang]
    for k in keys:
        text = text[k]
    return text

def get_industry_name(lang, industry):
    """Get industry name - translate if target industry, otherwise use original"""
    target_industries = list(INDUSTRY_KEYWORDS.keys())
    if industry in target_industries:
        return get_text(lang, f'industries.{industry}')
    else:
        # For other sectors, return original name (no translation)
        return industry

# Main app
def main():
    # Language selector in sidebar (at the top)
    lang = st.sidebar.selectbox(
        "🌐 Language / 语言",
        options=['zh', 'en'],
        format_func=lambda x: '中文' if x == 'zh' else 'English',
        index=0
    )
    
    # Header
    st.markdown(f'<div class="main-header">{get_text(lang, "title")}</div>', unsafe_allow_html=True)
    st.markdown(f'<div style="text-align: center; color: #7f8c8d; margin-bottom: 2rem;">{get_text(lang, "subtitle")}</div>', unsafe_allow_html=True)
    
    # Load data
    with st.spinner('Loading data...' if lang == 'en' else '加载数据中...'):
        df = load_data()
        df_expanded, all_industries = process_data(df)
    
    # Sidebar filters
    st.sidebar.header(get_text(lang, 'filters'))
    
    # Industry selection - separate target industries and other sectors
    target_industries = list(INDUSTRY_KEYWORDS.keys())
    other_sectors = [ind for ind in all_industries if ind not in target_industries]
    
    # Sort other sectors by frequency (number of projects)
    sector_counts = df_expanded[df_expanded['Industries'].isin(other_sectors)]['Industries'].value_counts()
    other_sectors_sorted = [s for s in sector_counts.index if s in other_sectors]
    
    # Target industries (with translation)
    st.sidebar.markdown(f"**{'🎯 ' + get_text(lang, 'target_industries') if lang == 'zh' else '🎯 Target Industries'}**")
    target_display = [get_text(lang, f'industries.{ind}') for ind in target_industries]
    selected_target_display = st.sidebar.multiselect(
        get_text(lang, 'select_industries'),
        target_display,
        default=target_display,
        key='target_industries'
    )
    
    # Other sectors (no translation needed) - default to top 10 by frequency
    st.sidebar.markdown(f"**{'📊 ' + (get_text(lang, 'other_sectors') if lang == 'zh' else 'Other Sectors')}**")
    default_other = other_sectors_sorted[:10] if len(other_sectors_sorted) > 10 else other_sectors_sorted
    selected_other_sectors = st.sidebar.multiselect(
        get_text(lang, 'select_industries') if lang == 'zh' else 'Select Sectors',
        other_sectors_sorted,  # Show sorted by frequency
        default=default_other,
        key='other_sectors'
    )
    
    # Map display names back to English keys and combine all selections
    display_to_key = {get_text(lang, f'industries.{ind}'): ind for ind in target_industries}
    selected_industries = [display_to_key[d] for d in selected_target_display] + selected_other_sectors
    
    # Year range
    year_min, year_max = int(df['Year'].min()), int(df['Year'].max())
    year_range = st.sidebar.slider(
        get_text(lang, 'year_range'),
        year_min, year_max,
        (year_min, year_max)
    )
    
    # Country filter
    all_countries = sorted(df_expanded['Country'].dropna().unique())
    selected_countries = st.sidebar.multiselect(
        get_text(lang, 'filter_country'),
        all_countries,
        default=[]
    )
    
    # Amount filter
    st.sidebar.subheader(get_text(lang, 'amount_range'))
    min_amount = st.sidebar.number_input(get_text(lang, 'min_amount'), value=0, step=100)
    max_amount = st.sidebar.number_input(get_text(lang, 'max_amount'), value=50000, step=100)
    
    # Apply filters
    filtered_df = df_expanded[
        (df_expanded['Industries'].isin(selected_industries)) &
        (df_expanded['Year'] >= year_range[0]) &
        (df_expanded['Year'] <= year_range[1]) &
        (df_expanded['Amount'] >= min_amount) &
        (df_expanded['Amount'] <= max_amount)
    ]
    
    if selected_countries:
        filtered_df = filtered_df[filtered_df['Country'].isin(selected_countries)]
    
    # Overview metrics
    st.markdown(f'<div class="sub-header">{get_text(lang, "overview")}</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            get_text(lang, 'total_projects'),
            f"{len(filtered_df):,}",
            delta=None
        )
    
    with col2:
        total_investment = filtered_df['Amount'].sum()
        st.metric(
            get_text(lang, 'total_investment'),
            f"${total_investment/1000:.1f}B",
            delta=None
        )
    
    with col3:
        avg_investment = filtered_df['Amount'].mean()
        st.metric(
            get_text(lang, 'avg_investment'),
            f"${avg_investment:.1f}M",
            delta=None
        )
    
    with col4:
        num_countries = filtered_df['Country'].nunique()
        st.metric(
            get_text(lang, 'countries'),
            f"{num_countries}",
            delta=None
        )
    
    # Tabs for different views
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        get_text(lang, 'tabs.trends'),
        get_text(lang, 'tabs.geographic'),
        get_text(lang, 'tabs.concentration'),
        get_text(lang, 'tabs.explorer'),
        get_text(lang, 'tabs.insights')
    ])
    
    with tab1:
        st.markdown(f"### {get_text(lang, 'trends_title')}")
        
        # Time series by industry
        for industry in selected_industries:
            industry_df = filtered_df[filtered_df['Industries'] == industry]
            
            if len(industry_df) == 0:
                continue
            
            yearly = industry_df.groupby('Year').agg({
                'Amount': ['sum', 'count']
            }).reset_index()
            yearly.columns = ['Year', 'Total_Investment', 'Project_Count']
            
            # Create dual-axis chart
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            
            fig.add_trace(
                go.Bar(x=yearly['Year'], y=yearly['Total_Investment'], 
                       name=get_text(lang, 'chart_labels.investment'), marker_color='steelblue'),
                secondary_y=False,
            )
            
            fig.add_trace(
                go.Scatter(x=yearly['Year'], y=yearly['Project_Count'], 
                          name=get_text(lang, 'chart_labels.projects'), mode='lines+markers',
                          marker=dict(size=8, color='red'), line=dict(width=2, color='red')),
                secondary_y=True,
            )
            
            fig.update_xaxes(title_text=get_text(lang, 'chart_labels.year'))
            fig.update_yaxes(title_text=get_text(lang, 'chart_labels.investment'), secondary_y=False)
            fig.update_yaxes(title_text=get_text(lang, 'chart_labels.projects'), secondary_y=True)
            
            industry_name = get_industry_name(lang, industry)
            fig.update_layout(
                title_text=f"{industry_name} - {get_text(lang, 'trends_title')}",
                hovermode='x unified',
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.markdown(f"### {get_text(lang, 'geographic_title')}")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Top countries by industry
            industry_display_options = [get_industry_name(lang, ind) for ind in selected_industries]
            # Build reverse mapping for both target and other industries
            display_to_industry = {get_industry_name(lang, ind): ind for ind in selected_industries}
            industry_select_display = st.selectbox(get_text(lang, 'select_industry_map'), industry_display_options)
            industry_select = display_to_industry[industry_select_display]
            
            industry_df = filtered_df[filtered_df['Industries'] == industry_select]
            
            country_stats = industry_df.groupby('Country').agg({
                'Amount': ['sum', 'count']
            }).reset_index()
            country_stats.columns = ['Country', 'Total_Investment', 'Project_Count']
            country_stats = country_stats.sort_values('Total_Investment', ascending=False).head(15)
            
            fig = px.bar(
                country_stats,
                x='Total_Investment',
                y='Country',
                orientation='h',
                title=f'{industry_select_display} - Top 15',
                labels={'Total_Investment': get_text(lang, 'chart_labels.amount'), 'Country': ''},
                color='Total_Investment',
                color_continuous_scale='Teal'
            )
            fig.update_layout(height=500, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown(f"#### {get_text(lang, 'top_destinations')}")
            for idx, row in country_stats.head(10).iterrows():
                st.markdown(f"""
                **{row['Country']}**  
                💰 ${row['Total_Investment']:,.0f}M  
                📊 {int(row['Project_Count'])} {'projects' if lang == 'en' else '个项目'}
                """)
    
    with tab3:
        st.markdown(f"### {get_text(lang, 'concentration_title')}")
        
        concentration_data = []
        
        for industry in selected_industries:
            industry_df = filtered_df[filtered_df['Industries'] == industry]
            
            if len(industry_df) == 0:
                continue
            
            country_amounts = industry_df.groupby('Country')['Amount'].sum().sort_values(ascending=False)
            total_amount = country_amounts.sum()
            
            if total_amount == 0:
                continue
            
            shares = (country_amounts / total_amount * 100)
            hhi = calculate_hhi(country_amounts)
            top3_share = shares.head(3).sum()
            
            concentration_data.append({
                'Industry': get_industry_name(lang, industry),
                'HHI_Index': round(hhi, 1),
                'Top3_Share_%': round(top3_share, 1),
                'Num_Countries': len(country_amounts),
                'Top_Destination': country_amounts.index[0] if len(country_amounts) > 0 else 'N/A'
            })
        
        if concentration_data:
            conc_df = pd.DataFrame(concentration_data)
            
            col1, col2 = st.columns(2)
            
            with col1:
                fig = px.bar(
                    conc_df,
                    x='Industry',
                    y='HHI_Index',
                    title=get_text(lang, 'hhi_title'),
                    color='HHI_Index',
                    color_continuous_scale='RdYlGn_r',
                    labels={'HHI_Index': get_text(lang, 'chart_labels.hhi'), 'Industry': ''}
                )
                fig.add_hline(y=1000, line_dash="dash", line_color="green", 
                             annotation_text="Low" if lang == 'en' else "低")
                fig.add_hline(y=1800, line_dash="dash", line_color="red",
                             annotation_text="High" if lang == 'en' else "高")
                fig.update_layout(height=400, showlegend=False)
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                fig = px.bar(
                    conc_df,
                    x='Industry',
                    y='Top3_Share_%',
                    title=get_text(lang, 'top3_title'),
                    color='Top3_Share_%',
                    color_continuous_scale='Blues',
                    labels={'Top3_Share_%': get_text(lang, 'chart_labels.share'), 'Industry': ''}
                )
                fig.add_hline(y=50, line_dash="dash", line_color="orange",
                             annotation_text="50%")
                fig.update_layout(height=400, showlegend=False)
                st.plotly_chart(fig, use_container_width=True)
            
            st.dataframe(conc_df, use_container_width=True)
    
    with tab4:
        st.markdown(f"### {get_text(lang, 'data_explorer_title')}")
        
        # Display filtered data
        display_df = filtered_df[[
            'Year', 'Month', 'Industries', 'Investor', 'Amount', 
            'Partner/Target', 'Country', 'Region', 'Sector', 'Subsector'
        ]].sort_values('Amount', ascending=False)
        
        # Translate industry names in display
        if lang == 'zh':
            display_df['Industries'] = display_df['Industries'].apply(
                lambda x: get_industry_name(lang, x)
            )
        
        st.dataframe(display_df, use_container_width=True, height=500)
    
    with tab5:
        st.markdown(f"### {get_text(lang, 'insights_title')}")
        
        for industry in selected_industries:
            industry_df = filtered_df[filtered_df['Industries'] == industry]
            
            if len(industry_df) == 0:
                continue
            
            industry_name = get_industry_name(lang, industry)
            st.markdown(f"#### {industry_name}")
            
            total_inv = industry_df['Amount'].sum()
            num_projects = len(industry_df)
            avg_inv = industry_df['Amount'].mean()
            
            top_country = industry_df.groupby('Country')['Amount'].sum().sort_values(ascending=False)
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"""
                **{get_text(lang, 'investment_summary')}**
                - {'Total Investment' if lang == 'en' else '总投资额'}: **${total_inv:,.0f}M** (${total_inv/1000:.1f}B)
                - {'Number of Projects' if lang == 'en' else '项目数量'}: **{num_projects}**
                - {'Average Investment' if lang == 'en' else '平均投资额'}: **${avg_inv:,.0f}M**
                - {'Top Destination' if lang == 'en' else '第一目的地'}: **{top_country.index[0]}** (${top_country.iloc[0]:,.0f}M)
                
                **{get_text(lang, 'risk_assessment')}**
                """)
                
                # Calculate concentration level
                hhi = calculate_hhi(top_country)
                if hhi > 1800:
                    st.error(get_text(lang, 'high_risk'))
                elif hhi > 1000:
                    st.warning(get_text(lang, 'med_risk'))
                else:
                    st.success(get_text(lang, 'low_risk'))
            
            with col2:
                # Top 5 countries
                st.markdown(f"**{get_text(lang, 'top_5_dest')}**")
                for idx, (country, amount) in enumerate(top_country.head(5).items(), 1):
                    pct = (amount / total_inv * 100) if total_inv > 0 else 0
                    st.markdown(f"{idx}. {country} ({pct:.1f}%)")
            
            st.markdown("---")

if __name__ == "__main__":
    main()
