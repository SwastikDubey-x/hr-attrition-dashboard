import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    """
    Two-pass canvas to dynamically compute and print 'Page X of Y' on every page.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, total_pages):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748b"))

        # Top Header (pages 2+)
        if self._pageNumber > 1:
            self.drawString(54, 750, "PulseHR: Strategic Talent Analytics & Attrition Predictor")
            self.drawRightString(558, 750, "Presentation & Demonstration Guide")
            self.setStrokeColor(colors.HexColor("#e2e8f0"))
            self.setLineWidth(0.5)
            self.line(54, 742, 558, 742)

        # Bottom Footer (all pages)
        self.setStrokeColor(colors.HexColor("#e2e8f0"))
        self.setLineWidth(0.5)
        self.line(54, 45, 558, 45)
        self.drawString(54, 32, "Confidential • Prepared for Academic & Stakeholder Presentation")
        page_str = f"Page {self._pageNumber} of {total_pages}"
        self.drawRightString(558, 32, page_str)
        self.restoreState()


def create_presentation_pdf(output_filename="PulseHR_Presentation_Guide_and_Script.pdf"):
    doc = SimpleDocTemplate(
        output_filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Custom Color Palette
    PRIMARY = colors.HexColor("#1e1b4b")     # Deep Indigo
    SECONDARY = colors.HexColor("#4f46e5")   # Electric Indigo
    TEXT_DARK = colors.HexColor("#0f172a")   # Slate 900
    TEXT_MUTED = colors.HexColor("#475569")  # Slate 600
    BG_LIGHT = colors.HexColor("#f8fafc")    # Slate 50
    ACCENT_GREEN = colors.HexColor("#059669")
    ACCENT_AMBER = colors.HexColor("#d97706")

    # Typography Styles
    title_style = ParagraphStyle(
        "CoverTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=24,
        leading=28,
        textColor=PRIMARY,
        spaceAfter=6
    )

    subtitle_style = ParagraphStyle(
        "CoverSubtitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=12,
        leading=16,
        textColor=SECONDARY,
        spaceAfter=15
    )

    h1_style = ParagraphStyle(
        "Heading1_Custom",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=15,
        leading=19,
        textColor=PRIMARY,
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        "Heading2_Custom",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=16,
        textColor=SECONDARY,
        spaceBefore=10,
        spaceAfter=5,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        "Body_Custom",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9.5,
        leading=13.5,
        textColor=TEXT_DARK,
        spaceAfter=6
    )

    script_speaker_style = ParagraphStyle(
        "ScriptSpeaker",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=10,
        leading=14,
        textColor=SECONDARY,
        spaceBefore=8,
        spaceAfter=3,
        keepWithNext=True
    )

    script_action_style = ParagraphStyle(
        "ScriptAction",
        parent=styles["Normal"],
        fontName="Helvetica-Oblique",
        fontSize=9,
        leading=13,
        textColor=ACCENT_AMBER,
        spaceAfter=3
    )

    script_speech_style = ParagraphStyle(
        "ScriptSpeech",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9.5,
        leading=14,
        textColor=TEXT_DARK,
        leftIndent=12,
        spaceAfter=8
    )

    callout_style = ParagraphStyle(
        "CalloutText",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=13,
        textColor=TEXT_DARK
    )

    story = []

    # -------------------------------------------------------------------------
    # COVER / HEADER BANNER
    # -------------------------------------------------------------------------
    header_table = Table(
        [[
            Paragraph("<b>PULSEHR SUITE</b> • DEMONSTRATION & PRESENTATION GUIDE", ParagraphStyle("Tag", fontName="Helvetica-Bold", fontSize=8.5, textColor=colors.HexColor("#4f46e5"))),
        ]],
        colWidths=[504]
    )
    header_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#eef2ff")),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LINEBELOW', (0,0), (-1,-1), 1, colors.HexColor("#c7d2fe")),
    ]))
    story.append(header_table)
    story.append(Spacer(1, 10))

    story.append(Paragraph("Strategic HR Analytics & Employee Attrition Predictor", title_style))
    story.append(Paragraph("A Complete Presenter Walkthrough, Step-by-Step Feature Guide, Core Terminology, and Word-for-Word Demonstration Script", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#4f46e5"), spaceBefore=0, spaceAfter=14))

    # -------------------------------------------------------------------------
    # SECTION 1: EXECUTIVE OVERVIEW (IN PLAIN ENGLISH)
    # -------------------------------------------------------------------------
    story.append(Paragraph("1. Executive Overview: What is PulseHR & Why Does It Matter?", h1_style))
    story.append(Paragraph(
        "Employee turnover (when employees resign and leave an organization) is among the most costly and disruptive problems modern companies face. "
        "Replacing a single skilled employee typically costs <b>50% to 200% of their annual salary</b> in recruitment expenses, onboarding time, and lost productivity.",
        body_style
    ))
    story.append(Paragraph(
        "<b>PulseHR</b> changes HR from <i>reactive</i> (holding exit interviews after an employee has already decided to quit) to <i>proactive</i> "
        "(identifying flight risk early and giving managers targeted retention strategies). It pairs real-time descriptive workforce analytics with a calibrated "
        "Machine Learning model to forecast turnover risk and protect company talent.",
        body_style
    ))

    # Quick Summary Callout Box
    overview_box = Table([[
        Paragraph(
            "<b>Key Takeaway for Presenters:</b> PulseHR is not just a dashboard; it is an intelligent decision-support system. "
            "It answers three vital questions for HR leaders:<br/>"
            "1. <i>What is happening right now?</i> (Headcount, attrition rates, and satisfaction levels).<br/>"
            "2. <i>Why are people leaving?</i> (Workload/overtime, salary gaps, early-career turnover).<br/>"
            "3. <i>Who is at risk next, and how do we retain them?</i> (AI predictive risk scoring and tailored action plans).",
            callout_style
        )
    ]], colWidths=[504])
    overview_box.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f8fafc")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#cbd5e1")),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(overview_box)
    story.append(Spacer(1, 14))

    # -------------------------------------------------------------------------
    # SECTION 2: ESSENTIAL TERMINOLOGY GLOSSARY
    # -------------------------------------------------------------------------
    story.append(Paragraph("2. Essential Terminology Glossary", h1_style))
    story.append(Paragraph("Use these standardized industry terms during your presentation to convey authority without getting bogged down in math:", body_style))

    term_data = [
        [Paragraph("<b>Term</b>", ParagraphStyle("TH", fontName="Helvetica-Bold", fontSize=9, textColor=colors.white)),
         Paragraph("<b>Plain-English Meaning</b>", ParagraphStyle("TH", fontName="Helvetica-Bold", fontSize=9, textColor=colors.white)),
         Paragraph("<b>How It's Used in the App</b>", ParagraphStyle("TH", fontName="Helvetica-Bold", fontSize=9, textColor=colors.white))],
        
        [Paragraph("<b>Attrition Rate (%)</b>", body_style),
         Paragraph("The percentage of the total workforce that leaves the organization during a period.", body_style),
         Paragraph("Displayed as a primary executive KPI card (e.g., 14.2%). Healthy benchmarks are under 15%.", body_style)],

        [Paragraph("<b>Flight Risk</b>", body_style),
         Paragraph("The calculated likelihood (0% to 100%) that an active employee will resign soon.", body_style),
         Paragraph("Shown on the Radial Gauge Meter in Tab 2 and the 360° Profile Inspector in Tab 3.", body_style)],

        [Paragraph("<b>Tenure</b>", body_style),
         Paragraph("How many years an employee has worked at the company.", body_style),
         Paragraph("Tracked in charts to show early-career risk (0–2 years) versus mid-career retention.", body_style)],

        [Paragraph("<b>Hygiene vs. Motivator Factors</b>", body_style),
         Paragraph("Herzberg's HRM theory: 'Hygiene' factors (salary, overtime) cause dissatisfaction if bad; 'Motivators' (growth, recognition) drive passion.", body_style),
         Paragraph("PulseHR tests both: compensation & overtime (hygiene) and job satisfaction (motivator).", body_style)],

        [Paragraph("<b>Random Forest Classifier</b>", body_style),
         Paragraph("An ensemble AI algorithm that combines hundreds of decision trees to make accurate, unbiased predictions.", body_style),
         Paragraph("Trained on workforce records to evaluate employee profile inputs in real time.", body_style)],

        [Paragraph("<b>Feature Importance</b>", body_style),
         Paragraph("A ranking showing which factors (Overtime, Income, Satisfaction, Age, Tenure) have the greatest impact on turnover.", body_style),
         Paragraph("Visualized as a horizontal bar chart in Tab 2, proving Overtime is the #1 churn driver.", body_style)],

        [Paragraph("<b>Actionable Retention Intervention</b>", body_style),
         Paragraph("Specific, concrete management steps taken to prevent an at-risk employee from resigning.", body_style),
         Paragraph("Dynamically generated in Tab 2 (e.g., workload rebalancing, comp review, mentorship).", body_style)],
    ]

    term_table = Table(term_data, colWidths=[110, 194, 200])
    term_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#f8fafc")]),
    ]))
    story.append(term_table)
    story.append(Spacer(1, 14))

    # -------------------------------------------------------------------------
    # SECTION 3: STEP-BY-STEP WORKING & FEATURE WALKTHROUGH
    # -------------------------------------------------------------------------
    story.append(PageBreak())
    story.append(Paragraph("3. Step-by-Step Feature Walkthrough", h1_style))
    story.append(Paragraph("PulseHR is structured into three intuitive visual tiers. Here is how each element functions:", body_style))

    # Feature 1
    story.append(Paragraph("Tier 1: Executive KPI Cards (Top Banner)", h2_style))
    story.append(Paragraph(
        "Located directly below the Hero Banner, five top-level metric cards display high-priority health vitals: "
        "<b>Total Headcount</b> (current active filtered staff), <b>Attrition Rate</b> (percentage with color-coded status badge), "
        "<b>Average Monthly Income</b> (salary baseline), <b>Average Job Satisfaction</b> (rated on a 1.0 to 4.0 scale), and "
        "<b>OverTime Load</b> (workforce proportion working extra hours). These metrics update dynamically whenever any filter is adjusted.",
        body_style
    ))

    # Feature 2
    story.append(Paragraph("Tier 2: Real-Time Dynamic Sidebar Filters", h2_style))
    story.append(Paragraph(
        "On the left sidebar, users can slice the workforce by <b>Department</b> (Research & Development, Sales, Human Resources), "
        "<b>OverTime Commitment</b> (segmented toggle: All Staff, Overtime Only, Standard Hours), and <b>Monthly Income Range</b> slider. "
        "A one-click <b>'Reset All Filters'</b> button instantly returns the dashboard to organization baseline.",
        body_style
    ))

    # Feature 3
    story.append(Paragraph("Tier 3: The Three Main Functional Tabs", h2_style))

    tab_data = [
        [Paragraph("<b>Tab Name</b>", ParagraphStyle("TH2", fontName="Helvetica-Bold", fontSize=9, textColor=colors.white)),
         Paragraph("<b>What it Displays</b>", ParagraphStyle("TH2", fontName="Helvetica-Bold", fontSize=9, textColor=colors.white)),
         Paragraph("<b>Business Purpose for HR</b>", ParagraphStyle("TH2", fontName="Helvetica-Bold", fontSize=9, textColor=colors.white))],

        [Paragraph("<b>📊 Tab 1:<br/>Workforce Insights & Analytics</b>", body_style),
         Paragraph("• Departmental Attrition grouped bar chart.<br/>"
                   "• Monthly Income vs. Attrition box plots (shows median disparity).<br/>"
                   "• Job Satisfaction & Churn correlation bar chart.<br/>"
                   "• Tenure vs. Overtime flight risk scatter plot.<br/>"
                   "• Executive HRM Strategic Takeaways callout box.", body_style),
         Paragraph("Gives HR leadership macro-level visibility into company-wide turnover patterns. Proves that overtime and salary gaps accelerate resignations.", body_style)],

        [Paragraph("<b>🎯 Tab 2:<br/>Attrition Risk Predictor (ML)</b>", body_style),
         Paragraph("• Interactive Employee Profile input form (Age, Tenure, Overtime, Income, Satisfaction).<br/>"
                   "• Radial Gauge Meter showing probability score (0–100%).<br/>"
                   "• Risk Tier Badge: Low (Green), Moderate (Amber), High (Red).<br/>"
                   "• Feature Importance chart showing top predictive drivers.<br/>"
                   "• Tailored Actionable HR Retention Interventions.", body_style),
         Paragraph("Simulates flight risk for any individual candidate or team member. Tells managers exactly <i>what</i> to do (e.g. rebalance workload, review salary, assign mentor) to prevent departure.", body_style)],

        [Paragraph("<b>📁 Tab 3:<br/>Raw Employee Records & Search</b>", body_style),
         Paragraph("• Universal Search Bar (searches ID, Role, Department).<br/>"
                   "• Advanced Talent Facet Filters (Attrition status, Role, Satisfaction tier, Tenure slider).<br/>"
                   "• Multi-column sorting (Income, Tenure, Satisfaction, ID).<br/>"
                   "• Live Cohort KPI Summary Cards.<br/>"
                   "• Individual 360° Profile Inspector.<br/>"
                   "• 'Export Filtered Cohort to CSV' button.", body_style),
         Paragraph("Operational tool for HR business partners. Allows instant lookup of at-risk staff and exporting clean CSV reports for executive meetings and retention audits.", body_style)],
    ]

    tab_table = Table(tab_data, colWidths=[120, 204, 180])
    tab_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), SECONDARY),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#f8fafc")]),
    ]))
    story.append(tab_table)
    story.append(Spacer(1, 14))

    # -------------------------------------------------------------------------
    # SECTION 4: COMPLETE WORD-FOR-WORD PRESENTATION SCRIPT
    # -------------------------------------------------------------------------
    story.append(PageBreak())
    story.append(Paragraph("4. Word-for-Word Presenter Script (5-Minute Demo Flow)", h1_style))
    story.append(Paragraph("Follow this turn-by-turn script when demonstrating PulseHR to professors, recruiters, or stakeholders:", body_style))

    # Act 1
    story.append(Paragraph("Step 1: The Hook & Introduction [0:00 - 0:45]", script_speaker_style))
    story.append(Paragraph("<b>Action on Screen:</b> Stand on the main dashboard showing the Hero Banner and Top KPI cards.", script_action_style))
    story.append(Paragraph(
        "<i>\"Hello everyone. Today, I'm excited to present <b>PulseHR</b>, an enterprise-grade Talent Intelligence and Attrition Predictor platform.<br/>"
        "In modern business, employee turnover is one of the most expensive hidden costs. When a valued employee resigns, the company loses institutional knowledge, "
        "team productivity halts, and rehiring costs tens of thousands of dollars. Most HR teams only learn someone was unhappy during their exit interview. "
        "PulseHR changes this paradigm: it turns HR from <b>reactive</b> to <b>proactive</b> using data analytics and artificial intelligence.\"</i>",
        script_speech_style
    ))

    # Act 2
    story.append(Paragraph("Step 2: Executive Health KPIs & Live Dynamic Filters [0:45 - 1:45]", script_speaker_style))
    story.append(Paragraph("<b>Action on Screen:</b> Point out the 5 KPI cards. Then adjust the sidebar Department filter and Monthly Income slider.", script_action_style))
    story.append(Paragraph(
        "<i>\"Looking at the top of the screen, we immediately see our organization's vitals: a Total Headcount of 1,200 employees, an overall Attrition Rate "
        "of 14.2%, average monthly compensation of nearly $11,000, and an average job satisfaction of 2.54 out of 4.<br/>"
        "On the left sidebar, we have real-time filter controls. Watch what happens when I filter down to the <b>Sales</b> department and adjust our monthly income range. "
        "Every single metric card, data table, and visualization on the dashboard re-computes in real time. This allows leadership to instantly diagnose specific departments "
        "or salary bands within seconds.\"</i>",
        script_speech_style
    ))

    # Act 3
    story.append(Paragraph("Step 3: Deep Workforce Insights (Tab 1) [1:45 - 2:45]", script_speaker_style))
    story.append(Paragraph("<b>Action on Screen:</b> Click on Tab 1: 'Workforce Insights & Analytics'. Scroll over the bar charts, box plot, and scatter plot.", script_action_style))
    story.append(Paragraph(
        "<i>\"In our <b>Workforce Insights</b> tab, we analyze <b>why</b> employees leave.<br/>"
        "First, our Departmental Dynamics chart shows where the bulk of departures occur. Next, looking at the <b>Monthly Income Box Plot</b>, notice the significant "
        "compensation gap: employees who left had a distinctly lower median income than those who stayed, showing that salary benchmarking is critical.<br/>"
        "Finally, looking at our Tenure versus Overtime scatter plot, we discover two crucial trends: first, attrition peaks in the first 0 to 2 years—known as early-career churn. "
        "Second, employees clocking mandatory overtime show double the flight risk of their standard-hour peers. This proves that burnout is an active driver of attrition.\"</i>",
        script_speech_style
    ))

    # Act 4
    story.append(Paragraph("Step 4: AI Attrition Risk Predictor Demo (Tab 2) [2:45 - 4:00]", script_speaker_style))
    story.append(Paragraph("<b>Action on Screen:</b> Click Tab 2: 'Attrition Risk Predictor'. In the form, set Age=32, Tenure=2, OverTime=Yes, Monthly Income=$4,200, Satisfaction=Low (1). Click 'Predict Attrition Risk'.", script_action_style))
    story.append(Paragraph(
        "<i>\"Now let's see the most powerful capability of PulseHR: our <b>Attrition Risk Predictor</b> powered by a machine-learning Random Forest model.<br/>"
        "Imagine an HR manager wants to evaluate a 32-year-old software engineer who has been with us for 2 years, earns $4,200 a month, works overtime, and reported low job satisfaction.<br/>"
        "I'll click <b>'Predict Attrition Risk'</b>... and instantly, our AI calculates an <b>81% Flight Risk (High Risk Tier)</b> on the radial gauge meter.<br/>"
        "Crucially, PulseHR doesn't just deliver a number; it provides <b>Actionable Retention Interventions</b>. The system recommends: workload rebalancing to mitigate overtime burnout, "
        "a structured 1-on-1 skip-level meeting to address sentiment, and a salary parity review. This gives managers a precise playbook to save that employee before they submit their two-week notice.\"</i>",
        script_speech_style
    ))

    # Act 5
    story.append(Paragraph("Step 5: Talent Search, 360° Profile & CSV Export (Tab 3) [4:00 - 5:00]", script_speaker_style))
    story.append(Paragraph("<b>Action on Screen:</b> Click Tab 3. Type 'Research' in the search bar. Open 'Inspect Individual Employee 360° Profile'. Then point to the 'Export to CSV' button.", script_action_style))
    story.append(Paragraph(
        "<i>\"Finally, in our <b>Raw Employee Records & Advanced Talent Search</b> tab, HR business partners can manage the workforce day-to-day.<br/>"
        "We have a universal search bar that instantly filters by Employee ID, Job Role, or Department. Above the table, live Cohort KPI cards summarize the average salary and attrition rate "
        "of the searched group.<br/>"
        "We can also open the <b>Individual Employee 360° Profile Inspector</b> to pull up any employee's full file and evaluate their personalized ML retention score.<br/>"
        "And with one click on <b>'Export Searched Cohort to CSV'</b>, HR can download a ready-to-use audit report for leadership meetings.\"</i>",
        script_speech_style
    ))

    # Closing
    story.append(Paragraph("Closing & Q&A Readiness [5:00 - 5:30]", script_speaker_style))
    story.append(Paragraph(
        "<i>\"To summarize, PulseHR bridges data science and strategic human resource management. It empowers companies to protect their greatest asset—their people—through proactive, "
        "data-driven retention. Thank you, and I welcome any questions!\"</i>",
        script_speech_style
    ))

    # -------------------------------------------------------------------------
    # SECTION 5: ANTICIPATED QUESTIONS & WINNING ANSWERS
    # -------------------------------------------------------------------------
    story.append(PageBreak())
    story.append(Paragraph("5. Anticipated Questions & Winning Answers", h1_style))
    story.append(Paragraph("Be prepared for these common questions from professors, interviewers, or managers:", body_style))

    qa_data = [
        [Paragraph("<b>Question</b>", ParagraphStyle("TH3", fontName="Helvetica-Bold", fontSize=9, textColor=colors.white)),
         Paragraph("<b>Recommended Winning Answer</b>", ParagraphStyle("TH3", fontName="Helvetica-Bold", fontSize=9, textColor=colors.white))],

        [Paragraph("<b>\"Where does the employee dataset come from?\"</b>", body_style),
         Paragraph("<i>\"The data is statistically synthesized using NumPy with a fixed random seed. It mirrors the realistic distributions of standard industry benchmarks (like the IBM HR Analytics dataset), incorporating realistic correlations like overtime stress and early-tenure turnover.\"</i>", body_style)],

        [Paragraph("<b>\"How does the Machine Learning model calculate flight risk?\"</b>", body_style),
         Paragraph("<i>\"We train a Random Forest Classifier with balanced class weights using Scikit-Learn. It evaluates key features—Overtime, Monthly Income, Job Satisfaction, Age, and Company Tenure—and generates a calibrated probability score (0% to 100%) indicating how closely the employee matches historical departure patterns.\"</i>", body_style)],

        [Paragraph("<b>\"Why is OverTime the strongest predictor of attrition?\"</b>", body_style),
         Paragraph("<i>\"In HRM organizational psychology, sustained overtime leads directly to work-life conflict and burnout. In our feature importance ranking, Overtime emerged as the single highest-weighted flight risk driver, proving that compensation alone cannot offset chronic workload fatigue.\"</i>", body_style)],

        [Paragraph("<b>\"How would a real-world enterprise integrate PulseHR?\"</b>", body_style),
         Paragraph("<i>\"In a live corporate environment, PulseHR connects directly to HR Information Systems (HRIS) like Workday, BambooHR, or SAP SuccessFactors via API. It runs quarterly or monthly retention scans and alerts department heads when high-performing staff enter high-risk flight zones.\"</i>", body_style)],
    ]

    qa_table = Table(qa_data, colWidths=[150, 354])
    qa_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 7),
        ('TOPPADDING', (0,0), (-1,-1), 7),
        ('LEFTPADDING', (0,0), (-1,-1), 7),
        ('RIGHTPADDING', (0,0), (-1,-1), 7),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#f8fafc")]),
    ]))
    story.append(qa_table)

    # Build Document using NumberedCanvas
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF successfully generated: {output_filename}")

if __name__ == "__main__":
    create_presentation_pdf()
