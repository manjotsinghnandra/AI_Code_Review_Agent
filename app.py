import streamlit as st
import pandas as pd
import os
import sys

# Force Python to look at the current working directory for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.ingestion import clone_repository, get_all_python_files
from core.parser import parse_python_file
from core.llm_client import analyze_code_structures

# Configure page visual style
st.set_page_config(page_title="AI Code Review Agent", page_icon="🤖", layout="wide")

st.title("🤖 Autonomous AI Code Review Agent")
st.markdown("---")

# Secure Linux temp directory for cloud cloning permissions
target_dir = "/tmp/active_review" if not os.name == 'nt' else os.path.join(os.getcwd(), "cloned_repos", "active_review")

# Input field for users to paste a public repository URL
repo_url = st.text_input(
    "Enter Public GitHub Repository URL:", 
    placeholder="https://github.com/octocat/Spoon-Knife"
)

# Execution logic button click
if st.button("Run Full Agentic Review", type="primary"):
    if not repo_url:
        st.error("Please provide a valid repository URL first!")
    else:
        with st.spinner("Step 1/3: Ingesting & Cloning repository down locally..."):
            try:
                if os.path.exists(target_dir):
                    import shutil
                    shutil.rmtree(target_dir, ignore_errors=True)
                clone_repository(repo_url, target_dir)
            except Exception as e:
                st.error(f"Ingestion Error: {e}")
                st.stop()

        with st.spinner("Step 2/3: Generating Abstract Syntax Tree (AST) mapping tracks..."):
            python_files = get_all_python_files(target_dir)
            all_structures = []
            
            for file_path in python_files:
                file_items = parse_python_file(file_path)
                for item in file_items:
                    item['file_path'] = os.path.relpath(file_path, target_dir)
                all_structures.extend(file_items)
                
            if not all_structures:
                st.warning("No parseable functions or classes discovered inside this repository.")
                st.stop()
                
        with st.spinner(f"Step 3/3: Passing {len(all_structures)} modules to Llama-3.3 brain..."):
            try:
                review_comments = analyze_code_structures(all_structures)
                st.session_state['review_findings'] = review_comments
                st.success("Analysis Complete!")
            except Exception as e:
                st.error(f"AI Matrix Evaluation Failure: {e}")

st.markdown("---")

if 'review_findings' in st.session_state and st.session_state['review_findings']:
    findings = st.session_state['review_findings']
    df = pd.DataFrame(findings)
    
    st.sidebar.header("🎛️ Filter Controls")
    available_categories = df['category'].unique().tolist() if 'category' in df.columns else []
    selected_categories = st.sidebar.multiselect("Select Categories:", options=available_categories, default=available_categories)
    
    available_severities = df['severity'].unique().tolist() if 'severity' in df.columns else []
    selected_severities = st.sidebar.multiselect("Select Severities:", options=available_severities, default=available_severities)
    
    if 'category' in df.columns and 'severity' in df.columns:
        filtered_df = df[(df['category'].isin(selected_categories)) & (df['severity'].isin(selected_severities))]
    else:
        filtered_df = df
    
    tab1, tab2 = st.tabs(["🔒 Verified Insights (Confidence >= 70%)", "⚠️ Unverified Checks (VERIFY THIS < 70%)"])
    
    with tab1:
        high_conf = filtered_df[filtered_df['confidence_score'] >= 70] if 'confidence_score' in filtered_df.columns else filtered_df
        st.subheader(f"Verified Audit Detections ({len(high_conf)} findings)")
        if high_conf.empty:
            st.info("No high-confidence items match your current filter selections.")
        else:
            for _, row in high_conf.iterrows():
                with st.expander(f"🔴 **[{row.get('severity', 'INFO')}]** inside `{row.get('target_name', 'Unknown')}` (Line {row.get('line_number', 'N/A')})"):
                    st.markdown(f"**File Location:** `{row.get('file_path', 'Root')}`")
                    st.markdown(f"**Category:** `{row.get('category', 'General')}` | **Agent Certainty Score:** `{row.get('confidence_score', 100)}%`")
                    st.markdown(f"**Issue Description:** {row.get('comment', '')}")
                    st.markdown("**💡 Recommended Solution Fix:**")
                    st.code(row.get('suggested_fix', '# No fix provided'), language="python")
                    
    with tab2:
        low_conf = filtered_df[filtered_df['confidence_score'] < 70] if 'confidence_score' in filtered_df.columns else pd.DataFrame()
        st.subheader(f"Epistemic Humility Checklist ({len(low_conf)} items requiring manual reviews)")
        if low_conf.empty:
            st.info("No lower-level uncertainty warning findings to show.")
        else:
            for _, row in low_conf.iterrows():
                with st.expander(f"⚠️ **[VERIFY THIS]** Suggestion inside `{row.get('target_name', 'Unknown')}` (Line {row.get('line_number', 'N/A')})"):
                    st.markdown(f"**File Location:** `{row.get('file_path', 'Root')}`")
                    st.warning(f"**Agent Confidence Warning Score:** {row.get('confidence_score', 0)}% (Human review highly advised)")
                    st.markdown(f"**Heuristic Note:** {row.get('comment', '')}")
                    st.markdown("**Suggested Layout Update Snippet:**")
                    st.code(row.get('suggested_fix', '# No fix provided'), language="python")

    st.markdown("---")
    st.subheader("📥 Export Audit Findings")
    csv_data = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(label="Download Full Summary Report as CSV", data=csv_data, file_name="ai_agent_code_review_report.csv", mime="text/csv")