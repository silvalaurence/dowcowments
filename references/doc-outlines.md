# Document outlines

The complete set, from Chapters 1 to 4 of the course book. Folders follow the five process groups (initiating, planning, executing, monitoring and controlling, closing) plus an optional Scrum folder.

How to read this file:
- File names go in `docs/source/<folder>/` as `.md` (the built `.docx` goes in the same folder one level up).
- Section names after the colon become the document's `#` headings, in order. Columns of a table are in parentheses. Drop a section only if it truly does not apply, and say why in one sentence instead of leaving a blank.
- Documents marked (recurring) are created again each time: one per week, per change, per sprint. Add a number or date to the file name, for example `01_Progress_Report_2026-11-07`.
- Every document ends with Revision History (Version, Date, Description, Author).
- Contents of this file: 1_Initiating, 2_Planning, 3_Executing, 4_Monitoring_Controlling, 5_Closing, Scrum, Optional extras, How Scrum maps to the formal documents.

---

## 1_Initiating

**01_Business_Case**: Introduction and Background; Business Objective; Current Situation and Problem or Opportunity; Critical Assumptions and Constraints; Analysis of Options and Recommendation (Option, Description, Advantages, Disadvantages; always include "do nothing"); Preliminary Project Requirements; Budget Estimate and Financial Analysis (cost assumptions table: Item, Hours or Quantity, Rate, Cost; benefit assumptions; then paste the output of `finance.py` for the NPV, ROI, and payback table, and insert the payback chart); Schedule Estimate; Potential Risks.

**02_Project_Selection**: Strategic Context (which organization or course goal the project supports); SWOT Analysis (Category, Item; categories Strengths, Weaknesses, Opportunities, Threats); Potential Projects Identified (Project, Need It Addresses, Type: problem, opportunity, or directive); Selection Criteria and Weights (Criterion, Weight %; weights total 100); Weighted Scoring Model (Criterion, Weight, one score column per project, last row the weighted total = sum of weight x score); Need, Funding, and Will Check (Question, Answer); Balanced Scorecard (Perspective: customer, financial, internal, growth and learning; Goal; Measure; include only if the teacher or organization uses one); Decision and Reason.

**03_Statement_of_Work**: Business Need; Product or Service Description; Summary of Requirements and Characteristics; Alignment with Strategic Goals; Assumptions.

**04_Project_Charter** (keep to one or two pages): Project Title and Authorization Date; Start and Finish Dates; Budget Information; Project Manager (name and contact); Project Objectives; Success Criteria; Approach; Key Milestones; Roles and Responsibilities (Name, Role, Position, Contact); Sign-off (Name, Signature, Date); Stakeholder Comments.

**05_Stakeholder_Register**: Purpose; Stakeholders (Name, Position, Internal or External, Project Role, Contact). Leave out anything sensitive such as support level or influence.

**06_Stakeholder_Management_Strategy**: set `status: Confidential`. Purpose; Strategy (Name, Level of Interest, Level of Influence, How We Will Gain Support or Reduce Obstacles). Mention to the user that the book treats this as private.

**07_Kickoff_Meeting**: Meeting Objective; Date, Time, and Place; Agenda (Time, Topic, Lead); Action Items (Action, Assigned To, Due Date); Next Meeting Date and Time; Meeting Minutes (key decisions and action items, sent to everyone within 24 hours).

---

## 2_Planning

**01_Team_Contract**: Code of Conduct; Participation; Communication; Problem Solving; Meeting Guidelines; Sign-off (Name, Signature, Date).

**02_Project_Management_Plan**: Introduction (project name; short description and the need it addresses; sponsor; project manager and key team members; deliverables; reference materials, including the other plans; definitions and acronyms); Project Organization (organizational chart as a nested list; project responsibilities; other process information); Management Approach (management objectives; project controls such as status reviews and change control; risk management summary; staffing); Technical Approach (life cycle model, for example waterfall, spiral, incremental, prototyping, RAD, or agile/Scrum, and why it was chosen; tools and technologies; technical documentation standards); Work to Perform (major work packages; key deliverables and quality expectations; assumptions); Schedule Summary (summary schedule, detailed schedule reference, assumptions); Budget Summary (summary budget, detailed budget reference, assumptions). For software projects this follows the IEEE 1058 outline: Overview, Project Organization, Managerial Process, Technical Process, Supporting Processes.

**03_Requirements_Document**: Purpose; How Requirements Are Collected, Approved, and Changed; Requirements (ID, Requirement, Type: functional or non-functional, Priority, Source, Status).

**04_Requirements_Traceability_Matrix**: Purpose; Matrix (Requirement ID, Requirement, Source, WBS Item, Design Item, Test Case ID, Status).

**05_Scope_Statement**: Project Summary and Justification; Product Characteristics and Requirements (numbered, each with a measurable detail); Summary of Deliverables (Project Management Deliverables list; Product Deliverables list); Out of Scope; Project Success Criteria (scope, time, cost, and what the sponsor wants).

**06_Scope_Management_Plan**: How Scope Is Defined; How the WBS Is Created and Maintained; How Scope Is Verified and Accepted; How Scope Changes Are Controlled.

**07_Work_Breakdown_Structure**: Purpose; WBS (nested numbered list, all work in the project; the book's example uses the five process groups as top-level groups, and a Scrum team may group by epic or sprint); WBS Dictionary (WBS ID, Work Package, Description, Owner, Deliverable, Due Date).

**08_Project_Schedule**: Overview; Milestone List (Milestone, Due Date, Owner, Status); Task Schedule (ID, Task, Start, End, Duration, Owner, Depends On; dates as YYYY-MM-DD; this table feeds `make_charts.py`); Gantt Chart (picture); Network Diagram and Critical Path (picture, then one sentence naming the critical path); Schedule Assumptions; How the Schedule Is Tracked and Changed.

**09_Cost_Estimate_and_Baseline**: Summary (total budget); Cost Estimate (Item, Quantity or Hours, Rate, Total); Cost Baseline by Period (Period, Planned Cost, Cumulative Planned Cost); Funding; Assumptions; How Costs Are Tracked and Changed.

**10_Quality_Management_Plan**: Quality Standards and Goals; Quality Metrics (Metric, Target, How Measured); Quality Checklists; Quality Assurance Activities (Activity, Who, How Often); Quality Control Activities; Process Improvement.

**11_Human_Resource_Plan**: Project Organizational Chart (nested list); Roles and Responsibilities (Name, Role, Responsibilities); Responsibility Assignment Matrix (Task, then one column per person with R = responsible, A = approves, C = consulted, I = informed); Staffing Plan and Resource Histogram (Person, hours per month, one column per month); Training Needs.

**12_Communications_Management_Plan**: Communication Needs (Stakeholder, Information Needed, Method, Frequency, Owner); Meetings; Reports (weekly progress report, milestone report, final report); Tools and Project Web Site or Shared Folder; Document Storage and Naming; Escalating Issues; Glossary.

**13_Risk_Management_Plan**: Approach; Roles; Probability and Impact Scales (Level, Probability Meaning, Impact Meaning); Probability and Impact Matrix (3 by 3 table, rows probability, columns impact, each cell Low, Medium, or High); How Risks Are Tracked and Reviewed.

**14_Risk_Register**: Purpose; Prioritized Risks (Rank, Risk, Root Cause, Warning Signs, Probability, Impact, Response Strategy, Owner, Status). Keep high and medium risks, and track the top ten.

**15_Procurement_Management_Plan**: What Will Be Bought or Outsourced; Make-or-Buy Decisions (Item, Decision, Reason); Statement of Work for Purchases; Source Selection Criteria (Criterion, Weight); Contract Type; Request for Proposal Outline (Introduction, Requirements, Instructions to Suppliers, Evaluation Criteria, Schedule); Procurement Schedule. If nothing is bought, write one paragraph saying so and why.

**16_Change_Control_Plan**: Purpose; Change Process (numbered steps: submit request, evaluate impact on scope, time, cost, and quality, decide, update plans, tell everyone); Change Control Board (Name, Role); Who Can Approve What (Type of Change, Approver, Time Limit); Configuration Management (what is controlled, version naming, where it is stored); How Changes Are Communicated; Change Log (ID, Date, Description, Requested By, Decision, Status).

**17_Test_Plan** (software projects): Purpose; Scope of Testing; Test Environment; Responsibilities; Test Cases (ID, Feature, Steps, Expected Result, Requirement ID); Defect Reporting; Pass and Fail Criteria.

---

## 3_Executing

**01_Milestone_Report** (recurring): Report Date; Milestones (Milestone, Date, Status, Responsible, Issues and Comments; group by process group); Summary in two sentences.

**02_Technical_Design_Document** (software projects): Overview; Architecture; Data Design; Interface Design; Security; Tools and Technologies; Design Decisions and Reasons.

**03_Test_Report**: Summary; Test Results (Test Case ID, Expected, Actual, Pass or Fail); Defects Found and Fixed (ID, Description, Status); Conclusion.

**04_Benefits_Measurement_Plan**: Purpose; What Will Be Measured (Measure, Starting Value, Target, How Measured, When, Who); Expected Financial Benefits (copy from Business Case); Review Schedule.

---

## 4_Monitoring_Controlling

**01_Progress_Report** (recurring, weekly): Reporting Period and Team Member; Work Completed This Week; Work Planned for Next Week; What Is Going Well and Why; What Is Not Going Well and Why; Suggestions and Issues; Project Changes.

**02_Change_Request_Form** (recurring, one per change): Request ID, Date, and Requested By; Description of the Change; Reason; Impact (Area: scope, time, cost, quality, risk; Effect); Alternatives Considered; Decision (Approved, Rejected, or Deferred; Approver; Date); Follow-up Actions.

**03_Issue_Log**: Purpose; Issues (ID, Date Raised, Issue, Raised By, Owner, Priority, Due Date, Status, Resolution).

**04_Expectations_Management_Matrix**: Purpose; Matrix (Stakeholder, Expectation, Importance, How We Will Meet It, Status).

**05_Earned_Value_Report** (recurring): As-of Date; Budget at Completion (BAC); Earned Value Table (Work Item, Planned Value PV, Earned Value EV, Actual Cost AC, Cost Variance CV = EV - AC, Schedule Variance SV = EV - PV, CPI = EV / AC, SPI = EV / PV); Forecast (Estimate at Completion EAC = BAC / CPI); Plain-Words Summary (over or under budget, ahead of or behind schedule, and what we will do about it).

**06_Phase_Exit_Review** (recurring, one per phase): Phase Reviewed and Date; Reviewers; Deliverables Completed (Deliverable, Status); Review Questions (Question, Answer; still meets the business need, still within budget and schedule, main open risks); Decision (continue, redirect, or stop) and Reason; Actions.

---

## 5_Closing

**01_Lessons_Learned_Report**: Project Information (name, sponsor, project manager, dates, final budget); 1. Did the project meet scope, time, and cost goals?; 2. What were the success criteria listed in the scope statement? (quote them); 3. Did we meet the success criteria?; 4. In terms of managing the project, what were the main lessons learned?; 5. One example of what went right; 6. One example of what went wrong; 7. What will we do differently on the next project?

**02_Client_Acceptance_Form**: Project; Deliverables Accepted (Deliverable, Accepted Yes or No); Comments; Sign-off (Name, Role, Signature, Date).

**03_Final_Project_Report**: Project Objectives; Summary of Project Results; Original and Actual Start and End Dates (Item, Original, Actual); Original and Actual Budget (Item, Original, Actual); Project Assessment (why we did the project, what we produced, whether it was a success, what went right and wrong); Transition Plan (issues to solve before real use, who supports the product, support costs); Annual Project Benefits Measurement Approach; Attachments (A: project management documents, listing every document in the index; B: product-related documents such as survey results, design, test reports, roll-out information).

**04_Contract_Closeout_Report** (only if something was bought): Contract and Supplier; Deliverables Received; Payments (Date, Amount, Status); Issues; Date Closed and Sign-off.

**05_Post_Implementation_Review**: Review Date (about a year after completion); Original Goals; Results Compared to Projections (Measure, Projected, Actual, Difference); Benefits Realized; Lessons; Recommendations.

**06_Final_Presentation_Outline**: Slides (Slide Number, Title, Key Points, Speaker): 1 Title and team; 2 Objectives; 3 What we built; 4 Schedule, planned and actual; 5 Budget, planned and actual; 6 Results and benefits; 7 Lessons learned; 8 Transition and next steps; 9 Questions. The slides themselves are made as a separate PowerPoint when the user asks.

---

## Scrum (only if the team uses Scrum)

**01_Product_Vision**: Vision Statement; Target Users; Key Goals; Success Measures; Constraints.

**02_Product_Backlog**: Purpose; Definition of Done; Backlog (ID, User Story written "As a ..., I want ..., so that ...", Priority, Estimate in story points, Sprint, Status).

**03_Release_Plan**: Release Goal; Sprints (Sprint, Dates, Goal, Planned Backlog Items); Milestones; Assumptions.

**04_Sprint_Plan** (recurring, one per sprint): Sprint Goal; Dates; Team Capacity (Person, Available Hours); Sprint Backlog (ID, Task, Owner, Estimate, Status).

**05_Sprint_Review_and_Retrospective** (recurring, one per sprint): Sprint Goal and Result; Completed Items; Not Completed and Why; Feedback from the Review; What Went Well; What To Improve; Actions for Next Sprint (Action, Owner, Due Date).

---

## Optional extras (only if the teacher asks)

- **Quality_Control_Report** in 4_Monitoring_Controlling: defect counts by cause (Cause, Count, Percent, Cumulative Percent), sorted largest first like a Pareto chart, and what will be fixed first.
- **Breakeven_Sensitivity_Analysis** in 2_Planning: how NPV changes if benefits fall 10, 20, or 30 percent, and the benefit level where NPV reaches zero. Calculate with `finance.py` by changing `--benefits`.
- **Any product deliverable** named in the Scope Statement that has no document above (survey and results, promotion plan, roll-out plan, user manual, training plan) gets its own short document in 3_Executing.

---

## How Scrum maps to the formal documents

This mapping is not from the book. It helps a Scrum team explain its work in the formal vocabulary.

| Scrum | Formal document |
|---|---|
| Product vision | Project Charter |
| Product backlog | Scope Statement, Requirements Document |
| Release plan | Schedule (Gantt chart) and Milestone List |
| Sprint backlog | Work Breakdown Structure |
| Daily scrum | Weekly Progress Report |
| Sprint review | Milestone Report |
| Retrospective | Lessons Learned Report |
