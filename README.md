# Retail & E-Commerce Analytics Dashboard Through AI Agents

[Power BI Project (.pbip)](./Retail_Ecommerce_Analytics.pbip) | [Power BI PDF Report Export](./Retail_Ecommerce_Analytics_PBI_PDF.pdf) | [Raw Datasets](./datasets/)

A complete, fully functional Retail and E-Commerce dashboard built in Power BI Developer Mode (.pbip).

Building a comprehensive dashboard like this by hand typically takes between 16 and 26 hours of manual setup. By using AI agents, this entire project was planned, built, and verified in just 30 to 45 minutes. That represents an immediate time savings of over 95%, cutting more than 20 hours of repetitive manual effort while maintaining high visual quality and accurate business formulas.

This repository demonstrates how raw data and straightforward instructions can be fed into Google Antigravity and Microsoft Power BI tools to deliver a polished, ready to use business dashboard in a fraction of the usual time.

---

## The 4-Step Creation Workflow

This project followed a straightforward, repeatable four-step process combining human direction with AI tools:

1. Data Sourcing and Customization
   Located a raw Retail and E-Commerce transactional dataset on Google Dataset Search. Curated and adjusted the tables to reflect realistic multi-channel retail operations, covering sales transactions, customer records, store locations, products, and inventory snapshots.

2. Prompt Engineering in Google Gemini
   Used the Google Gemini Web App to synthesize the project context and generate the master prompt for the build. Provided Gemini with the custom datasets along with Microsoft research resources, including:
   * Microsoft demonstration videos on building Power BI reports through AI agents: [Video 1](https://youtu.be/O8OKSNUD3lA) and [Video 2](https://youtu.be/NIDS9wMcSsE)
   * [Microsoft Skills for Fabric](https://github.com/microsoft/skills-for-fabric/tree/main) repository for modeling and design best practices
   * [Microsoft Power BI Modeling MCP](https://github.com/microsoft/powerbi-modeling-mcp) documentation for programmatic model creation
   Prompted Gemini to synthesize these resources and generate the most effective, structured instructions for Google Antigravity to build the entire solution.

3. Autonomous Build in Google Antigravity
   Created the project workspace inside Google Antigravity, placed the dataset files into the folder, and provided the generated master prompt. Antigravity read the files, structured the data model, wrote 26 business calculations, and built the four dashboard pages with consistent formatting.

4. Fine-Tuning and Verification
   Ran automated checks against official Microsoft rules to ensure the report opens without errors, verified visual alignments, and exported high-resolution PDF copies for easy sharing.

---

## Executive Summary: How the AI Agent Methodology Works

In a traditional setup, creating a business report in Power BI requires hours of clicking through menus. An analyst has to clean and format tables one by one, manually connect them, write dozens of formulas by hand, adjust visual charts pixel by pixel, and test every page to make sure nothing broke.

This project tested a faster, automated alternative. Raw data files from Google Dataset Search were provided to Google Antigravity alongside clear instructions on what the dashboard should accomplish.

Working as an autonomous assistant, the AI tools handled the entire process from start to finish:
1. Understood the raw retail data and organized it into clean, connected tables.
2. Built 26 standard business calculations, including sales revenue, profit margins, and inventory levels.
3. Designed and formatted a 4-page visual dashboard with consistent color palettes, clean spacing, and clear layouts.
4. Checked all report pages against official Microsoft rules to guarantee that everything opens smoothly with zero errors.

---

## Quantifiable Efficiency: Manual Development vs. AI Agents

The table below breaks down the time required for each phase of dashboard creation, comparing traditional manual work in Power BI Desktop against the AI agent method.

| Development Stage | Traditional Manual Work (Power BI Desktop) | AI Agent Method (Antigravity + Microsoft Tools) | Time Saved |
| :--- | :--- | :--- | :--- |
| Data Preparation and Cleaning | 2 to 3 Hours (Clicking through Power Query menus, manual adjustments) | Under 3 Minutes (Automated data loading and transformation) | ~95% Faster |
| Connecting Data Tables | 1 to 2 Hours (Dragging relationship lines, setting connections manually) | Under 2 Minutes (Automatic table relationship setup) | ~95% Faster |
| Writing 26 Business Formulas | 4 to 6 Hours (Typing formulas, fixing syntax errors, organizing folders) | Under 5 Minutes (Automated formula creation and folder organization) | ~98% Faster |
| Building 4 Dashboard Pages | 6 to 10 Hours (Creating visuals, arranging cards, aligning charts, fixing margins) | Under 10 Minutes (Automated layout generation with consistent spacing) | ~98% Faster |
| Styling and Color Themes | 1 to 2 Hours (Picking color codes, setting fonts, testing visual contrast) | Under 1 Minute (Instant application of a clean editorial theme) | ~98% Faster |
| Quality Checks and Testing | 2 to 3 Hours (Clicking through tabs, checking numbers, hunting for visual bugs) | Under 2 Minutes (Automated error checks against official Microsoft standards) | ~90% Faster |
| TOTAL TURNAROUND TIME | 16 to 26 Hours | 30 to 45 Minutes | Over 95% Saved (20+ Hours) |

Beyond saving time, this approach offers three practical benefits for business teams:
* Fewer Human Errors: Automated checks catch mistakes early, such as broken formulas or misaligned charts, before anyone sees the report.
* Easy Team Collaboration: The dashboard is saved as open text files instead of a locked binary file, making it easy to track changes, review updates, and collaborate using GitHub.
* Reusable for Future Projects: The same prompts and guidance can be applied to new datasets or other departments in minutes, turning days of work into quick turnaround tasks.

---

## Tech Stack & Tooling

Google Antigravity
The primary AI coding assistant that orchestrated the project. Antigravity read the raw data files, interpreted the business requirements, wrote the underlying code, and ran automated quality checks.

Microsoft Power BI Modeling Tools
Tools provided by Microsoft that allow AI assistants to build and modify Power BI data models directly in code, without needing to click through the user interface.

Microsoft Skills for Fabric
A set of best-practice guides created by Microsoft. These taught the AI assistant how to structure data tables cleanly, follow proven dashboard layout patterns, and choose accessible color themes.

Power BI Developer Mode (.pbip)
A modern Power BI format that saves reports as open, readable text files. This open format allows AI assistants to build and edit reports directly.

Microsoft Validation Tools
Automated utilities that test the report files against Microsoft standards, confirming that the finished dashboard opens smoothly with zero errors.

Google Dataset Search
The public data search engine used to find the initial retail records, which were then customized and scaled to reflect real-world business volume.

---

## How to Open and View the Solution

1. Clone or download this repository to your computer:
   ```bash
   git clone https://github.com/FedericoBucayan/Retail-Ecommerce-Analytics.git
   ```

2. Open the project in Power BI Desktop:
   Double-click Retail_Ecommerce_Analytics.pbip from Windows Explorer. All tables, calculations, filters, and report pages will load automatically.

3. Run the automated quality check:
   Double-click scripts/Validate_Report.bat to run the Microsoft validator and confirm that all report pages pass with zero errors.

4. View the PDF export without Power BI:
   Open Retail_Ecommerce_Analytics_PBI_PDF.pdf to review a full-resolution, four-page view of the completed dashboard.

---

Designed and Developed by Federico Bucayan | 2026
