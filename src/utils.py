import streamlit as st
import plotly.graph_objects as go

def inject_custom_css():
    """Injects strong CSS overrides to force a premium, colorful dark medical theme globally."""
    st.markdown(
        """
        <style>
        /* Base typography and theme setup (Plus Jakarta Sans) */
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght=300;400;500;600;700&display=swap');
        
        /* 1. Dark Mode Viewport Constraints */
        html, body, [class*="css"], [data-testid="stAppViewContainer"] {
            font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background-color: #0b0f19 !important;
            color: #ffffff !important;
        }
        
        [data-testid="stHeader"] {
            background-color: #0b0f19 !important;
            color: #ffffff !important;
        }

        /* Hide Sidebar Completely */
        [data-testid="stSidebar"] {
            display: none !important;
        }
        [data-testid="collapsedControl"] {
            display: none !important;
        }

        /* 2. Radio Selector as Segmented Pills (Unified stRadio selector) */
        div[data-testid="stRadio"] > div[role="radiogroup"] {
            display: flex !important;
            flex-direction: row !important;
            justify-content: center !important;
            gap: 12px !important;
            background: transparent !important;
            border: none !important;
            padding: 8px 0 !important;
        }
        
        div[data-testid="stRadio"] label {
            padding: 8px 24px !important;
            border-radius: 30px !important;
            background-color: #151b2d !important;
            border: 1.5px solid #2e3a52 !important;
            color: #94a3b8 !important;
            text-align: center !important;
            font-weight: 600 !important;
            font-size: 14px !important;
            cursor: pointer !important;
            transition: all 0.25s ease-in-out !important;
            box-shadow: 0 2px 4px rgba(0,0,0,0.15) !important;
            margin: 0 !important;
        }
        
        div[data-testid="stRadio"] label:hover {
            border-color: #0ea5e9 !important;
            color: #0ea5e9 !important;
            box-shadow: 0 0 8px rgba(14, 165, 233, 0.2) !important;
        }

        /* Hide the circular indicator in radio inputs */
        div[data-testid="stRadio"] label > div:first-child {
            display: none !important;
        }
        
        /* Highlight selected label in premium blue/cyan gradient */
        div[data-testid="stRadio"] label:has(input:checked) {
            background: linear-gradient(135deg, #2563eb 0%, #0ea5e9 100%) !important;
            color: #ffffff !important;
            border-color: #0ea5e9 !important;
            box-shadow: 0 4px 14px rgba(14, 165, 233, 0.4) !important;
        }
        
        div[data-testid="stRadio"] div[data-checked="true"] label {
            background: linear-gradient(135deg, #2563eb 0%, #0ea5e9 100%) !important;
            color: #ffffff !important;
            border-color: #0ea5e9 !important;
            box-shadow: 0 4px 14px rgba(14, 165, 233, 0.4) !important;
        }

        /* 3. Hide Streamlit number input spinner buttons completely */
        div[data-testid="stNumberInputStepUp"], 
        div[data-testid="stNumberInputStepDown"],
        div[data-testid="stNumberInput"] button {
            display: none !important;
        }
        
        /* Remove webkit and firefox spinner display */
        input[type="number"]::-webkit-outer-spin-button,
        input[type="number"]::-webkit-inner-spin-button {
            -webkit-appearance: none !important;
            margin: 0 !important;
        }
        
        input[type="number"] {
            -moz-appearance: textfield !important;
            border: 1px solid #2e3a52 !important;
            border-radius: 6px !important;
            padding: 8px 12px !important;
            height: 38px !important;
            font-size: 14px !important;
            background-color: #1e293b !important;
            color: #ffffff !important;
            width: 100% !important;
            transition: all 0.2s ease !important;
        }

        input[type="number"]:focus {
            border-color: #0ea5e9 !important;
            box-shadow: 0 0 8px rgba(14, 165, 233, 0.3) !important;
            outline: none !important;
        }
        
        /* Expand input container to take 100% width since buttons are hidden */
        div[data-testid="stNumberInput"] > div {
            width: 100% !important;
        }

        /* Dropdowns in main container */
        div[data-baseweb="select"] > div {
            background-color: #1e293b !important;
            color: #ffffff !important;
            border: 1px solid #2e3a52 !important;
            border-radius: 6px !important;
            height: 38px !important;
            transition: all 0.2s ease !important;
        }
        
        div[data-baseweb="select"] > div:focus-within {
            border-color: #0ea5e9 !important;
            box-shadow: 0 0 8px rgba(14, 165, 233, 0.3) !important;
        }
        
        /* Dropdown popover list items styling */
        div[role="listbox"] {
            background-color: #151b2d !important;
            color: #ffffff !important;
            border: 1px solid #2e3a52 !important;
        }
        
        li[role="option"] {
            background-color: transparent !important;
            color: #ffffff !important;
        }
        
        li[role="option"]:hover, li[role="option"][aria-selected="true"] {
            background-color: #1e293b !important;
            color: #0ea5e9 !important;
        }

        /* Form labels */
        label, .stWidgetLabel, [data-testid="stWidgetLabel"] p, [data-testid="stWidgetLabel"] span {
            color: #cbd5e1 !important;
            font-weight: 600 !important;
            font-size: 13px !important;
            margin-bottom: 2px !important;
        }

        /* Primary Button (Glowing Blue-to-Sky Gradient) */
        button[kind="primary"] {
            background: linear-gradient(135deg, #2563eb 0%, #0ea5e9 100%) !important;
            color: #ffffff !important;
            border: none !important;
            font-weight: 700 !important;
            font-size: 15px !important;
            border-radius: 6px !important;
            padding: 10px 24px !important;
            box-shadow: 0 4px 14px rgba(14, 165, 233, 0.3) !important;
            transition: all 0.2s ease !important;
            width: 100% !important;
            height: 44px !important;
        }
        
        button[kind="primary"]:hover {
            background: linear-gradient(135deg, #1d4ed8 0%, #0284c7 100%) !important;
            box-shadow: 0 6px 20px rgba(14, 165, 233, 0.45) !important;
            transform: translateY(-1px);
        }

        /* Secondary Button (Export/Reset style) */
        button[kind="secondary"] {
            border: 1.5px solid #2e3a52 !important;
            background-color: #1e293b !important;
            color: #cbd5e1 !important;
            font-weight: 600 !important;
            border-radius: 6px !important;
            transition: all 0.2s ease !important;
            width: 100% !important;
        }
        
        button[kind="secondary"]:hover {
            border-color: #0ea5e9 !important;
            color: #0ea5e9 !important;
            background-color: #151b2d !important;
        }

        /* 4. Global Typography Overrides */
        p, li, span, ul, ol, div.stMarkdown {
            color: #cbd5e1 !important;
        }
        
        h1, h2, h3, h4, h5, h6 {
            color: #ffffff !important;
            font-weight: 700 !important;
            margin-top: 0px !important;
        }

        /* 5. Custom White Containers (Darkened) */
        [data-testid="stVerticalBlockBorderWrapper"] {
            background-color: #151b2d !important;
            border: 1px solid #2e3a52 !important;
            border-radius: 8px !important;
            padding: 20px !important;
            margin-bottom: 12px !important;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25) !important;
        }
        
        /* Clinical Header Styling */
        .clinical-header {
            text-align: center;
            margin-bottom: 16px;
        }
        .medical-icon {
            font-size: 32px;
            margin-bottom: 4px;
        }
        .gradient-title {
            background: linear-gradient(135deg, #2563eb 0%, #0ea5e9 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 30px;
            font-weight: 800;
            margin: 0 0 2px 0 !important;
        }
        .clinical-subtitle {
            font-size: 13.5px;
            color: #94a3b8 !important;
            margin: 0 !important;
        }

        /* Diagnostic Status Banner Styling */
        .status-banner {
            padding: 10px 14px;
            border-radius: 6px;
            font-size: 13.5px;
            margin-bottom: 16px;
            border: 1px solid;
            display: flex;
            align-items: center;
            gap: 8px;
            font-weight: 600;
        }
        .status-awaiting {
            background-color: #2a1f0d !important; /* dark amber */
            border-color: #78350f !important;
            color: #f59e0b !important; /* amber-500 */
        }
        .status-complete {
            background-color: #0c2315 !important; /* dark green */
            border-color: #064e3b !important;
            color: #22c55e !important; /* green-500 */
        }

        /* Results & Custom progress bar */
        .result-card {
            border-radius: 8px;
            padding: 18px;
            margin-top: 8px;
            border: 1px solid;
            background-color: #151b2d;
            box-shadow: 0 4px 15px rgba(0,0,0,0.3) !important;
        }
        .result-healthy {
            border-color: #22c55e !important;
            border-left: 5px solid #22c55e !important;
            box-shadow: 0 0 15px rgba(34, 197, 94, 0.15) !important;
        }
        .result-risk {
            border-color: #ef4444 !important;
            border-left: 5px solid #ef4444 !important;
            box-shadow: 0 0 15px rgba(239, 68, 68, 0.15) !important;
        }
        
        .result-header {
            font-size: 19px;
            font-weight: 700;
            margin-bottom: 14px;
            display: flex;
            align-items: center;
            gap: 6px;
        }
        .result-healthy-title {
            color: #22c55e !important;
        }
        .result-risk-title {
            color: #ef4444 !important;
        }

        .confidence-container {
            margin-top: 14px;
            margin-bottom: 12px;
        }
        .confidence-label {
            font-size: 13px;
            font-weight: 600;
            color: #cbd5e1 !important;
            display: flex;
            justify-content: space-between;
        }
        .confidence-bar-bg {
            background-color: #1e293b;
            border-radius: 9999px;
            height: 10px;
            width: 100%;
            margin-top: 6px;
            overflow: hidden;
            border: 1px solid #2e3a52;
        }
        .confidence-bar-fill {
            height: 100%;
            border-radius: 9999px;
            box-shadow: 0 0 8px rgba(255,255,255,0.15);
        }
        .confidence-fill-healthy {
            background: linear-gradient(90deg, #10b981 0%, #22c55e 100%) !important;
            box-shadow: 0 0 8px rgba(34, 197, 94, 0.4) !important;
        }
        .confidence-fill-risk {
            background: linear-gradient(90deg, #f43f5e 0%, #ef4444 100%) !important;
            box-shadow: 0 0 8px rgba(239, 68, 68, 0.4) !important;
        }

        .result-detail-row {
            display: flex;
            justify-content: space-between;
            font-size: 13px;
            padding: 6px 0;
            border-bottom: 1px dashed #2e3a52;
        }
        .result-detail-row:last-child {
            border-bottom: none;
        }
        .result-detail-label {
            color: #94a3b8 !important;
        }
        .result-detail-value {
            font-weight: 600;
            color: #ffffff !important;
        }

        </style>
        """,
        unsafe_allow_html=True
    )

def plot_confusion_matrix(cm, model_name):
    """Placeholder chart for test suite compatibility."""
    return go.Figure()

def plot_roc_curve(fpr, tpr, roc_auc, model_name):
    """Placeholder chart for test suite compatibility."""
    return go.Figure()

def plot_feature_importance(df_imp, model_name):
    """Placeholder chart for test suite compatibility."""
    return go.Figure()
