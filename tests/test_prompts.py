"""
10 diverse test prompts for visual quality testing.
Every engine change gets tested against ALL of these.
If quality doesn't improve across the board, it's overfitting.
"""

TEST_PROMPTS = [
    {
        "id": "tech_saas",
        "prompt": "floom is the production layer for AI scripts. Paste Python from ChatGPT, get a live app with UI, API, MCP. Solo founder Fede De Ponte (scaled SCAILE to 600K ARR). Raising 200K FF at 8M cap SAFE.",
        "url": "https://floom.dev",
        "audience": "ff",
        "theme_override": None,
    },
    {
        "id": "consulting_b2b",
        "prompt": "GreenLeaf Consulting helps mid-market retailers reduce supply chain waste by 30%. $2M ARR, 15 enterprise clients including Whole Foods and Trader Joes. Team of 12 ex-McKinsey and BCG consultants. Raising $5M Series A.",
        "url": None,
        "audience": "vc",
        "theme_override": {"primary": "#1a2744", "headline_font": "Playfair Display", "body_font": "Inter"},
    },
    {
        "id": "consumer_app",
        "prompt": "Pebble is a social fitness app where friends bet on each other's workouts. 50K MAU, 4.8 star rating, 65% D7 retention. $200K MRR from premium subscriptions. Founded by two ex-Peloton PMs. Raising $3M seed from Andreessen Horowitz.",
        "url": None,
        "audience": "vc",
        "theme_override": {"primary": "#ec4899", "headline_font": "Inter", "body_font": "Inter"},
    },
    {
        "id": "fintech",
        "prompt": "Ledgr automates bookkeeping for freelancers using bank API connections and AI categorization. 8K paying users, $40/month ARPU, 2% monthly churn. Profitable since month 8. Raising $1.5M seed to expand to EU markets.",
        "url": None,
        "audience": "angel",
        "theme_override": {"primary": "#2563eb", "headline_font": "DM Serif Display", "body_font": "Inter"},
    },
    {
        "id": "healthcare",
        "prompt": "MedScribe uses AI to generate clinical notes from doctor-patient conversations in real time. 40 hospitals in pilot, 92% accuracy, saves doctors 2 hours per day. HIPAA compliant. Raising $10M Series A. Founded by a radiologist and an ex-Google NLP researcher.",
        "url": None,
        "audience": "vc",
        "theme_override": {"primary": "#0d9488", "headline_font": "Inter", "body_font": "Inter"},
    },
    {
        "id": "marketplace",
        "prompt": "CraftBridge connects independent artisans in developing countries directly with boutique retailers in the US and EU. 200 artisans, 45 retailers, $80K GMV last month, 15% take rate. Raising $500K pre-seed. Founded by a former Etsy product lead.",
        "url": None,
        "audience": "angel",
        "theme_override": {"primary": "#b45309", "headline_font": "Playfair Display", "body_font": "Inter"},
    },
    {
        "id": "devtools",
        "prompt": "Testwright generates end-to-end browser tests from natural language descriptions. Integrates with Playwright and Cypress. 2000 GitHub stars, 300 weekly active teams on the hosted version. $15K MRR. Raising $2M seed.",
        "url": None,
        "audience": "vc",
        "theme_override": None,
    },
    {
        "id": "edtech",
        "prompt": "Fluently is an AI language tutor that adapts to each student's mistakes in real time. 25K students across 12 universities. B2B model: $5 per student per month. NPS of 72. Raising $4M Series A to expand beyond Spanish to 5 more languages.",
        "url": None,
        "audience": "vc",
        "theme_override": {"primary": "#7c3aed", "headline_font": "DM Serif Display", "body_font": "Inter"},
    },
    {
        "id": "climate",
        "prompt": "CarbonLens provides satellite-based carbon credit verification for forest conservation projects. 15 projects verified, $800K revenue, partnerships with Stripe Climate and Shopify. Team includes 2 remote sensing PhDs. Raising $6M Series A.",
        "url": None,
        "audience": "vc",
        "theme_override": {"primary": "#15803d", "headline_font": "Inter", "body_font": "Inter"},
    },
    {
        "id": "agency_pitch",
        "prompt": "Velocity is a growth marketing agency specializing in B2B SaaS. 35 clients, $3M annual revenue, 90% retention rate. Average client sees 3x pipeline increase in 6 months. Team of 20 across SEO, paid, and content. Looking for a strategic partner to invest $1M for equity and help scale to $10M.",
        "url": None,
        "audience": "angel",
        "theme_override": {"primary": "#171717", "headline_font": "Inter", "body_font": "Inter"},
    },
]
