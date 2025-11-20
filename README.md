# China Outbound Investment Analysis - Interactive Dashboard

An interactive Streamlit dashboard for analyzing Chinese enterprises' outbound investment patterns across key industries.

## 🎯 Target Industries

1. **Integrated Circuits** (4 projects) - High geopolitical risk case study
2. **Biopharmaceuticals** (30 projects) - Healthcare sector analysis
3. **New Energy Vehicles** (225 projects) - Major automotive investments
4. **Mineral Resources** (412 projects) - Most comprehensive dataset

## 🚀 Quick Start

### Local Development

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Run the app:**
```bash
streamlit run app.py
```

3. **Open in browser:**
The app will automatically open at `http://localhost:8501`

## 📊 Features

### Interactive Filters
- **Industry Selection**: Choose one or multiple industries
- **Time Range**: Filter by year range (2005-2025)
- **Country Filter**: Focus on specific countries
- **Investment Amount**: Set min/max investment thresholds

### Analysis Views

#### 📈 Trends Tab
- Time series analysis for each industry
- Dual-axis charts showing investment amount and project count
- Identify peak investment periods and policy shifts

#### 🌍 Geographic Tab
- Top 15 investment destinations per industry
- Interactive bar charts with detailed statistics
- Quick country-level summaries

#### 🎯 Concentration Tab
- HHI (Herfindahl-Hirschman Index) analysis
- Top 3 countries share visualization
- Risk concentration assessment

#### 📋 Data Explorer
- Full dataset table with sorting and filtering
- Download filtered data as CSV
- Detailed project information

#### 💡 Insights Tab
- Automated risk assessments
- Key statistics per industry
- Top destination rankings

## 🌐 Deploy to Streamlit Cloud

### Method 1: Via GitHub

1. **Create a GitHub repository:**
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin <your-repo-url>
git push -u origin main
```

2. **Deploy on Streamlit Cloud:**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Click "New app"
   - Connect your GitHub repository
   - Select `app.py` as the main file
   - Click "Deploy"

### Method 2: Direct Upload

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Upload your files directly
3. Streamlit will automatically detect `requirements.txt`

## 📁 Required Files

Make sure these files are in the same directory:
- `app.py` - Main Streamlit application
- `china_investment_tracker.csv` - Investment data
- `requirements.txt` - Python dependencies
- `README.md` - This file

## 🎓 Training Usage

### For Presenters:
1. Use filters to focus on specific industries relevant to the audience
2. Show real-time data exploration during Q&A
3. Generate custom visualizations on the fly
4. Export filtered data for follow-up discussions

### For Participants:
1. Self-serve data exploration after training
2. Compare different industries and time periods
3. Identify investment opportunities in specific countries
4. Download data for further analysis

## 📊 Data Notes

- **Time Period**: 2005-2025
- **Classification Method**: Strict keyword matching to avoid false positives
- **Integrated Circuits**: Only 4 projects reflect tight M&A restrictions
- **AI Industry**: Excluded due to insufficient historical data

## 🔧 Customization

### Adding New Industries

Edit `INDUSTRY_KEYWORDS` in `app.py`:
```python
INDUSTRY_KEYWORDS = {
    'Your Industry': ['keyword1', 'keyword2', ...],
    ...
}
```

### Adjusting Filters

Modify the sidebar section in `app.py` to add new filter options.

### Changing Chart Styles

Update Plotly chart configurations for different visualizations.

## 📝 License

This tool is for educational and training purposes.

## 🤝 Support

For questions or issues, please contact the training organizers.

---

**Built for Beijing Belt & Road Enterprise Training Program**






