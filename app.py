import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

# ==========================================
# 1. إعدادات الصفحة
# ==========================================
st.set_page_config(page_title="نظام الشاليهات", layout="wide", page_icon="🏡")

# ==========================================
# 🎨 تصميم احترافي متطور مع RTL
# ==========================================
st.markdown("""
<style>
    /* استيراد خط Cairo العربي الأنيق */
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700;800&display=swap');

    /* تطبيق الخط واتجاه RTL على كامل الصفحة */
    html, body, [class*="css"], .stApp {
        font-family: 'Cairo', sans-serif !important;
        direction: rtl !important;
        text-align: right !important;
        background: linear-gradient(135deg, #f5f7fa 0%, #e8eef5 100%);
    }

    /* إخفاء العناصر الافتراضية */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* تصميم الهيدر الرئيسي الفخم */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2.5rem 2rem;
        border-radius: 20px;
        margin-bottom: 2.5rem;
        box-shadow: 0 15px 35px rgba(102, 126, 234, 0.4);
        text-align: center;
        border: 3px solid rgba(255,255,255,0.2);
    }
    
    .main-header h1 {
        color: white;
        font-size: 3rem;
        font-weight: 800;
        margin: 0;
        text-shadow: 3px 3px 6px rgba(0,0,0,0.3);
        letter-spacing: 2px;
    }
    
    .main-header p {
        color: rgba(255,255,255,0.95);
        font-size: 1.2rem;
        margin-top: 0.8rem;
        font-weight: 300;
        letter-spacing: 0.5px;
    }

    /* تصميم البطاقات الأنيقة */
    .custom-card {
        background: white;
        padding: 2.5rem;
        border-radius: 20px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
        border: 1px solid rgba(102, 126, 234, 0.1);
        transition: all 0.3s ease;
    }
    
    .custom-card:hover {
        box-shadow: 0 12px 35px rgba(0,0,0,0.15);
        transform: translateY(-3px);
    }

    /* تنسيق الأزرار الاحترافية */
    div.stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 12px;
        font-weight: 700;
        font-size: 1.1rem;
        width: 100%;
        border: none;
        padding: 0.8rem 2rem;
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
        transition: all 0.3s ease;
        letter-spacing: 0.5px;
    }
    
    div.stButton > button:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
        box-shadow: 0 8px 30px rgba(102, 126, 234, 0.6);
        transform: translateY(-2px);
    }
    
    div.stButton > button:active {
        transform: translateY(0px);
    }

    /* تنسيق بطاقات المؤشرات (Metrics) - احترافية جداً */
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        padding: 2rem 1.5rem;
        border-radius: 18px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.08);
        text-align: center;
        border: 2px solid rgba(102, 126, 234, 0.15);
        transition: all 0.3s ease;
    }
    
    [data-testid="stMetric"]:hover {
        box-shadow: 0 12px 35px rgba(102, 126, 234, 0.2);
        transform: translateY(-5px);
        border-color: rgba(102, 126, 234, 0.3);
    }
    
    [data-testid="stMetric"] label {
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        color: #4a5568 !important;
    }
    
    [data-testid="stMetric"] [data-testid="stMetricValue"] {
        font-size: 2.2rem !important;
        font-weight: 800 !important;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    /* ضبط محاذاة العناوين */
    h1, h2, h3, h4, h5, h6 {
        text-align: right !important;
        font-family: 'Cairo', sans-serif !important;
    }
    
    h2 {
        color: #2d3748;
        font-weight: 700;
        margin-top: 1.5rem;
    }
    
    h3 {
        color: #4a5568;
        font-weight: 600;
    }

    /* تحسين شكل التابات - فاخرة */
    .stTabs [data-baseweb="tab-list"] {
        gap: 15px;
        background: transparent;
        padding: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: white;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        padding: 1rem 2.5rem;
        font-weight: 600;
        font-size: 1.05rem;
        color: #4a5568;
        border: 2px solid transparent;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: #f7fafc;
        box-shadow: 0 6px 20px rgba(0,0,0,0.12);
        transform: translateY(-2px);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white !important;
        font-weight: 800;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
        border-color: rgba(255,255,255,0.3);
    }

    /* تحسين الحقول */
    .stSelectbox, .stDateInput, .stNumberInput {
        background: white;
        border-radius: 10px;
    }
    
    /* تحسين شكل الفواصل */
    hr {
        margin: 2.5rem 0;
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, #667eea, transparent);
    }
    
    /* تحسين رسائل النجاح والخطأ */
    .stSuccess {
        background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);
        color: white;
        border-radius: 12px;
        padding: 1rem;
        font-weight: 600;
    }
    
    .stError {
        background: linear-gradient(135deg, #f56565 0%, #e53e3e 100%);
        color: white;
        border-radius: 12px;
        padding: 1rem;
        font-weight: 600;
    }
    
    .stInfo {
        background: linear-gradient(135deg, #4299e1 0%, #3182ce 100%);
        color: white;
        border-radius: 12px;
        padding: 1rem;
        font-weight: 600;
    }
    
    .stWarning {
        background: linear-gradient(135deg, #ed8936 0%, #dd6b20 100%);
        color: white;
        border-radius: 12px;
        padding: 1rem;
        font-weight: 600;
    }
    
    /* تحسين الجداول */
    [data-testid="stDataFrame"] {
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 6px 20px rgba(0,0,0,0.1);
    }
    
    /* توسيط زر الإرسال في الفورم */
    .stForm {
        background: white;
        padding: 2rem;
        border-radius: 18px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.08);
        border: 2px solid rgba(102, 126, 234, 0.1);
    }
    
    /* تحسين مظهر الفاصل */
    .section-divider {
        height: 3px;
        background: linear-gradient(90deg, transparent, #667eea, #764ba2, transparent);
        margin: 3rem 0;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# عنوان الصفحة الفخم
# ==========================================
st.markdown("""
<div class="main-header">
    <h1>🏡 نظام إدارة الشاليهات المشترك</h1>
    <p>منصة احترافية لإدارة الحجوزات وتتبع الأرباح</p>
</div>
""", unsafe_allow_html=True)

# خريطة الألوان للسمسار (للجدول الزمني)
BROKER_COLORS = {
    "نجلاء": "#fff59d",
    "مي": "#e1bee7",
    "أحمد": "#c8e6c9",
    "بسملة": "#ffcdd2"
}

# ==========================================
# 2. دوال الاتصال والتعامل مع الداتا
# ==========================================
conn = st.connection("gsheets", type=GSheetsConnection)

def get_data():
    try:
        df = conn.read(worksheet="Data", ttl=0)
        df = df.dropna(how='all')
        return df
    except:
        return pd.DataFrame(columns=['Chalet', 'Broker', 'Start_Date', 'End_Date', 'Days', 'Price_Day', 'Total_Price'])

def save_booking(new_row):
    df = get_data()
    updated_df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    conn.update(worksheet="Data", data=updated_df)
    st.cache_data.clear()

def delete_booking(index_to_delete):
    df = get_data()
    updated_df = df.drop(index_to_delete)
    conn.update(worksheet="Data", data=updated_df)
    st.cache_data.clear()

def check_availability(chalet, start, end):
    df = get_data()
    if df.empty: return True, ""
    
    df['Start_Date'] = pd.to_datetime(df['Start_Date'])
    df['End_Date'] = pd.to_datetime(df['End_Date'])
    req_start = pd.to_datetime(start)
    req_end = pd.to_datetime(end)
    
    chalet_bookings = df[df['Chalet'] == chalet]
    
    for _, row in chalet_bookings.iterrows():
        if req_start < row['End_Date'] and req_end > row['Start_Date']:
            return False, f"مشغول من {row['Start_Date'].date()} إلى {row['End_Date'].date()} (حجز: {row['Broker']})"
    
    return True, "متاح"

# ==========================================
# 3. واجهة المستخدم (Tabs)
# ==========================================
tab1, tab2, tab3 = st.tabs(["📅 الحجوزات والجدول", "❌ إدارة وإلغاء الحجز", "📊 تحليل الأرباح"])

# === التاب 1: الحجز والجدول ===
with tab1:
    # --- فورم الحجز الأنيق ---
    with st.container():
        st.markdown("### ➕ إضافـة حجـز جديـد")
        st.markdown("")
        
        with st.form("booking_form"):
            c1, c2, c3 = st.columns(3)
            
            with c1:
                chalet_name = st.selectbox("🏠 الشاليه", ["3 غرف 1111", "3 غرف عمارة 7435", "3024غرفتين ارضي","3317غرفتين علوي","6313 غرفتين علوي","غرفتين اليخت 11304","5301 السفينه","5201ريفير","5202تيتانك","5201Aاطلنتس","5202Aارابيسك","3401a ٣ غرف ","3305اربع غرف","14013","3308"])
                broker_name = st.selectbox("👤 السمسار", ["نجلاء", "مي", "أحمد", "بسملة"])
            
            with c2:
                check_in = st.date_input("📅 تاريخ الوصول", datetime.today())
                check_out = st.date_input("📅 تاريخ المغادرة", datetime.today() + timedelta(days=1))
            
            with c3:
                days = (check_out - check_in).days
                st.info(f"⏰ المدة: **{days} ليالي**")
                price = st.number_input("💵 سعر الليلة (جنيه)", value=1000, step=100)
            
            st.markdown("")
            
            # توسيط الزرار
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                submit = st.form_submit_button("💾 حفظ الحجز")
            
            if submit:
                if days <= 0:
                    st.error("⚠️ تاريخ المغادرة يجب أن يكون بعد تاريخ الوصول!")
                else:
                    is_free, msg = check_availability(chalet_name, check_in, check_out)
                    if not is_free:
                        st.error(f"⛔ لا يمكن الحجز! الشاليه {msg}")
                    else:
                        new_data = {
                            "Chalet": chalet_name, "Broker": broker_name,
                            "Start_Date": str(check_in), "End_Date": str(check_out),
                            "Days": days, "Price_Day": price, "Total_Price": days*price
                        }
                        save_booking(new_data)
                        st.success("✅ تم حفظ الحجز بنجاح!")
                        st.rerun()

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    # --- الجدول الزمني الملون ---
    st.markdown("### Sheet")
    st.markdown("")
    
    df = get_data()
    if not df.empty:
        grid = []
        for _, row in df.iterrows():
            try:
                s = pd.to_datetime(row['Start_Date'])
                e = pd.to_datetime(row['End_Date'])
                curr = s
                while curr < e:
                    grid.append({'Date': curr, 'Chalet': row['Chalet'], 
                                 'Info': f"{row['Broker']}\n({row['Total_Price']})", 
                                 'ColorKey': row['Broker']})
                    curr += timedelta(days=1)
            except: continue
            
        if grid:
            grid_df = pd.DataFrame(grid)
            full_range = pd.date_range(start=datetime(datetime.now().year, 1, 1), 
                                     end=datetime(datetime.now().year, 12, 31))
            
            matrix = grid_df.pivot_table(index='Date', columns='Chalet', values='Info', aggfunc='last')
            matrix = matrix.reindex(full_range)
            matrix.index = matrix.index.strftime('%a %d-%m')

            def colorize(val):
                if pd.isna(val): return ''
                color = "#e0e0e0"
                for name, code in BROKER_COLORS.items():
                    if name in str(val): color = code
                return f'background-color: {color}; color: black; border: 1px solid white; font-weight: bold; text-align: center;'

            st.dataframe(matrix.style.applymap(colorize), use_container_width=True, height=600)
        else:
            st.info("📭 لا توجد حجوزات لعرضها في الجدول الزمني")
    else:
        st.info("📭 لا توجد حجوزات حالياً")

# === التاب 2: الإلغاء ===
with tab2:
    st.markdown("### ❌ إدارة الحجوزات")
    st.info("💡 يمكنك هنا مراجعة وحذف الحجوزات الخاطئة أو الملغاة")
    st.markdown("")
    
    df_del = get_data()
    if not df_del.empty:
        df_del['Label'] = df_del.apply(lambda x: f"{x['Chalet']} | {x['Broker']} | من {x['Start_Date']}", axis=1)
        
        with st.container():
            col_del1, col_del2 = st.columns([3, 1])
            
            with col_del1:
                booking_to_cancel = st.selectbox("🔻 اختر الحجز المراد إلغاؤه:", df_del['Label'].unique())
            
            with col_del2:
                st.markdown("")
                st.markdown("")
                if st.button("🗑️ حذف الحجز"):
                    index_to_drop = df_del[df_del['Label'] == booking_to_cancel].index
                    delete_booking(index_to_drop)
                    st.success("✅ تم حذف الحجز بنجاح!")
                    st.rerun()
        
        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
        
        st.markdown("### 📋 سجل الحجوزات الحالي")
        st.dataframe(df_del[['Chalet', 'Broker', 'Start_Date', 'End_Date', 'Total_Price']], use_container_width=True)
    else:
        st.warning("📭 لا توجد حجوزات حالياً")

# === التاب 3: التحليل (Analysis) ===
with tab3:
    st.markdown("### 📊 Dashboard")
    st.markdown("")
    
    df_an = get_data()
    
    if not df_an.empty:
        df_an['Total_Price'] = pd.to_numeric(df_an['Total_Price'], errors='coerce')
        df_an['Days'] = pd.to_numeric(df_an['Days'], errors='coerce')
        
        total_rev = df_an['Total_Price'].sum()
        total_days = df_an['Days'].sum()
        
        if not df_an.empty and total_rev > 0:
            top_chalet = df_an.groupby('Chalet')['Total_Price'].sum().idxmax()
        else:
            top_chalet = "غير متاح"
        
        # عرض بطاقات المؤشرات الاحترافية
        m1, m2, m3 = st.columns(3)
        m1.metric("💰 إجمالي الأرباح", f"{total_rev:,.0f} ج.م")
        m2.metric("🌙 عدد الليالي المحجوزة", f"{total_days}")
        m3.metric("🏆 الشاليه الأفضل أداءً", top_chalet)
        
        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
        
        # الرسوم البيانية
        c_chart1, c_chart2 = st.columns(2)
        
        with c_chart1:
            st.markdown("#### 📈 توزيع الأرباح حسب الشاليه")
            if total_rev > 0:
                fig_bar = px.bar(
                    df_an.groupby('Chalet')['Total_Price'].sum().reset_index(), 
                    x='Chalet', 
                    y='Total_Price', 
                    color='Chalet', 
                    text_auto=True,
                    color_discrete_sequence=px.colors.qualitative.Pastel
                )
                fig_bar.update_layout(
                    showlegend=False,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)'
                )
                st.plotly_chart(fig_bar, use_container_width=True)
        
        with c_chart2:
            st.markdown("#### 🕵️ نشاط المؤجرين")
            if total_rev > 0:
                fig_pie = px.pie(
                    df_an, 
                    names='Broker', 
                    values='Total_Price', 
                    hole=0.4,
                    color_discrete_sequence=px.colors.qualitative.Pastel
                )
                fig_pie.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)'
                )
                st.plotly_chart(fig_pie, use_container_width=True)
    else:
        st.info("📊 لا توجد بيانات كافية لعرض التحليلات المالية")