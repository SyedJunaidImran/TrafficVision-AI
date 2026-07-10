"""
TrafficVision AI
AI Powered Traffic Monitoring System

Author: Syed Junaid
"""

import time
import tempfile
import textwrap
from pathlib import Path

import cv2
import pandas as pd
import streamlit as st

from src.video_processor import VideoProcessor
from src.counter import VehicleCounter
from src.density import TrafficDensity
from src.dashboard import Dashboard
from src.report_generator import ReportGenerator

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="TrafficVision AI",
    page_icon="🚦",
    layout="wide",
    initial_sidebar_state="expanded",
)


def render_html(content: str) -> None:
    """Render raw HTML via st.markdown safely.

    Streamlit's markdown parser treats any line indented 4+ spaces as a
    code block. Multi-line HTML strings written with normal Python
    indentation trigger that rule and show up as literal text instead of
    rendering. Dedenting first avoids that.
    """
    st.markdown(textwrap.dedent(content).strip(), unsafe_allow_html=True)


# =====================================================
# THEME / CSS
# =====================================================

render_html(
    """
    <style>
        :root {
            --tv-bg: #0b0f14;
            --tv-panel: #12181f;
            --tv-panel-2: #161d26;
            --tv-border: #232b35;
            --tv-green: #22c55e;
            --tv-green-soft: rgba(34,197,94,0.12);
            --tv-amber: #f59e0b;
            --tv-amber-soft: rgba(245,158,11,0.12);
            --tv-red: #ef4444;
            --tv-red-soft: rgba(239,68,68,0.12);
            --tv-blue: #3b82f6;
            --tv-text: #e6e9ec;
            --tv-muted: #8b96a3;
        }

        .stApp {
            background:
                radial-gradient(circle at 15% -10%, rgba(34,197,94,0.08), transparent 40%),
                radial-gradient(circle at 85% 0%, rgba(59,130,246,0.08), transparent 40%),
                var(--tv-bg);
        }

        #MainMenu, footer, header {visibility: hidden;}

        section[data-testid="stSidebar"] {
            background: var(--tv-panel);
            border-right: 1px solid var(--tv-border);
        }

        .block-container {
            padding-top: 1.5rem;
            padding-bottom: 3rem;
            max-width: 1300px;
        }

        /* Hero header */
        .tv-hero {
            display: flex;
            align-items: center;
            gap: 16px;
            padding: 22px 28px;
            border-radius: 18px;
            background: linear-gradient(135deg, rgba(34,197,94,0.14), rgba(59,130,246,0.10));
            border: 1px solid var(--tv-border);
            margin-bottom: 28px;
        }
        .tv-hero-icon {
            font-size: 40px;
            line-height: 1;
        }
        .tv-hero-title {
            font-size: 28px;
            font-weight: 800;
            color: var(--tv-text);
            margin: 0;
            letter-spacing: -0.3px;
        }
        .tv-hero-sub {
            font-size: 14px;
            color: var(--tv-muted);
            margin: 2px 0 0 0;
        }
        .tv-hero-badge {
            margin-left: auto;
            padding: 6px 14px;
            border-radius: 999px;
            background: var(--tv-green-soft);
            color: var(--tv-green);
            font-size: 12px;
            font-weight: 700;
            border: 1px solid rgba(34,197,94,0.3);
            white-space: nowrap;
        }

        /* Section labels */
        .tv-section-label {
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 13px;
            font-weight: 700;
            letter-spacing: 0.6px;
            text-transform: uppercase;
            color: var(--tv-muted);
            margin: 6px 0 14px 0;
        }
        .tv-section-label::after {
            content: "";
            flex: 1;
            height: 1px;
            background: var(--tv-border);
        }

        /* KPI cards */
        .tv-kpi-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 14px;
            margin-bottom: 14px;
        }
        @media (max-width: 900px) {
            .tv-kpi-grid { grid-template-columns: repeat(2, 1fr); }
        }
        .tv-kpi-card {
            background: var(--tv-panel);
            border: 1px solid var(--tv-border);
            border-radius: 16px;
            padding: 18px 20px;
            transition: transform 0.15s ease, border-color 0.15s ease;
        }
        .tv-kpi-card:hover {
            transform: translateY(-2px);
            border-color: rgba(34,197,94,0.4);
        }
        .tv-kpi-icon {
            font-size: 22px;
            margin-bottom: 6px;
            display: block;
        }
        .tv-kpi-value {
            font-size: 30px;
            font-weight: 800;
            color: var(--tv-text);
            line-height: 1.1;
        }
        .tv-kpi-label {
            font-size: 12.5px;
            color: var(--tv-muted);
            margin-top: 4px;
            font-weight: 600;
        }

        /* Congestion pill */
        .tv-congestion {
            display: inline-flex;
            align-items: center;
            gap: 10px;
            padding: 12px 20px;
            border-radius: 14px;
            font-weight: 700;
            font-size: 15px;
            border: 1px solid transparent;
        }
        .tv-congestion.low {
            background: var(--tv-green-soft);
            color: var(--tv-green);
            border-color: rgba(34,197,94,0.3);
        }
        .tv-congestion.medium {
            background: var(--tv-amber-soft);
            color: var(--tv-amber);
            border-color: rgba(245,158,11,0.3);
        }
        .tv-congestion.high {
            background: var(--tv-red-soft);
            color: var(--tv-red);
            border-color: rgba(239,68,68,0.3);
        }

        /* Empty state */
        .tv-empty {
            text-align: center;
            padding: 70px 20px;
            border: 1px dashed var(--tv-border);
            border-radius: 20px;
            background: var(--tv-panel);
        }
        .tv-empty-icon { font-size: 52px; margin-bottom: 14px; }
        .tv-empty-title { font-size: 20px; font-weight: 700; color: var(--tv-text); margin-bottom: 6px; }
        .tv-empty-sub { font-size: 14px; color: var(--tv-muted); max-width: 420px; margin: 0 auto; }

        /* Frame panel labels */
        .tv-frame-label {
            font-size: 13px;
            font-weight: 700;
            color: var(--tv-muted);
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 8px;
        }

        /* Buttons */
        .stButton > button, .stDownloadButton > button {
            border-radius: 12px !important;
            font-weight: 600 !important;
            border: 1px solid var(--tv-border) !important;
            transition: all 0.15s ease;
        }
        .stButton > button:hover, .stDownloadButton > button:hover {
            border-color: var(--tv-green) !important;
            color: var(--tv-green) !important;
        }

        /* Progress bar */
        div[data-testid="stProgress"] > div > div {
            background-image: linear-gradient(90deg, #22c55e, #3b82f6);
        }

        /* Footer */
        .tv-footer {
            text-align: center;
            padding: 24px 10px 6px 10px;
            color: var(--tv-muted);
            font-size: 12.5px;
        }
        .tv-footer b { color: #a7b0bb; }
        .tv-footer-title {
            font-size: 15px;
            font-weight: 800;
            color: var(--tv-green);
            margin-bottom: 4px;
        }
    </style>
    """
)

# =====================================================
# HERO HEADER
# =====================================================

render_html(
    """
    <div class="tv-hero">
        <div class="tv-hero-icon">🚦</div>
        <div>
            <p class="tv-hero-title">TrafficVision AI</p>
            <p class="tv-hero-sub">AI-powered traffic monitoring using YOLOv8 + ByteTrack</p>
        </div>
        <div class="tv-hero-badge">● Engine Ready</div>
    </div>
    """
)

# =====================================================
# MODULES
# =====================================================

processor = VideoProcessor()
counter = VehicleCounter()
density = TrafficDensity()
dashboard = Dashboard()
report = ReportGenerator()

# =====================================================
# SESSION STATE
# =====================================================

defaults = {
    "analysis_done": False,
    "vehicle_counts": {},
    "density_stats": {},
    "processed_frames": [],
    "original_frames": [],
}
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


def reset_all():
    counter.reset()
    density.reset()
    st.session_state.analysis_done = False
    st.session_state.vehicle_counts = {}
    st.session_state.density_stats = {}
    st.session_state.original_frames = []
    st.session_state.processed_frames = []


# =====================================================
# SIDEBAR — UPLOAD & CONTROLS
# =====================================================

with st.sidebar:

    st.markdown("### 📂 Upload Media")

    media_type = st.radio(
        "Select input type",
        ["🎥 Video", "🖼 Image"],
        horizontal=True,
        label_visibility="collapsed",
    )

    if media_type == "🎥 Video":
        uploaded_file = st.file_uploader(
            "Choose a traffic video",
            type=["mp4", "avi", "mov", "mkv"],
        )
    else:
        uploaded_file = st.file_uploader(
            "Choose a traffic image",
            type=["jpg", "jpeg", "png"],
        )

    if uploaded_file is not None:
        size_kb = uploaded_file.size / 1024
        size_label = f"{size_kb:,.0f} KB" if size_kb < 1024 else f"{size_kb/1024:,.1f} MB"
        st.caption(f"✅ **{uploaded_file.name}** · {size_label}")

    st.write("")

    analyze_button = st.button("🚀 Analyze", use_container_width=True, type="primary")
    reset_button = st.button("🔄 Reset", use_container_width=True)

    st.markdown("---")
    st.markdown("### ⚙️ Engine Info")
    st.caption("Detection: **YOLOv8**")
    st.caption("Tracking: **ByteTrack**")
    st.caption("Vision: **OpenCV**")

    if st.session_state.analysis_done:
        st.markdown("---")
        st.markdown("### 📌 Quick Stats")
        c = st.session_state.vehicle_counts
        if c:
            st.caption(f"Total vehicles tracked: **{c.get('Total', 0)}**")
            st.caption(f"Frames analyzed: **{len(st.session_state.original_frames)}**")

# =====================================================
# RESET
# =====================================================

if reset_button:
    reset_all()
    st.rerun()

# =====================================================
# PROGRESS PLACEHOLDERS (main area)
# =====================================================

progress_placeholder = st.empty()
status_placeholder = st.empty()

# =====================================================
# ANALYSIS ENGINE
# =====================================================

if uploaded_file is not None and analyze_button:

    counter.reset()
    density.reset()
    st.session_state.original_frames = []
    st.session_state.processed_frames = []

    suffix = Path(uploaded_file.name).suffix
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    temp_file.write(uploaded_file.read())
    temp_file.close()
    file_path = temp_file.name

    progress_bar = progress_placeholder.progress(0)
    status_placeholder.info("⏳ Preparing analysis...")

    # ---------------- IMAGE MODE ----------------
    if media_type == "🖼 Image":

        frame = cv2.imread(file_path)

        if frame is None:
            status_placeholder.error("❌ Unable to read image.")

        else:
            annotated_frame, tracked_data = processor.process_frame(frame)

            counter.update(tracked_data)
            density.update(tracked_data)

            st.session_state.original_frames.append(frame)
            st.session_state.processed_frames.append(annotated_frame)

            st.session_state.vehicle_counts = counter.get_counts()
            st.session_state.density_stats = density.get_statistics()

            progress_bar.progress(100)
            status_placeholder.success("✅ Image analysis completed.")
            st.session_state.analysis_done = True

    # ---------------- VIDEO MODE ----------------
    else:

        cap = cv2.VideoCapture(file_path)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        processed = 0

        status_placeholder.info("⏳ Analyzing complete video...")

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            annotated_frame, tracked_data = processor.process_frame(frame)

            counter.update(tracked_data)
            density.update(tracked_data)

            st.session_state.original_frames.append(frame)
            st.session_state.processed_frames.append(annotated_frame)

            processed += 1

            if total_frames > 0:
                percentage = int((processed / total_frames) * 100)
                progress_bar.progress(min(percentage, 100))
                status_placeholder.info(f"⏳ Analyzing video... {min(percentage, 100)}% ({processed}/{total_frames} frames)")

        cap.release()

        st.session_state.vehicle_counts = counter.get_counts()
        st.session_state.density_stats = density.get_statistics()

        progress_bar.progress(100)
        status_placeholder.success("✅ Video analysis completed successfully.")
        st.session_state.analysis_done = True

    time.sleep(0.4)
    progress_placeholder.empty()
    status_placeholder.empty()

# =====================================================
# EMPTY STATE
# =====================================================

if not st.session_state.analysis_done:

    render_html(
        """
        <div class="tv-empty">
            <div class="tv-empty-icon">📡</div>
            <div class="tv-empty-title">No analysis yet</div>
            <div class="tv-empty-sub">
                Upload a traffic video or image from the sidebar and hit
                <b>Analyze</b> to detect vehicles, track density, and generate
                a full traffic report.
            </div>
        </div>
        """
    )

# =====================================================
# RESULTS (TABBED LAYOUT)
# =====================================================

if st.session_state.analysis_done:

    counts = st.session_state.vehicle_counts
    density_stats = st.session_state.density_stats
    original_frames = st.session_state.original_frames
    processed_frames = st.session_state.processed_frames
    is_image = len(original_frames) == 1

    tab_feed, tab_analytics, tab_reports = st.tabs(
        ["🎥 Live Feed", "📈 Analytics", "📄 Reports & Downloads"]
    )

    # -------------------------------------------------
    # TAB 1 — FEED + KPIs
    # -------------------------------------------------
    with tab_feed:

        st.markdown('<div class="tv-section-label">Original vs Processed</div>', unsafe_allow_html=True)

        left_col, right_col = st.columns(2)
        with left_col:
            st.markdown('<div class="tv-frame-label">📹 Original</div>', unsafe_allow_html=True)
            original_placeholder = st.empty()
        with right_col:
            st.markdown('<div class="tv-frame-label">🎯 Processed (Detections)</div>', unsafe_allow_html=True)
            processed_placeholder = st.empty()

        if is_image:
            original_placeholder.image(
                cv2.cvtColor(original_frames[0], cv2.COLOR_BGR2RGB),
                use_container_width=True,
            )
            processed_placeholder.image(
                cv2.cvtColor(processed_frames[0], cv2.COLOR_BGR2RGB),
                use_container_width=True,
            )
        else:
            speed = st.slider(
                "Playback speed (ms/frame)",
                min_value=1, max_value=100, value=25,
            )
            play = st.toggle("▶️ Play video loop", value=True)

            if play:
                for original, processed_f in zip(original_frames, processed_frames):
                    original_placeholder.image(
                        cv2.cvtColor(original, cv2.COLOR_BGR2RGB),
                        use_container_width=True,
                    )
                    processed_placeholder.image(
                        cv2.cvtColor(processed_f, cv2.COLOR_BGR2RGB),
                        use_container_width=True,
                    )
                    time.sleep(speed / 1000)
            else:
                original_placeholder.image(
                    cv2.cvtColor(original_frames[0], cv2.COLOR_BGR2RGB),
                    use_container_width=True,
                )
                processed_placeholder.image(
                    cv2.cvtColor(processed_frames[0], cv2.COLOR_BGR2RGB),
                    use_container_width=True,
                )

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="tv-section-label">Traffic Summary</div>', unsafe_allow_html=True)

        kpis = [
            ("🚗", counts["Total"], "Total Vehicles"),
            ("🚙", counts["Car"], "Cars"),
            ("🏍", counts["Motorcycle"], "Motorcycles"),
            ("🚌", counts["Bus"], "Buses"),
            ("🚛", counts["Truck"], "Trucks"),
            ("🚦", density_stats["current_density"], "Current Density"),
            ("🔥", density_stats["peak_density"], "Peak Density"),
        ]

        card_parts = ['<div class="tv-kpi-grid">']
        for icon, value, label in kpis:
            card_parts.append(
                f'<div class="tv-kpi-card">'
                f'<span class="tv-kpi-icon">{icon}</span>'
                f'<div class="tv-kpi-value">{value}</div>'
                f'<div class="tv-kpi-label">{label}</div>'
                f'</div>'
            )
        card_parts.append("</div>")
        # Joined as a single unindented line so Streamlit's markdown
        # parser renders it as HTML rather than an indented code block.
        st.markdown("".join(card_parts), unsafe_allow_html=True)

        level = density_stats["congestion_level"]
        level_class = {"LOW": "low", "MEDIUM": "medium"}.get(level, "high")
        level_icon = {"LOW": "🟢", "MEDIUM": "🟡"}.get(level, "🔴")

        st.write("")
        st.markdown(
            f'<div class="tv-congestion {level_class}">{level_icon} Congestion Level: {level}</div>',
            unsafe_allow_html=True,
        )

    # -------------------------------------------------
    # TAB 2 — ANALYTICS CHARTS
    # -------------------------------------------------
    with tab_analytics:

        st.markdown('<div class="tv-section-label">Vehicle Distribution</div>', unsafe_allow_html=True)

        chart_counts = {
            "Car": counts["Car"],
            "Motorcycle": counts["Motorcycle"],
            "Bus": counts["Bus"],
            "Truck": counts["Truck"],
        }

        chart_col1, chart_col2 = st.columns(2)
        with chart_col1:
            st.plotly_chart(
                dashboard.vehicle_distribution_chart(chart_counts),
                use_container_width=True,
                key="vehicle_pie_chart",
            )
        with chart_col2:
            st.plotly_chart(
                dashboard.vehicle_bar_chart(chart_counts),
                use_container_width=True,
                key="vehicle_bar_chart",
            )

        st.markdown('<div class="tv-section-label">Density Over Time</div>', unsafe_allow_html=True)

        chart_col3, chart_col4 = st.columns(2)
        with chart_col3:
            st.plotly_chart(
                dashboard.traffic_trend_chart(density_stats["history"]),
                use_container_width=True,
                key="traffic_trend_chart",
            )
        with chart_col4:
            density_percent = min(density_stats["current_density"] * 5, 100)
            st.plotly_chart(
                dashboard.density_gauge(density_percent),
                use_container_width=True,
                key="density_gauge_chart",
            )

    # -------------------------------------------------
    # TAB 3 — REPORTS
    # -------------------------------------------------
    with tab_reports:

        st.markdown('<div class="tv-section-label">Export Analysis</div>', unsafe_allow_html=True)

        pdf_path = report.generate_report(counts, density_stats)

        summary_df = pd.DataFrame(
            {
                "Metric": [
                    "Total Vehicles", "Cars", "Motorcycles", "Buses", "Trucks",
                    "Current Density", "Peak Density", "Congestion Level",
                ],
                "Value": [
                    counts["Total"], counts["Car"], counts["Motorcycle"],
                    counts["Bus"], counts["Truck"],
                    density_stats["current_density"], density_stats["peak_density"],
                    density_stats["congestion_level"],
                ],
            }
        )
        summary_df = summary_df.astype(str)
        csv_data = summary_df.to_csv(index=False)

        st.dataframe(summary_df, use_container_width=True, hide_index=True)

        st.write("")
        download_col1, download_col2 = st.columns(2)

        with download_col1:
            with open(pdf_path, "rb") as pdf_file:
                st.download_button(
                    label="📄 Download PDF Report",
                    data=pdf_file,
                    file_name="TrafficVision_Report.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                )

        with download_col2:
            st.download_button(
                label="📊 Download CSV Report",
                data=csv_data,
                file_name="TrafficVision_Report.csv",
                mime="text/csv",
                use_container_width=True,
            )

        st.write("")
        if st.button("🔄 Analyze Another File", use_container_width=True):
            reset_all()
            st.rerun()

# =====================================================
# FOOTER
# =====================================================

render_html(
    """
    <div class="tv-footer">
        <div class="tv-footer-title">🚦 TrafficVision AI v1.0</div>
        <p>AI-Based Intelligent Traffic Monitoring System</p>
        <p>Built using <b>YOLOv8</b> • <b>ByteTrack</b> • <b>OpenCV</b> • <b>Streamlit</b> • <b>Plotly</b></p>
        <hr style="border: 1px solid #232b35; max-width: 500px; margin: 12px auto;">
        <p style="font-size:12px;">© 2026 TrafficVision AI. All Rights Reserved.</p>
    </div>
    """
)