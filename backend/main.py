# backend/main.py — InterviewIQ FastAPI Backend (Starter Scaffold)
# -------------------------------------------------------------------
# This file provides the same mock data the React front-end currently
# generates client-side, but served over proper HTTP endpoints so you
# can swap in real logic (DB queries, LLM calls, resume parsing) one
# endpoint at a time without touching the front-end.
# -------------------------------------------------------------------

import random
import math
from typing import List, Optional

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# ─── App Setup ────────────────────────────────────────────────────────
app = FastAPI(
    title="InterviewIQ API",
    version="0.1.0",
    description="Backend API for the InterviewIQ mock-interview platform.",
)

# Allow the Vite dev server (localhost:5173) to call us
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ─── Data Models (Pydantic) ──────────────────────────────────────────
class SetupData(BaseModel):
    domain: str = "Computer Science"
    role: str = "Software Engineer"
    experienceLevel: str = "Mid-Level"
    type: str = "Technical"
    difficulty: str = "Medium"
    questionCount: int = 5
    persona: str = "sarah"
    focusAreas: List[str] = []


class QuestionItem(BaseModel):
    id: str
    question: str
    duration: int
    hint: str = ""


class GradeRequest(BaseModel):
    setup: SetupData
    questions: List[QuestionItem]
    answers: List[str]


# ─── Static Data (mirrors src/services/*.js) ─────────────────────────

INTERVIEWER_PERSONAS = {
    "sarah": {
        "id": "sarah",
        "name": "Sarah Chen",
        "role": "Staff Engineer & Tech Lead",
        "company": "InterviewIQ (ex-Netflix)",
        "avatar": "https://images.unsplash.com/photo-1494790108377-be9c29b29330?auto=format&fit=crop&q=80&w=120",
        "description": "Encouraging but detailed. Focuses heavily on clean architecture, performance, code readability, and deep problem-solving skills.",
        "accentColor": "text-indigo-400",
        "borderColor": "border-indigo-500/30",
        "bgColor": "bg-indigo-950/20",
        "glowColor": "glow-primary",
        "voicePitch": 1.0,
        "voiceRate": 1.0,
    },
    "david": {
        "id": "david",
        "name": "David Vance",
        "role": "Engineering Manager",
        "company": "InterviewIQ (ex-Stripe)",
        "avatar": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&q=80&w=120",
        "description": "Pragmatic, product-minded engineering manager. Focuses on execution, scope management, scalability, trade-offs, and communication.",
        "accentColor": "text-violet-400",
        "borderColor": "border-violet-500/30",
        "bgColor": "bg-violet-950/20",
        "glowColor": "glow-secondary",
        "voicePitch": 0.9,
        "voiceRate": 0.95,
    },
    "techbot": {
        "id": "techbot",
        "name": "TechBot v2.4",
        "role": "Autonomous AI Assessor",
        "company": "InterviewIQ Core Protocol",
        "avatar": "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?auto=format&fit=crop&q=80&w=120",
        "description": "Strict, analytical, and highly structured. Evaluates edge cases, algorithmic complexities, and rigorous logic without emotional bias.",
        "accentColor": "text-cyan-400",
        "borderColor": "border-cyan-500/30",
        "bgColor": "bg-cyan-950/20",
        "glowColor": "glow-accent",
        "voicePitch": 1.2,
        "voiceRate": 1.1,
    },
}

CAREER_DOMAINS = {
    "Computer Science": [
        "Software Engineer", "Frontend Developer", "Backend Developer",
        "Full Stack Developer", "Mobile App Developer", "DevOps Engineer",
        "Cloud Engineer", "Cybersecurity Analyst", "Network Engineer",
        "Database Engineer",
    ],
    "Artificial Intelligence": [
        "AI Engineer", "Machine Learning Engineer", "Deep Learning Engineer",
        "NLP Engineer", "Computer Vision Engineer", "Prompt Engineer",
    ],
    "Data & Analytics": [
        "Data Analyst", "Data Scientist",
        "Business Intelligence Analyst", "Data Engineer",
    ],
    "Finance": [
        "Financial Analyst", "Investment Analyst",
        "Equity Research Analyst", "Financial Planning Analyst",
    ],
    "Science & Education": [
        "Chemistry Teacher", "Physics Teacher", "Biology Teacher",
        "Mathematics Teacher", "Computer Science Teacher",
    ],
}

QUESTION_DATABASE = {
    "Computer Science": {
        "technical": [
            {"question": "Explain React's reconciliation algorithm and virtual DOM diffing. Why are keys important when rendering dynamic arrays?", "duration": 120, "hint": "Mention time complexity, element identity, and sibling reordering."},
            {"question": "What is the event loop in JavaScript? How does the browser handle microtasks (Promises) vs macrotasks (setTimeout)?", "duration": 150, "hint": "Talk about the call stack, task queues, and render cycles."},
            {"question": "Describe how closures work in JavaScript and how they can potentially cause memory leaks in modern single-page apps.", "duration": 120, "hint": "Discuss lexical scoping, garbage collection references, and clearing intervals."},
            {"question": "How would you optimize the Core Web Vitals (specifically LCP, INP, and CLS) for a large enterprise dashboard application?", "duration": 180, "hint": "Mention code splitting, dynamic imports, font swaps, and element sizing."},
            {"question": "What are the main architectural differences between SQL and NoSQL databases? In what scenarios would you choose one over the other?", "duration": 150, "hint": "Discuss transactions, ACID compliance, horizontal scaling, and document structures."},
        ]
    },
    "Artificial Intelligence": {
        "technical": [
            {"question": "Explain the self-attention mechanism in Transformer architectures. How does it resolve sequence order details?", "duration": 180, "hint": "Mention query-key-value projections, scaled dot-product attention, and positional encodings."},
            {"question": "What is the core difference between fine-tuning a Large Language Model and applying Retrieval-Augmented Generation (RAG)?", "duration": 150, "hint": "Analyze memory-weight updates, context window limitations, and latency costs."},
            {"question": "How do you handle issues of vanishing or exploding gradients when training deep neural network architectures?", "duration": 120, "hint": "Mention residual connections, batch normalization, gradient clipping, and activation functions."},
            {"question": "Explain the difference between supervised learning, unsupervised learning, and reinforcement learning.", "duration": 120, "hint": "Discuss labeled datasets, clustering algorithms, reward functions, and policy gradients."},
        ]
    },
    "Data & Analytics": {
        "technical": [
            {"question": "How would you write an optimized SQL query to perform a rolling average calculation over user activities without subqueries?", "duration": 150, "hint": "Mention window functions, PARTITION BY, and ROWS BETWEEN."},
            {"question": "What is the difference between a dimensional model (star schema) and a normalized model (snowflake schema)? When would you use each?", "duration": 120, "hint": "Discuss database normalization, query join performance, and data warehousing."},
            {"question": "How do you clean and preprocess a raw dataset containing significant levels of missing data and outliers?", "duration": 120, "hint": "Mention imputation methods, z-scores, interquartile range (IQR), and scaling."},
        ]
    },
    "Finance": {
        "technical": [
            {"question": "Walk me through how you build a discounted cash flow (DCF) model and how you calculate the Weighted Average Cost of Capital (WACC).", "duration": 180, "hint": "Explain free cash flows, terminal value, cost of equity (CAPM), and cost of debt."},
            {"question": "How do the three financial statements link together? Walk me through how a $10 depreciation expense flows through them.", "duration": 150, "hint": "Track changes from income statement net income, cash flow adjustments, to balance sheet assets."},
            {"question": "Explain the capital asset pricing model (CAPM) and how we would estimate beta for a private company.", "duration": 120, "hint": "Mention risk-free rate, market risk premium, and pure-play comparable public companies."},
        ]
    },
    "Science & Education": {
        "technical": [
            {"question": "How do you explain the concept of chemical equilibrium and Le Chatelier's principle to a class of high school students?", "duration": 120, "hint": "Focus on analogies, pressure/temperature stresses, and reversible reactions."},
            {"question": "Describe a laboratory experiment you would design to teach students about acid-base titrations. What indicators would you use?", "duration": 150, "hint": "Discuss safety protocols, buret setups, phenolphthalein, and pH curves."},
            {"question": "How do you structure a lesson plan on quadratic equations for students with diverse mathematical backgrounds?", "duration": 120, "hint": "Mention differentiated learning, visual graphs, factoring, and the quadratic formula."},
        ]
    },
    "behavioral": [
        {"question": "Describe a situation where you had a disagreement with a team member regarding a technical implementation. How did you resolve it?", "duration": 120, "hint": "Focus on communication, objective criteria, and team alignment."},
        {"question": "Tell me about a project that failed or had a significant setback. What was your role, and what steps did you take to mitigate it?", "duration": 150, "hint": "Show extreme ownership, constructive review, and prevention systems."},
        {"question": "How do you handle scope creep and tight deadlines when working on critical product launches?", "duration": 150, "hint": "Emphasize data-driven estimations, prioritization matrices, and stakeholder communication."},
    ],
    "system-design": [
        {"question": "Design a highly available and scalable notification service capable of sending billions of push alerts daily. How do you handle delivery deduplication?", "duration": 180, "hint": "Message queues (Kafka), idempotency keys, rate limiters, mail delivery providers."},
        {"question": "Design a real-time collaborative document editor like Google Docs. How do you manage concurrent editing conflicts?", "duration": 180, "hint": "Operational Transformation (OT) vs Conflict-free Replicated Data Types (CRDTs), WebSockets."},
        {"question": "Design a distributed rate limiter middleware for a high-traffic API gateway. What algorithms would you choose?", "duration": 180, "hint": "Token bucket vs leaky bucket, Redis cluster counters, sliding window logs."},
    ],
}


# ─── Helpers ──────────────────────────────────────────────────────────

def get_questions_for_setup(
    q_type: str = "technical",
    difficulty: str = "medium",
    domain: str = "Computer Science",
) -> list[dict]:
    """Return a list of questions matching the requested type/domain."""
    norm_type = q_type.lower()

    if norm_type == "behavioral":
        questions = list(QUESTION_DATABASE["behavioral"])
    elif norm_type in ("system design", "system-design"):
        questions = list(QUESTION_DATABASE["system-design"])
    elif norm_type == "mixed":
        domain_tech = (
            QUESTION_DATABASE.get(domain, {}).get("technical")
            or QUESTION_DATABASE["Computer Science"]["technical"]
        )
        questions = (
            domain_tech[:2]
            + QUESTION_DATABASE["behavioral"][:1]
            + QUESTION_DATABASE["system-design"][:1]
        )
    else:
        questions = list(
            QUESTION_DATABASE.get(domain, {}).get("technical")
            or QUESTION_DATABASE["Computer Science"]["technical"]
        )

    diff_prefix = ""
    if difficulty.lower() == "easy":
        diff_prefix = "[Fundamentals] "
    elif difficulty.lower() == "hard":
        diff_prefix = "[Advanced Theory] "

    return [
        {
            "id": f"q_{norm_type}_{idx}",
            "question": f"{diff_prefix}{q['question']}",
            "duration": q["duration"],
            "hint": q.get("hint", ""),
        }
        for idx, q in enumerate(questions)
    ]


def generate_feedback_report(
    setup: dict, questions_list: list[dict], answers_list: list[str]
) -> dict:
    """Produce a mock grading report identical to resultsApi.js output."""
    scores = {
        "technicalAccuracy": 75 + random.randint(0, 19),
        "communication": 80 + random.randint(0, 14),
        "depth": 70 + random.randint(0, 24),
        "timeManagement": 85 + random.randint(0, 11),
    }
    overall = round(sum(scores.values()) / 4)

    q_type = setup.get("type", "technical").lower()
    breakdowns = []
    for idx, q in enumerate(questions_list):
        answer = answers_list[idx] if idx < len(answers_list) else "No answer provided."
        score_val = 70 + (idx * 6 + len(answer) % 20) % 25

        if q_type == "technical":
            feedback = (
                "Good usage of technical terms. You successfully touched on key structural mechanics. "
                "Your description was logical and easy to follow."
            )
            suggestions = [
                "Include more concrete examples of how you applied this in a past production system.",
                "Mention the time complexity or rendering overhead details to showcase senior depth.",
            ]
        elif q_type == "behavioral":
            feedback = (
                "Strong narrative alignment. You set the context and actions clearly. "
                "Great usage of the STAR framework (Situation, Task, Action, Result)."
            )
            suggestions = [
                "Provide more specific metrics on the outcome (e.g. numbers, percentages, times saved).",
                "Explain what you would do differently in hindsight.",
            ]
        else:
            feedback = (
                "Your high level block diagram elements were well described. "
                "Clear explanation of network interfaces and data stores."
            )
            suggestions = [
                "Discuss scalability limitations and point out single points of failure (SPOFs).",
                "Consider caching and database read/write ratios.",
            ]

        breakdowns.append(
            {
                "id": q.get("id", f"q_{idx}"),
                "question": q["question"],
                "userAnswer": answer,
                "score": score_val,
                "idealConcepts": q.get("hint", "Core concepts related to the topic."),
                "feedback": feedback,
                "suggestions": suggestions,
                "strengths": (
                    "Detailed response structure, use of industry terminology."
                    if len(answer) > 80
                    else "Direct, straightforward communication."
                ),
            }
        )

    return {
        "overallScore": overall,
        "categories": scores,
        "breakdown": breakdowns,
        "interviewerComments": (
            f"You performed well during this {setup.get('type', 'technical')} interview. "
            "Your structural clarity stands out, and you communicate technical decisions with "
            "strong confidence. Focus on providing quantitative evidence in behavioral tracks "
            "and detailing edge cases in technical tracks to elevate your performance further."
        ),
        "personaId": setup.get("persona", "sarah"),
        "setupData": setup,
        "strengths": [
            "Clear articulation of core concepts",
            "Good structural organisation of answers",
            "Confident communication style",
        ],
        "weaknesses": [
            "Could provide more concrete production examples",
            "Edge-case analysis could be deeper",
        ],
        "plan": [
            {"topic": "System Design Patterns", "desc": "Study distributed caching, message queues, and load balancing strategies."},
            {"topic": "Algorithmic Complexity", "desc": "Practice Big-O analysis for common data structures and sorting algorithms."},
            {"topic": "Behavioural Storytelling", "desc": "Prepare 5 STAR-framework stories with quantifiable outcomes."},
        ],
    }


# ─── Endpoints ────────────────────────────────────────────────────────

@app.get("/")
async def root():
    return {"status": "ok", "service": "InterviewIQ API", "version": "0.1.0"}


@app.get("/healthz")
async def healthz():
    return {"status": "healthy"}


# --- Personas ---
@app.get("/api/personas")
async def get_personas():
    """Return the list of available AI interviewer personas."""
    return INTERVIEWER_PERSONAS


# --- Career Domains & Roles ---
@app.get("/api/domains")
async def get_domains():
    """Return a list of supported career domain names."""
    return list(CAREER_DOMAINS.keys())


@app.get("/api/domains/{domain}/roles")
async def get_roles(domain: str):
    """Return the roles available under a specific domain."""
    roles = CAREER_DOMAINS.get(domain)
    if roles is None:
        raise HTTPException(status_code=404, detail=f"Domain '{domain}' not found.")
    return roles


# --- Questions ---
@app.get("/api/questions")
async def get_questions(
    domain: str = "Computer Science",
    difficulty: str = "medium",
    type: str = "technical",
    count: Optional[int] = None,
):
    """Return a set of mock interview questions."""
    qs = get_questions_for_setup(type, difficulty, domain)
    if count and count < len(qs):
        qs = qs[:count]
    return qs


# --- Resume Upload ---
@app.post("/api/resume")
async def upload_resume(
    file: UploadFile = File(...),
    jobTitle: str = Form("Software Engineer"),
    jobDescription: str = Form(""),
):
    """
    Accept a resume file and return a mock analysis report.
    In production, replace the body with real PDF parsing (pdfminer,
    docx2txt) and NLP-based skill extraction (spaCy, sentence-transformers).
    """
    common_keywords = ["React", "TypeScript", "JavaScript", "Tailwind", "Git", "REST API", "Vite", "State Management"]
    missing_keywords = ["Next.js", "GraphQL", "Docker", "CI/CD", "Jest/Cypress", "System Design"]

    length_score = min(25, len(jobTitle) + len(jobDescription) // 10)
    base_match = 65 + (length_score % 20)

    return {
        "matchPercentage": base_match,
        "fileName": file.filename,
        "skillsMatched": common_keywords[: 4 + (base_match % 4)],
        "skillsMissing": missing_keywords[: 2 + (base_match % 3)],
        "summary": (
            f"Your resume demonstrates a strong foundational match for the {jobTitle} role. "
            "Key highlights include hands-on experience with modern frontend practices and "
            "responsive design systems. To improve compatibility, consider adding more "
            "references to full-stack integration and testing tools."
        ),
        "scoreBreakdown": {
            "formatting": 90,
            "skills": base_match + 2,
            "experienceRelevance": base_match - 5,
            "impactMetrics": 72,
        },
        "recommendations": [
            "Quantify accomplishments with metrics (e.g., 'Optimized render cycles leading to a 30% reduction in TTI').",
            f"Add explicit mentions of {missing_keywords[0]} and {missing_keywords[1]} to pass recruiter screening.",
            "Include testing workflows such as unit tests with Vitest/Jest or end-to-end integration.",
        ],
    }


# --- Grading ---
@app.post("/api/grade")
async def grade(req: GradeRequest):
    """
    Grade an interview session and return a detailed feedback report.
    In production, call Claude / OpenAI server-side here with your
    secret API key instead of the mock generator.
    """
    report = generate_feedback_report(
        req.setup.model_dump(),
        [q.model_dump() for q in req.questions],
        req.answers,
    )
    return report


# ─── Entry Point ──────────────────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
