import argparse
import json
import sys
import zipfile
from pathlib import Path

SLUG = "xiaojiao_art_teacher_business_pack_productized_preview_1007I"
EXPECTED_STATUS = "XIAOJIAO_ART_TEACHER_BUSINESS_PACK_PRODUCTIZED_PREVIEW_PASS"
EXPECTED_MARKER = "ALL_1007I_ART_TEACHER_BUSINESS_PACK_PRODUCTIZED_PREVIEW_CHECKS_OK"
REQUIRED_FILES = [
    "docs/foundation/xiaojiao_art_teacher_business_pack_productized_preview_1007I.md",
    "docs/foundation/xiaojiao_art_teacher_business_pack_productized_preview_1007I.json",
    "samples/xiaojiao_art_teacher_business_pack_productized_preview_1007I/productized_preview_render_directives_1007I.json",
    "samples/xiaojiao_art_teacher_business_pack_productized_preview_1007I/state_1_light_entry.html",
    "samples/xiaojiao_art_teacher_business_pack_productized_preview_1007I/state_2_lesson_focus.html",
    "samples/xiaojiao_art_teacher_business_pack_productized_preview_1007I/state_3_handout_patch_preview.html",
    "samples/xiaojiao_art_teacher_business_pack_productized_preview_1007I/state_4_teacher_review_gate.html",
    "scripts/validate_xiaojiao_art_teacher_business_pack_productized_preview_1007I.py",
    "docs/audit/xiaojiao_art_teacher_business_pack_productized_preview_1007I_result.json",
    "docs/audit/xiaojiao_art_teacher_business_pack_productized_preview_1007I_report.md",
    "docs/audit_packages/xiaojiao_art_teacher_business_pack_productized_preview_1007I_manifest.json",
    "docs/audit_packages/xiaojiao_art_teacher_business_pack_productized_preview_1007I.zip",
]
ZIP_ENTRIES = REQUIRED_FILES[:-1]
FORBIDDEN_PARTS = [".env", "token", "secret", "key", "node_modules", "__pycache__", ".db", ".sqlite", "dist", "build", "coverage", ".DS_Store"]
FALSE_FLAGS = ["provider_called","model_called","api_key_configured","database_written","real_database_written","memory_written","real_memory_written","Feishu_written","formal_export_created","real_frontend_runtime_modified","frontend_runtime_modified","dependency_installed","teacher_control_runtime_entered","public_display_runtime_entered","student_side_runtime_entered","auto_teacher_approval_performed","formal_apply_performed"]

def fail(msg):
    print("VALIDATION_FAILED: " + msg)
    sys.exit(1)

def rel_ok(path):
    return not (path.startswith("/") or path.startswith("\\") or (len(path) > 1 and path[1] == ":")) and "\\" not in path

def forbidden(path):
    low = path.lower()
    return any(part.lower() in low for part in FORBIDDEN_PARTS)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    for rel in REQUIRED_FILES:
        if not rel_ok(rel):
            fail("bad required path: " + rel)
        if forbidden(rel):
            fail("forbidden required path: " + rel)
        if not (root / rel).exists():
            fail("missing required file: " + rel)

    result = json.loads((root / f"docs/audit/{SLUG}_result.json").read_text(encoding="utf-8"))
    if result.get("final_status") != EXPECTED_STATUS or result.get("pass") is not True:
        fail("unexpected result status")
    if result.get("marker") != EXPECTED_MARKER:
        fail("unexpected marker")
    flags = result.get("boundary_flags", {})
    for flag in FALSE_FLAGS:
        if flags.get(flag) is not False:
            fail("unsafe boundary flag: " + flag)
    if flags.get("teacher_review_required") is not True:
        fail("teacher_review_required must be true")

    directives = json.loads((root / f"samples/{SLUG}/productized_preview_render_directives_1007I.json").read_text(encoding="utf-8"))
    items = directives.get("directives", {})
    expected = ["light_entry_today_directive", "lesson_focus_directive", "handout_patch_preview_directive", "teacher_review_gate_directive"]
    for key in expected:
        if key not in items:
            fail("missing directive: " + key)
        for field in ["surface_mode", "primary_object", "supporting_objects", "visible_zones", "hidden_zones", "agent_notes", "available_actions", "teacher_review_required", "formal_apply_performed"]:
            if field not in items[key]:
                fail(f"directive {key} missing field {field}")
        if items[key].get("formal_apply_performed") is not False:
            fail("formal_apply_performed must be false for " + key)
    if items["handout_patch_preview_directive"].get("teacher_review_required") is not True:
        fail("patch preview must require teacher review")
    if items["teacher_review_gate_directive"].get("teacher_review_required") is not True:
        fail("teacher review gate must require teacher review")
    modes = {items[k].get("surface_mode") for k in expected}
    for mode in ["light_entry", "focus_surface", "guided_review"]:
        if mode not in modes:
            fail("missing surface_mode: " + mode)

    html_checks = {
        "state_1_light_entry.html": ["今日 3 节课", "现在处理", "稍后"],
        "state_2_lesson_focus.html": ["第二环节", "生成学习单候选", "学习单"],
        "state_3_handout_patch_preview.html": ["不是正式学习单", "待教师审核", "采用"],
        "state_4_teacher_review_gate.html": ["系统不能替老师做最终专业判断", "teacher_review_required", "false"],
    }
    forbidden_teacher_terms = ["render directive", "action gate", "model candidate envelope"]
    for name, terms in html_checks.items():
        text = (root / f"samples/{SLUG}/{name}").read_text(encoding="utf-8")
        for term in terms:
            if term not in text:
                fail(f"HTML {name} missing term {term}")
        visible = text.lower()
        for term in forbidden_teacher_terms:
            if term in visible:
                fail(f"teacher-facing HTML contains engineering term: {term}")

    manifest = json.loads((root / f"docs/audit_packages/{SLUG}_manifest.json").read_text(encoding="utf-8"))
    with zipfile.ZipFile(root / f"docs/audit_packages/{SLUG}.zip", "r") as zf:
        entries = sorted(zf.namelist())
    for entry in entries:
        if not rel_ok(entry):
            fail("bad ZIP entry path: " + entry)
        if forbidden(entry):
            fail("forbidden ZIP entry: " + entry)
    expected_entries = sorted(manifest.get("zip_entries", []))
    manifest_minus_zip = sorted(set(expected_entries) - set(entries))
    zip_minus_manifest = sorted(set(entries) - set(expected_entries))
    if manifest_minus_zip or zip_minus_manifest:
        fail(f"manifest/ZIP mismatch: {manifest_minus_zip} / {zip_minus_manifest}")
    if manifest.get("zip_entry_count") != len(entries):
        fail("zip_entry_count mismatch")
    if manifest.get("manifest_minus_zip") != [] or manifest.get("zip_minus_manifest") != []:
        fail("manifest diff fields must be []")
    print(EXPECTED_MARKER)

if __name__ == "__main__":
    main()
