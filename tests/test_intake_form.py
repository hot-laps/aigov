import core
import intake_form


def test_form_covers_every_request_field():
    assert {item.field for item in intake_form.QUESTIONS} == set(core.FIELDS)
    assert {item.section for item in intake_form.QUESTIONS} == set(intake_form.SECTIONS)
    rubric_ids = {item["id"] for item in core.read_json(core.BASE_DIR / "rubric.json")["dimensions"]} | {"B1", "B2"}
    assert all(choice.rubric in rubric_ids and choice.reason for item in intake_form.QUESTIONS for choice in item.options if choice.risk)


def test_blank_form_has_no_flags_and_unknown_request():
    assert intake_form.flags_for({}) == []
    assert intake_form.preliminary_risk([]) is None
    assert intake_form.request_from({}) == core.blank_request()


def test_risky_selections_are_flagged_with_highest_first():
    flags = intake_form.flags_for({"human_review": "Spot checks only", "autonomy": "Consequential decisions or actions without prior approval"})
    assert [(flag.risk, flag.rubric) for flag in flags] == [("high", "B2"), ("medium", "D5")]
    assert intake_form.preliminary_risk(flags) == "high"


def test_combined_selections_flag_blocking_rules():
    b1 = intake_form.flags_for({"input_sources": ["Customer records"], "tool_approval": "Explicitly not approved"})
    assert any(flag.rubric == "B1" and "Sensitive data combined" in flag.reason for flag in b1)
    b2 = intake_form.flags_for({"purpose_category": ["Hiring, HR, or employee evaluation"], "human_review": "No review planned"})
    assert any(flag.rubric == "B2" for flag in b2)


def test_request_combines_answers_and_leaves_unsure_unknown():
    request = intake_form.request_from({
        "tool_name": "Copilot", "tool_approval": "Not yet reviewed",
        "users": ["My team", "Other"], "retention": "Not sure yet", "outputs": ["Other"],
    }, {"users": "Auditors"})
    assert request["tool"] == "Tool: Copilot. Approval status: Not yet reviewed"
    assert request["users"] == "My team; Other: Auditors"
    assert core.is_unknown(request["retention"])
    assert core.is_unknown(request["outputs"])
