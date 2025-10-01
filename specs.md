Perfect — let’s make this super clear for your IT partner: step-by-step, with a flow diagram, the team setup, the software stack, the parameters needed, and finally an example walk-through at micro-level detail.

⸻

Estimation Automation – End-to-End Flow

1. Input Stage: What OEM Sends
   • 2D Drawings: PDF/DWG with dimensions, tolerances, GD&T (quality requirements).
   • 3D Models: CAD files (.SLDPRT, .SLDASM, .STEP) containing full geometry.
   • Customer Requirements:
   • Material (e.g., AlSi7Mg alloy)
   • Quantity per year
   • Surface finish (e.g., anodizing, coating)
   • Special notes (e.g., leak-proofing, X-ray, testing).

⸻

2. Team Setup (Typical Estimation Team)
   • Design/Engineering – validates geometry, checks manufacturability.
   • Estimation Team – does cost calculations (casting, machining, tooling).
   • SCM Team – verifies vendor/partner pricing, updates rate cards.
   • Business Development (BD) – uses the final estimate to quote to OEM.

👉 With automation, the software does 70–80% of the work, humans only review.

⸻

3. Software Stack
   • CAD Platform: SolidWorks (OEM input files).
   • Extraction Tools:
   • SolidWorks API / Macros (extract geometry, BOM, properties).
   • Neutral CAD formats (STEP, IGES).
   • Geometry Analysis: PythonOCC, OpenCascade, Trimesh (open-source).
   • Estimation Engine: Python/AI models applying business logic (casting, machining, tooling).
   • Database: Stores part data, partner rates, past estimates, and actuals (e.g., PostgreSQL).
   • Integration: Inticore’s BOLT platform (UI + workflow + dashboards).

⸻

4. Parameters Needed for Automated Quotes
   1. From CAD / Drawings:
      • Volume, surface area, weight, bounding box
      • Hole count, threads, ribs, min radius, draft angles
      • BOM (if assembly)
      • GD&T & tolerance levels
   2. From Customer:
      • Material grade
      • Annual quantity (batch size matters for cost/lead time)
      • Special treatments/finishes
   3. From Inticore Database:
      • Partner machine rates (₹/hr)
      • Alloy cost (₹/kg)
      • Process yield percentages (per casting type)
      • Tooling cost models (by size & complexity)

⸻

5. Process Flow Diagram

OEM Customer
│
▼
Receives 2D Drawings + 3D Models
│
▼
CAD Extraction Gateway
(SolidWorks API → STEP/CSV/JSON)
│
▼
Geometry Analysis Engine
(volume, weight, features, BOM, notes)
│
▼
Estimation Engine
┌────────────────────────────┐
│ Casting Model │
│ Machining Model │
│ Tooling Model │
│ Finishing/Inspection Model │
└────────────────────────────┘
│
▼
Cost Breakdown & Lead Time
(Material + Conversion + Tooling + Overheads)
│
▼
Review Panel
(red flags: no draft, thin ribs, tight tolerances)
│
▼
BOLT Dashboard
(final cost, lead time, quotation PDF/Excel)

⸻

6. Micro-Level Example

OEM Input
• Customer: Automotive OEM
• Part: Gearbox housing
• Files: STEP file + 2D drawing PDF
• Requirements:
• Material: AlSi10Mg
• Qty: 10,000 per year
• Finish: Anodized, leak test required

⸻

Step 1 – CAD Extraction
• CAD API exports:
• Volume = 1.8e6 mm³
• Surface Area = 0.95 m²
• Bounding Box = 220 × 180 × 160 mm
• Features: 36 holes, 2 threaded holes, 4 ribs, min radius 2 mm, draft angle = OK
• Mass (net weight) = 4.8 kg

⸻

Step 2 – Casting Model
• Process chosen: Gravity Die Casting (GDC)
• Material density: 2.68 g/cc
• Yield = 70% (GDC standard, part complexity OK)
• Gross weight = 4.8 / 0.70 = 6.9 kg
• Alloy price = ₹290/kg → Material cost = ₹2,000

⸻

Step 3 – Machining Model
• Features → Machining cycle time:
• Holes: 36 × 0.25 min = 9 min
• Threads: 2 × 0.8 min = 1.6 min
• Profiles: 0.95 m² × 0.02 min/cm² = 19 min
• Setup: 15 min
• Total cycle = 45 min
• Machine rate (VMC): ₹800/hr → Machining cost = ₹600

⸻

Step 4 – Tooling Model
• Housing size requires a 2-cavity steel die with 2 sliders.
• Tooling cost estimate = ₹18,00,000 (amortized over 10,000 pcs → ₹180/pc).

⸻

Step 5 – Finishing & Testing
• Leak test: ₹40/pc
• Anodizing: ₹60/pc

⸻

Step 6 – Final Cost Breakdown
• Material = ₹2,000
• Machining = ₹600
• Tooling (amortized) = ₹180
• Finishing + Testing = ₹100
• Overheads + Scrap allowance = ₹120
• Total = ₹3,000 per piece
• Lead time = 8 weeks for tooling + 2 weeks for sample approval

⸻

Step 7 – Output
• System generates in BOLT:
• Detailed cost sheet
• Lead time
• Risks flagged (“High machining time – consider alternate design”)
• PDF quotation ready for BD team to send to OEM

⸻

✅ In simple words: The customer sends CAD → system extracts part details → AI converts them into process costs → system adds up costs → BOLT shows final quote instantly. Humans only review unusual cases
