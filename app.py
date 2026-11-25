import streamlit as st
import pandas as pd
from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer,
    Table, TableStyle, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER

st.set_page_config(
    page_title="ERwin DM Architecture",
    page_icon="🏗️",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
.stApp {
    background-color: #0e1726;
}
.arch-title {
    text-align: center;
    color: #ffffff;
    font-size: 32px;
    font-weight: bold;
}
.subtitle {
    text-align: center;
    color: #aab7c4;
    font-size: 16px;
}
.tier {
    padding: 20px;
    border-radius: 15px;
    margin: 10px 0;
    color: white;
}
.tier1 {
    background: linear-gradient(135deg,#155799,#1597BB);
}
.tier2 {
    background: linear-gradient(135deg,#11998e,#38ef7d);
    color: #062b24;
}
.tier3 {
    background: linear-gradient(135deg,#f7971e,#ffd200);
    color: #382400;
}
.server {
    background: rgba(255,255,255,0.15);
    padding: 15px;
    border-radius: 10px;
    margin: 5px;
    text-align: center;
}
.arrow {
    text-align: center;
    font-size: 35px;
    color: #ffffff;
}
.ip {
    font-size: 17px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)


# ---------------- ARCHITECTURE DATA ----------------

network_data = [
    ["Users / Admin", "Tier 1 – CI/CD", "443", "HTTPS",
     "Secure Portal Access"],
    ["Users / Admin", "Tier 1 – CI/CD", "18170", "TCP",
     "Portal Access"],
    ["Tier 2 Application", "Tier 3 – Database", "3035", "TCP",
     "Database Connectivity"]
]


# ---------------- PDF GENERATOR ----------------

def create_pdf():

    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=landscape(A4),
        rightMargin=35,
        leftMargin=35,
        topMargin=35,
        bottomMargin=35
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "TitleCustom",
        parent=styles["Title"],
        textColor=colors.HexColor("#155799"),
        alignment=TA_CENTER,
        fontSize=22,
        spaceAfter=8
    )

    subtitle_style = ParagraphStyle(
        "SubtitleCustom",
        parent=styles["Normal"],
        alignment=TA_CENTER,
        textColor=colors.HexColor("#555555"),
        fontSize=11,
        spaceAfter=20
    )

    heading_style = ParagraphStyle(
        "HeadingCustom",
        parent=styles["Heading2"],
        textColor=colors.white,
        fontSize=13
    )

    normal_style = ParagraphStyle(
        "NormalCustom",
        parent=styles["Normal"],
        fontSize=10,
        leading=15
    )

    elements = []

    # TITLE
    elements.append(
        Paragraph("ERwin DM Package Architecture", title_style)
    )

    elements.append(
        Paragraph(
            "Three-Tier Infrastructure Architecture",
            subtitle_style
        )
    )

    # TIER 1
    tier1_content = [
        Paragraph("TIER 1 – DEVELOPMENT & CI/CD", heading_style),
        Paragraph(
            "<b>CI/CD Platform – DDL Data Modeler</b><br/>"
            "IP Address: 10.1.192.12<br/>"
            "Portal Port: 18170<br/>"
            "HTTPS Port: 443",
            normal_style
        )
    ]

    tier1 = Table([[tier1_content]], colWidths=[700])
    tier1.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), colors.HexColor("#155799")),
        ("BOX", (0,0), (-1,-1), 1, colors.HexColor("#1597BB")),
        ("LEFTPADDING", (0,0), (-1,-1), 15),
        ("TOPPADDING", (0,0), (-1,-1), 12),
        ("BOTTOMPADDING", (0,0), (-1,-1), 12)
    ]))

    elements.append(tier1)
    elements.append(Spacer(1, 12))

    # TIER 2
    tier2_content = [
        Paragraph("TIER 2 – APPLICATION LAYER", heading_style),
        Paragraph(
            "<b>Apache Web Server – Mart Application</b><br/>"
            "IP Address: 10.1.192.11",
            normal_style
        ),
        Spacer(1, 8),
        Paragraph(
            "<b>Apache Web Server – ER360 Portal</b><br/>"
            "IP Address: 10.1.192.11",
            normal_style
        )
    ]

    tier2 = Table([[tier2_content]], colWidths=[700])
    tier2.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), colors.HexColor("#167C58")),
        ("BOX", (0,0), (-1,-1), 1, colors.HexColor("#38ef7d")),
        ("LEFTPADDING", (0,0), (-1,-1), 15),
        ("TOPPADDING", (0,0), (-1,-1), 12),
        ("BOTTOMPADDING", (0,0), (-1,-1), 12)
    ]))

    elements.append(
        Paragraph(
            "↓ Application Integration",
            ParagraphStyle(
                "Arrow1",
                parent=styles["Normal"],
                alignment=TA_CENTER,
                fontSize=12
            )
        )
    )

    elements.append(tier2)
    elements.append(Spacer(1, 8))

    elements.append(
        Paragraph(
            "↓ Database Connection – TCP 3035",
            ParagraphStyle(
                "Arrow2",
                parent=styles["Normal"],
                alignment=TA_CENTER,
                fontSize=12
            )
        )
    )

    # TIER 3
    tier3_content = [
        Paragraph("TIER 3 – DATABASE / DATA LAYER", heading_style),
        Paragraph(
            "<b>Primary Database Server</b><br/>"
            "IP Address: 10.1.192.12<br/>"
            "Database Port: 3035<br/><br/>"
            "<b>Offline / Supporting Servers</b><br/>"
            "Offline Server 1: 10.1.192.13<br/>"
            "Offline Server 2: 10.1.192.14",
            normal_style
        )
    ]

    tier3 = Table([[tier3_content]], colWidths=[700])
    tier3.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), colors.HexColor("#D99019")),
        ("BOX", (0,0), (-1,-1), 1, colors.HexColor("#FFD200")),
        ("LEFTPADDING", (0,0), (-1,-1), 15),
        ("TOPPADDING", (0,0), (-1,-1), 12),
        ("BOTTOMPADDING", (0,0), (-1,-1), 12)
    ]))

    elements.append(tier3)
    elements.append(Spacer(1, 18))

    # NETWORK TABLE
    elements.append(
        Paragraph("Network Connectivity Summary", styles["Heading2"])
    )

    table_data = [
        ["Source", "Destination", "Port", "Protocol", "Purpose"]
    ] + network_data

    network_table = Table(
        table_data,
        colWidths=[130, 155, 55, 65, 250],
        repeatRows=1
    )

    network_table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#155799")),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),
        ("GRID", (0,0), (-1,-1), 0.5, colors.grey),
        ("BACKGROUND", (0,1), (-1,-1), colors.HexColor("#EAF0F6")),
        ("FONTSIZE", (0,0), (-1,-1), 9),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("PADDING", (0,0), (-1,-1), 7)
    ]))

    elements.append(network_table)
    elements.append(Spacer(1, 15))

    # TECHNICAL NOTES
    elements.append(
        Paragraph("Technical Notes & Validation", styles["Heading2"])
    )

    notes = [
        "1. The IP address 10.1.192.12 is assigned to both Tier 1 and Tier 3. "
        "Confirm whether these are separate interfaces or whether an IP correction is required.",
        "2. Confirm the purpose and role of offline servers - and 10.1.192.14.",
        "3. Confirm the actual Apache application ports and database configuration.",
        "4. Restrict database access to authorized application servers."
    ]

    for note in notes:
        elements.append(Paragraph(note, normal_style))
        elements.append(Spacer(1, 5))

    elements.append(Spacer(1, 15))
    elements.append(
        Paragraph(
            "ERwin DM Infrastructure | Three-Tier Architecture",
            subtitle_style
        )
    )

    doc.build(elements)

    buffer.seek(0)
    return buffer.getvalue()


# ---------------- STREAMLIT DASHBOARD ----------------

st.markdown(
    '<div class="arch-title">ERwin DM Package Architecture</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Three-Tier Infrastructure Architecture</div>',
    unsafe_allow_html=True
)

st.divider()

# TIER 1
st.markdown("""
<div class="tier tier1">
    <h2>🔵 TIER 1 – DEVELOPMENT & CI/CD</h2>
    <div class="server">
        <h3>CI/CD Platform – DDL Data Modeler</h3>
        <p class="ip">IP Address: 10.1.192.12</p>
        <p>Portal Port: 18170</p>
        <p>HTTPS Port: 443</p>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown(
    '<div class="arrow">⬇️ Application Integration</div>',
    unsafe_allow_html=True
)

# TIER 2
st.markdown("""
<div class="tier tier2">
    <h2>🟢 TIER 2 – APPLICATION LAYER</h2>
    <div style="display:flex; gap:15px;">
        <div class="server" style="flex:1;">
            <h3>Apache Web Server</h3>
            <h4>Mart Application</h4>
            <p class="ip">IP: 10.1.192.11</p>
        </div>
        <div class="server" style="flex:1;">
            <h3>Apache Web Server</h3>
            <h4>ER360 Portal</h4>
            <p class="ip">IP: 10.1.192.11</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown(
    '<div class="arrow">⬇️ Database Connection – TCP 3035</div>',
    unsafe_allow_html=True
)

# TIER 3
st.markdown("""
<div class="tier tier3">
    <h2>🟠 TIER 3 – DATABASE / DATA LAYER</h2>
    <div class="server">
        <h3>Primary Database Server</h3>
        <p class="ip">IP: 10.1.192.12</p>
        <p>Database Port: 3035</p>
    </div>
    <br>
    <h3>Offline / Supporting Servers</h3>
    <div style="display:flex; gap:15px;">
        <div class="server" style="flex:1;">
            <h4>Offline Server 1</h4>
            <p class="ip">-</p>
        </div>
        <div class="server" style="flex:1;">
            <h4>Offline Server 2</h4>
            <p class="ip">10.1.192.14</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.divider()

# NETWORK SUMMARY
st.subheader("🌐 Network Connectivity Summary")

df = pd.DataFrame(
    network_data,
    columns=["Source", "Destination", "Port", "Protocol", "Purpose"]
)

st.dataframe(
    df,
    use_container_width=True,
    hide_index=True
)

st.divider()

# DOWNLOAD PDF
st.subheader("📄 Download Architecture Documentation")

pdf_file = create_pdf()

st.download_button(
    label="⬇️ Download ERwin DM Architecture PDF",
    data=pdf_file,
    file_name="ERwin_DM_Three_Tier_Architecture.pdf",
    mime="application/pdf",
    use_container_width=True
)

st.caption(
    "ERwin DM Infrastructure | Three-Tier Architecture"
)
