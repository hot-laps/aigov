from pydantic import BaseModel

import core


UNSURE = "Not sure yet"
OTHER = "Other"
RISK_ORDER = {"medium": 1, "high": 2}


class Option(BaseModel):
    label: str
    risk: str | None = None
    rubric: str = ""
    reason: str = ""


class Question(BaseModel):
    key: str
    field: str
    section: str
    label: str
    kind: str
    prefix: str = ""
    help: str = ""
    options: list[Option] = []


def option(label, risk=None, rubric="", reason=""):
    return Option(label=label, risk=risk, rubric=rubric, reason=reason)


def question(key, field, section, label, kind, options=(), prefix="", help=""):
    return Question(key=key, field=field, section=section, label=label, kind=kind, prefix=prefix, help=help, options=list(options))


SECTIONS = ["Basics", "Users and affected people", "Data", "Outputs and autonomy", "Controls"]

QUESTIONS = [
    question("title", "title", "Basics", "Use-case title", "text", help="A short name, e.g. Research digest assistant"),
    question("owner", "owner", "Basics", "Owner or team", "text"),
    question("purpose_category", "purpose", "Basics", "What will AI help with?", "multi", prefix="Purpose", options=[
        option("Research and summarization"),
        option("Drafting documents or emails"),
        option("Meeting notes and transcription", "medium", "D1", "Meeting recordings often capture personal or confidential discussion."),
        option("Data analysis and reporting"),
        option("Code assistance"),
        option("Customer support", "medium", "D4", "Customer-facing use has meaningful consequences when outputs are wrong."),
        option("Hiring, HR, or employee evaluation", "high", "D4", "Employment decisions are a high-impact category in the rubric."),
        option("Legal or contract review", "medium", "D1", "Legal material is often confidential or privileged."),
        option("Financial decisions or approvals", "high", "D4", "Material financial consequences are a high-impact category."),
        option(OTHER),
    ]),
    question("purpose_detail", "purpose", "Basics", "Describe the problem and the benefit in a sentence or two", "area", prefix="Details"),
    question("tool_name", "tool", "Basics", "AI tool and vendor", "text", prefix="Tool", help="e.g. Microsoft Copilot, ChatGPT Enterprise, an internal model"),
    question("tool_approval", "tool", "Basics", "Has the tool been approved for this kind of data?", "single", prefix="Approval status", options=[
        option("Approved for this data"),
        option("Approved for general use, not for sensitive data", "medium", "D2", "Approval may not cover the data in this use case."),
        option("Not yet reviewed", "medium", "D2", "The tool has not been through vendor review."),
        option("Explicitly not approved", "high", "B1", "Using an unapproved tool can trigger blocking rule B1 if any sensitive data is involved."),
        option(UNSURE),
    ]),
    question("use_type", "use_type", "Basics", "What kind of AI is it?", "single", options=[
        option("Chat assistant"),
        option("AI feature inside existing software"),
        option("Custom integration or API"),
        option("Autonomous agent that takes actions", "medium", "D3", "Agents that act on their own need explicit limits and oversight."),
        option(OTHER),
    ]),
    question("users", "users", "Users and affected people", "Who will use it or see its outputs?", "multi", options=[
        option("Just me"),
        option("My team"),
        option("Wider internal staff"),
        option("Customers or the public", "medium", "D5", "External audiences raise the cost of inaccurate outputs."),
        option(OTHER),
    ]),
    question("affected_people", "affected_people", "Users and affected people", "Who could be affected if it gets something wrong?", "multi", options=[
        option("No one beyond the users"),
        option("Internal colleagues"),
        option("Customers", "medium", "D4", "Errors could affect customers."),
        option("General public", "medium", "D4", "Errors could affect members of the public."),
        option("Job applicants or employees", "high", "D4", "Effects on employment are high impact in the rubric."),
        option("Patients or vulnerable people", "high", "D4", "Safety or rights of vulnerable people may be affected."),
        option(OTHER),
    ]),
    question("input_sources", "input_sources", "Data", "Where will the input data come from?", "multi", options=[
        option("Public or published material"),
        option("Synthetic or test data"),
        option("Internal documents"),
        option("Email, chat, or meeting content", "medium", "D1", "Communications often contain personal or confidential information."),
        option("Customer records", "medium", "D1", "Customer records usually include personal data."),
        option("HR or personnel records", "high", "D1", "Personnel records are sensitive personal data."),
        option("Third-party licensed content", "medium", "D6", "Check that the license permits use with AI tools."),
        option(OTHER),
    ]),
    question("data_categories", "data_categories", "Data", "What types of data are included?", "multi", options=[
        option("Public information only"),
        option("Internal business information"),
        option("Source code"),
        option("Financial data", "medium", "D1", "Financial data is typically confidential."),
        option("Personal data (names, contact details)", "medium", "D1", "Personal data requires privacy safeguards."),
        option("Sensitive personal data (health, ID numbers, biometrics, finances)", "high", "D1", "Sensitive personal data scores high on data confidentiality."),
        option(OTHER),
    ]),
    question("confidentiality", "confidentiality", "Data", "Highest confidentiality level involved", "single", options=[
        option("Public"),
        option("Internal"),
        option("Confidential", "medium", "D1", "Confidential data needs stated handling and safeguards."),
        option("Highly confidential, privileged, or trade secret", "high", "D1", "Privileged or highly confidential data scores high on data confidentiality."),
        option(UNSURE),
    ]),
    question("outputs", "outputs", "Outputs and autonomy", "What will it produce?", "multi", options=[
        option("Summaries"),
        option("Draft text or emails"),
        option("Code"),
        option("Images or media", "medium", "D6", "Generated media can raise ownership and permitted-use questions."),
        option("Recommendations or scores", "medium", "D5", "Recommendations and scores can be over-relied on."),
        option("Decisions or actions", "high", "D3", "Producing decisions or actions directly is high autonomy."),
        option(OTHER),
    ]),
    question("output_use", "output_use", "Outputs and autonomy", "How will the outputs be used?", "single", options=[
        option("Personal reference only"),
        option("Internal working material"),
        option("Shared with customers or partners", "medium", "D5", "External outputs need validation before sharing."),
        option("Published publicly", "medium", "D5", "Published outputs carry reputational and accuracy risk."),
        option("Basis for decisions about people", "high", "D4", "Decisions about people are high impact."),
        option(UNSURE),
    ]),
    question("autonomy", "autonomy", "Outputs and autonomy", "What can the AI do on its own?", "single", options=[
        option("Suggestions only; a person does everything"),
        option("Drafts that a person approves before use"),
        option("Low-impact actions automatically", "medium", "D3", "Automatic actions need monitoring, limits, and a way to reverse them."),
        option("Consequential decisions or actions without prior approval", "high", "B2", "This can trigger blocking rule B2."),
        option(UNSURE),
    ]),
    question("human_review", "human_review", "Controls", "How will people review outputs?", "single", options=[
        option("Every output reviewed before use"),
        option("Spot checks only", "medium", "D5", "Unchecked outputs may be used with errors."),
        option("No review planned", "high", "D5", "Unverified outputs score high on output reliability."),
        option(UNSURE),
    ]),
    question("access", "access", "Controls", "Who can access the tool and its data?", "single", options=[
        option("Named individuals"),
        option("A specific team"),
        option("Anyone in the organization"),
        option("External users", "medium", "D2", "External access widens exposure."),
        option(UNSURE),
    ]),
    question("sharing", "sharing", "Controls", "What can the vendor do with your data?", "single", options=[
        option("No external processing; runs internally"),
        option("Vendor processes data but does not retain it or train on it"),
        option("Vendor may retain data, but does not train on it", "medium", "D2", "Retained data at a vendor is residual exposure."),
        option("Vendor may train on our data", "high", "B1", "Vendor training on sensitive data can trigger blocking rule B1."),
        option(UNSURE),
    ]),
    question("retention", "retention", "Controls", "How long are inputs and outputs kept?", "single", options=[
        option("Not stored beyond the session"),
        option("Deleted within 30 days"),
        option("Kept under standard company retention"),
        option("Kept indefinitely", "medium", "D2", "Indefinite retention increases exposure."),
        option(UNSURE),
    ]),
    question("safeguards", "safeguards", "Controls", "Which other safeguards are in place?", "multi", options=[
        option("Access logging or audit trail"),
        option("Output testing or validation"),
        option("Data minimization or redaction"),
        option("User training or usage guidelines"),
        option("Incident reporting process"),
        option("None yet", "medium", "D2", "No safeguards beyond the basics are in place."),
        option(OTHER),
    ]),
    question("ip_rights", "ip_rights", "Controls", "Do you have the rights to use the inputs and outputs this way?", "single", options=[
        option("Inputs are our own, public domain, or synthetic"),
        option("Licensed content used within its license"),
        option("Third-party content; permissions unclear", "medium", "D6", "Unclear permissions are a residual licensing question."),
        option("Content we do not have rights to use", "high", "D6", "Unauthorized use scores high on intellectual property."),
        option(UNSURE),
    ]),
]

SENSITIVE = {
    "HR or personnel records", "Customer records", "Personal data (names, contact details)",
    "Sensitive personal data (health, ID numbers, biometrics, finances)", "Financial data",
    "Confidential", "Highly confidential, privileged, or trade secret",
}
CONSEQUENTIAL = {
    "Hiring, HR, or employee evaluation", "Financial decisions or approvals",
    "Job applicants or employees", "Patients or vulnerable people", "Basis for decisions about people",
}


class Flag(BaseModel):
    risk: str
    rubric: str
    question: str
    reason: str


def selected(answers, key):
    value = answers.get(key)
    if value is None:
        return []
    return [value] if isinstance(value, str) else list(value)


def flags_for(answers):
    flags = []
    for item in QUESTIONS:
        for choice in item.options:
            if choice.risk and choice.label in selected(answers, item.key):
                flags.append(Flag(risk=choice.risk, rubric=choice.rubric, question=item.label, reason=f"{choice.label}: {choice.reason}"))
    chosen = {label for item in QUESTIONS for label in selected(answers, item.key)}
    if chosen & SENSITIVE and chosen & {"Explicitly not approved", "Vendor may train on our data"}:
        flags.append(Flag(risk="high", rubric="B1", question="Data and vendor",
                          reason="Sensitive data combined with an unapproved tool or vendor training is likely to trigger blocking rule B1."))
    if chosen & CONSEQUENTIAL and chosen & {"No review planned", "Consequential decisions or actions without prior approval"}:
        flags.append(Flag(risk="high", rubric="B2", question="Autonomy and oversight",
                          reason="Consequential decisions without human review or approval are likely to trigger blocking rule B2."))
    return sorted(flags, key=lambda flag: -RISK_ORDER[flag.risk])


def preliminary_risk(flags):
    if not flags:
        return None
    return max((flag.risk for flag in flags), key=RISK_ORDER.get)


def answer_text(item, answers, other_text):
    if item.kind in ("text", "area"):
        return (answers.get(item.key) or "").strip()
    labels = selected(answers, item.key)
    if not labels or UNSURE in labels:
        return ""
    labels = [f"Other: {other_text.strip()}" if label == OTHER and other_text.strip() else label for label in labels if label != OTHER or other_text.strip()]
    return "; ".join(labels)


def request_from(answers, other_texts=None):
    other_texts = other_texts or {}
    parts = {key: [] for key in core.FIELDS}
    for item in QUESTIONS:
        text = answer_text(item, answers, other_texts.get(item.key, ""))
        if text:
            parts[item.field].append(f"{item.prefix}: {text}" if item.prefix else text)
    return {key: ". ".join(values) if values else "Unknown" for key, values in parts.items()}


def summary_message(request):
    lines = ["I completed the new AI use case intake form:", ""]
    lines += [f"- **{label}:** {request[key]}" for key, label in core.FIELDS.items()]
    return "\n".join(lines)


def flags_message(flags):
    lines = ["Thanks — your intake form is recorded. I'm running the assessment now. Send a message here to correct or add any facts."]
    if flags:
        lines += ["", "The form flagged these selections for attention (preliminary, not the assessment result):"]
        lines += [f"- **{flag.risk.title()}** ({flag.rubric}) {flag.reason}" for flag in flags]
    return "\n".join(lines)
