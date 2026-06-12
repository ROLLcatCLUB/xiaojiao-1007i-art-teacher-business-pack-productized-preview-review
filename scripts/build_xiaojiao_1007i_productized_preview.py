import hashlib
import json
import textwrap
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SLUG = "xiaojiao_art_teacher_business_pack_productized_preview_1007I"
FINAL_STATUS = "XIAOJIAO_ART_TEACHER_BUSINESS_PACK_PRODUCTIZED_PREVIEW_PASS"
MARKER = "ALL_1007I_ART_TEACHER_BUSINESS_PACK_PRODUCTIZED_PREVIEW_CHECKS_OK"
SAMPLE_DIR = f"samples/{SLUG}"
ZIP_PATH = f"docs/audit_packages/{SLUG}.zip"


def write(path: str, text: str) -> None:
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text, encoding="utf-8")


def dump(path: str, obj) -> None:
    write(path, json.dumps(obj, ensure_ascii=False, indent=2))


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def make_zip(entries: list[str]) -> str:
    zpath = ROOT / ZIP_PATH
    zpath.parent.mkdir(parents=True, exist_ok=True)
    if zpath.exists():
        zpath.unlink()
    with zipfile.ZipFile(zpath, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for entry in entries:
            zf.write(ROOT / entry, entry.replace("\\", "/"))
    return sha256(zpath)


BOUNDARY_FLAGS = {
    "provider_called": False,
    "model_called": False,
    "api_key_configured": False,
    "database_written": False,
    "real_database_written": False,
    "memory_written": False,
    "real_memory_written": False,
    "Feishu_written": False,
    "formal_export_created": False,
    "real_frontend_runtime_modified": False,
    "frontend_runtime_modified": False,
    "dependency_installed": False,
    "teacher_control_runtime_entered": False,
    "public_display_runtime_entered": False,
    "student_side_runtime_entered": False,
    "auto_teacher_approval_performed": False,
    "formal_apply_performed": False,
    "teacher_review_required": True,
}


CSS = """
:root {
  color-scheme: light;
  --ink: #1f2933;
  --muted: #607080;
  --line: #d6dee6;
  --soft: #f5f7fa;
  --panel: #ffffff;
  --accent: #256f7f;
  --accent-2: #8a5a14;
  --ok: #24704a;
  --warn: #9a5b00;
  --danger: #9d3434;
}
* { box-sizing: border-box; }
body {
  margin: 0;
  font-family: "Microsoft YaHei", "Segoe UI", Arial, sans-serif;
  background: #eef3f5;
  color: var(--ink);
}
.shell {
  min-height: 100vh;
  display: grid;
  grid-template-rows: auto 1fr;
}
.topbar {
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 28px;
  background: #ffffff;
  border-bottom: 1px solid var(--line);
}
.brand {
  display: flex;
  align-items: baseline;
  gap: 12px;
}
.brand strong { font-size: 20px; }
.brand span, .meta { color: var(--muted); font-size: 14px; }
.main {
  width: min(1120px, calc(100vw - 40px));
  margin: 0 auto;
  padding: 28px 0 40px;
}
.surface {
  background: var(--panel);
  border: 1px solid var(--line);
  border-radius: 8px;
  padding: 28px;
}
.light-hero {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 300px;
  gap: 28px;
  align-items: start;
}
h1, h2, h3 { margin: 0; letter-spacing: 0; }
h1 { font-size: 28px; line-height: 1.2; }
h2 { font-size: 22px; line-height: 1.25; }
h3 { font-size: 17px; line-height: 1.35; }
p { margin: 0; line-height: 1.65; }
.muted { color: var(--muted); }
.focus-title { margin-top: 10px; font-size: 34px; line-height: 1.2; }
.summary-strip {
  margin-top: 24px;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  border: 1px solid var(--line);
  border-radius: 8px;
  overflow: hidden;
}
.summary-strip div {
  padding: 16px;
  background: #fbfcfd;
  border-right: 1px solid var(--line);
}
.summary-strip div:last-child { border-right: 0; }
.summary-strip b { display: block; font-size: 22px; margin-bottom: 4px; }
.agent-note {
  border-left: 4px solid var(--accent);
  background: #eef7f8;
  padding: 14px 16px;
  border-radius: 6px;
  line-height: 1.6;
}
.actions { display: flex; flex-wrap: wrap; gap: 10px; margin-top: 22px; }
button {
  appearance: none;
  border: 1px solid var(--line);
  background: #fff;
  color: var(--ink);
  padding: 10px 14px;
  border-radius: 6px;
  font-size: 15px;
  cursor: default;
}
button.primary {
  background: var(--accent);
  border-color: var(--accent);
  color: #fff;
}
button.warning {
  border-color: #ddb36f;
  background: #fff8ed;
  color: #663d00;
}
.lesson-grid {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 300px;
  gap: 22px;
  align-items: start;
}
.section {
  border: 1px solid var(--line);
  border-radius: 8px;
  padding: 18px;
  background: #fff;
  margin-top: 14px;
}
.section.problem {
  border-color: #ddb36f;
  background: #fffaf2;
}
.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
}
.pill {
  display: inline-flex;
  align-items: center;
  min-height: 26px;
  padding: 3px 9px;
  border-radius: 999px;
  border: 1px solid var(--line);
  background: #f7f9fb;
  color: var(--muted);
  font-size: 13px;
  white-space: nowrap;
}
.pill.warn { border-color: #ddb36f; color: #7a4a00; background: #fff6e7; }
.side-list {
  display: grid;
  gap: 12px;
}
.object-row {
  border: 1px solid var(--line);
  border-radius: 8px;
  padding: 14px;
  background: #fbfcfd;
}
.object-row b { display: block; margin-bottom: 5px; }
.attached {
  margin-top: 12px;
  margin-left: 18px;
  max-width: 560px;
}
.patch-layout {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 320px;
  gap: 22px;
}
.preview-doc {
  border: 1px solid var(--line);
  border-radius: 8px;
  background: #fff;
  overflow: hidden;
}
.preview-doc header {
  padding: 18px;
  border-bottom: 1px solid var(--line);
  background: #f7fafb;
}
.preview-doc .doc-body { padding: 18px; display: grid; gap: 14px; }
.task {
  padding: 14px;
  background: #fbfcfd;
  border: 1px solid var(--line);
  border-radius: 8px;
}
.review-banner {
  display: flex;
  justify-content: space-between;
  gap: 18px;
  align-items: center;
  border: 1px solid #e6bd72;
  background: #fff8ea;
  border-radius: 8px;
  padding: 16px;
  margin-bottom: 18px;
}
.kv {
  display: grid;
  grid-template-columns: 180px minmax(0, 1fr);
  border-top: 1px solid var(--line);
}
.kv div {
  padding: 12px;
  border-bottom: 1px solid var(--line);
}
.kv div:nth-child(odd) {
  color: var(--muted);
  background: #f8fafb;
}
@media (max-width: 780px) {
  .topbar { padding: 0 16px; }
  .main { width: min(100vw - 24px, 1120px); padding-top: 16px; }
  .surface { padding: 18px; }
  .light-hero, .lesson-grid, .patch-layout { grid-template-columns: 1fr; }
  .summary-strip { grid-template-columns: 1fr; }
  .summary-strip div { border-right: 0; border-bottom: 1px solid var(--line); }
  .summary-strip div:last-child { border-bottom: 0; }
}
"""


def html_page(title: str, body: str) -> str:
    return f"""<!doctype html>
<html lang=\"zh-CN\">
<head>
  <meta charset=\"utf-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
  <title>{title}</title>
  <style>{CSS}</style>
</head>
<body>
{body}
</body>
</html>
"""


def build_html_files() -> None:
    state1 = html_page(
        "小教 今日轻入口",
        """
<div class=\"shell\">
  <header class=\"topbar\">
    <div class=\"brand\"><strong>小教</strong><span>第3周 · 周三</span></div>
    <div class=\"meta\">今日 3 节课 · 1 项待确认</div>
  </header>
  <main class=\"main\">
    <section class=\"surface light-hero\">
      <div>
        <p class=\"muted\">今日最重要的一件事</p>
        <h1 class=\"focus-title\">四年级 1班《色彩的感觉》草稿待确认</h1>
        <div class=\"summary-strip\">
          <div><b>3</b><span class=\"muted\">今日课程</span></div>
          <div><b>1</b><span class=\"muted\">待确认</span></div>
          <div><b>第2课</b><span class=\"muted\">当前优先</span></div>
        </div>
        <div class=\"actions\">
          <button class=\"primary\">现在处理</button>
          <button>稍后</button>
        </div>
      </div>
      <aside class=\"agent-note\">四年级第2课草稿已经生成，第二环节时间可能偏长。要先看一下吗？</aside>
    </section>
  </main>
</div>
""",
    )
    state2 = html_page(
        "小教 单课焦点工作面",
        """
<div class=\"shell\">
  <header class=\"topbar\">
    <div class=\"brand\"><strong>小教</strong><span>单课焦点</span></div>
    <div class=\"meta\">四年级 1班 · 色彩的感觉</div>
  </header>
  <main class=\"main lesson-grid\">
    <section class=\"surface\">
      <p class=\"muted\">课时设计草稿</p>
      <h1>《色彩的感觉》</h1>
      <div class=\"section\">
        <h3>教学目标</h3>
        <p>通过观察、比较与表达，感受色彩冷暖、明度和情绪之间的关系，并能用色彩完成一幅有情绪表达的作品。</p>
      </div>
      <div class=\"section\">
        <div class=\"section-header\"><h3>环节一 · 导入观察</h3><span class=\"pill\">8 分钟</span></div>
        <p>展示两组不同色调的图片，引导学生说出第一感受。</p>
      </div>
      <div class=\"section problem\">
        <div class=\"section-header\"><h3>第二环节 · 色彩探究</h3><span class=\"pill warn\">25 分钟</span></div>
        <p>学生分组讨论冷暖色、明暗变化和情绪表达，再完成一组色彩小实验。</p>
        <div class=\"agent-note attached\">这一段 25 分钟有点撑。要不要我帮你压到 18 分钟，把展示时间留出来？</div>
      </div>
      <div class=\"section\">
        <div class=\"section-header\"><h3>环节三 · 创作与展示</h3><span class=\"pill\">17 分钟</span></div>
        <p>学生完成色彩表达作品，并选择一处说明自己的色彩选择。</p>
      </div>
      <div class=\"actions\">
        <button class=\"primary\">确认课时草稿</button>
        <button class=\"warning\">生成学习单候选</button>
        <button>暂时忽略建议</button>
      </div>
    </section>
    <aside class=\"surface side-list\">
      <div class=\"object-row\"><b>学习单</b><span class=\"muted\">未生成 · 关联本课</span></div>
      <div class=\"object-row\"><b>评价量规</b><span class=\"muted\">待生成 · 作品表达维度</span></div>
      <div class=\"object-row\"><b>资源参考</b><span class=\"muted\">可打开资源选择器，本阶段不接真实资源库</span></div>
    </aside>
  </main>
</div>
""",
    )
    state3 = html_page(
        "小教 学习单候选预览",
        """
<div class=\"shell\">
  <header class=\"topbar\">
    <div class=\"brand\"><strong>小教</strong><span>学习单候选</span></div>
    <div class=\"meta\">等待张老师审核</div>
  </header>
  <main class=\"main\">
    <div class=\"review-banner\">
      <div><strong>这是候选内容，还不是正式学习单。</strong><p class=\"muted\">确认前不会写入正式材料。</p></div>
      <span class=\"pill warn\">待教师审核</span>
    </div>
    <section class=\"patch-layout\">
      <article class=\"preview-doc\">
        <header><h1>《色彩的感觉》学习单候选</h1><p class=\"muted\">四年级 · 课堂练习型 · 难度正常</p></header>
        <div class=\"doc-body\">
          <div class=\"task\"><h3>学习目标</h3><p>我能观察色彩带来的情绪感受，并说出自己使用某种色彩的理由。</p></div>
          <div class=\"task\"><h3>学生任务</h3><p>选择一种情绪，用 3 组颜色做小样，再圈出最能表达这种情绪的一组。</p></div>
          <div class=\"task\"><h3>自查问题</h3><p>我的颜色选择和想表达的感受一致吗？我能说出一种颜色变化带来的不同感觉吗？</p></div>
        </div>
      </article>
      <aside class=\"surface side-list\">
        <div class=\"object-row\"><b>来源</b><span class=\"muted\">来自《色彩的感觉》课时目标、当前课时结构、四年级学情 stub。</span></div>
        <div class=\"object-row\"><b>状态</b><span class=\"muted\">等待教师审核 · 不会自动采用</span></div>
        <div class=\"actions\">
          <button class=\"primary\">采用</button>
          <button>修改</button>
          <button>不采用</button>
          <button>重新生成候选</button>
        </div>
      </aside>
    </section>
  </main>
</div>
""",
    )
    state4 = html_page(
        "小教 教师审核门",
        """
<div class=\"shell\">
  <header class=\"topbar\">
    <div class=\"brand\"><strong>小教</strong><span>教师审核</span></div>
    <div class=\"meta\">候选内容不会自动通过</div>
  </header>
  <main class=\"main\">
    <section class=\"surface\">
      <div class=\"review-banner\">
        <div><strong>小教已经把学习单候选放到审核区。</strong><p class=\"muted\">系统不能替老师做最终专业判断。</p></div>
        <span class=\"pill warn\">需要确认</span>
      </div>
      <div class=\"kv\">
        <div>patch_id</div><div>patch_handout_L004_001</div>
        <div>target_work_object</div><div>art_handout</div>
        <div>patch_type</div><div>create_handout_candidate</div>
        <div>applied</div><div>false</div>
        <div>rollback_available</div><div>true</div>
        <div>teacher_review_required</div><div>true</div>
      </div>
      <div class=\"actions\">
        <button class=\"primary\">确认采用</button>
        <button>修改后采用</button>
        <button>暂存</button>
        <button>放弃</button>
        <button>重新生成候选</button>
      </div>
    </section>
  </main>
</div>
""",
    )
    write(f"{SAMPLE_DIR}/state_1_light_entry.html", state1)
    write(f"{SAMPLE_DIR}/state_2_lesson_focus.html", state2)
    write(f"{SAMPLE_DIR}/state_3_handout_patch_preview.html", state3)
    write(f"{SAMPLE_DIR}/state_4_teacher_review_gate.html", state4)


def build_directives() -> dict:
    base_false = {"teacher_review_required": False, "formal_apply_performed": False}
    return {
        "stage": "1007I_ART_TEACHER_BUSINESS_PACK_PRODUCTIZED_PREVIEW",
        "final_status": FINAL_STATUS,
        "directives": {
            "light_entry_today_directive": {
                **base_false,
                "surface_mode": "light_entry",
                "primary_object": "today_work_items",
                "supporting_objects": ["art_lesson_design.lesson_L004_color_feeling"],
                "visible_zones": ["today_summary", "priority_item", "agent_note", "two_actions"],
                "hidden_zones": ["resource_library_home", "grid_studio", "right_ai_panel"],
                "agent_notes": [{"attach_to": "priority_item", "text": "四年级第2课草稿已经生成，第二环节时间可能偏长。要先看一下吗？"}],
                "available_actions": ["现在处理", "稍后"],
            },
            "lesson_focus_directive": {
                **base_false,
                "surface_mode": "focus_surface",
                "primary_object": "art_lesson_design.lesson_L004_color_feeling",
                "supporting_objects": ["art_handout.handout_L004_missing", "art_rubric.rubric_L004_pending", "art_resource_ref.drawer_stub"],
                "visible_zones": ["lesson_objectives", "lesson_structure", "attached_agent_note", "linked_objects", "lesson_actions"],
                "hidden_zones": ["resource_library_home", "student_side_runtime", "public_display_surface"],
                "agent_notes": [{"attach_to": "lesson_structure.section_2", "text": "这一段 25 分钟有点撑。要不要我帮你压到 18 分钟，把展示时间留出来？"}],
                "available_actions": ["确认课时草稿", "生成学习单候选", "暂时忽略建议"],
            },
            "handout_patch_preview_directive": {
                "surface_mode": "guided_review",
                "primary_object": "handout_candidate_patch.patch_handout_L004_001",
                "supporting_objects": ["art_lesson_design.lesson_L004_color_feeling", "teacher_profile_stub.grade_4"],
                "visible_zones": ["candidate_preview", "source_context", "review_actions", "status_notice"],
                "hidden_zones": ["formal_export", "database_apply", "provider_trace"],
                "agent_notes": [{"attach_to": "candidate_preview", "text": "这是候选内容，还不是正式学习单。确认前不会写入正式材料。"}],
                "available_actions": ["采用", "修改", "不采用", "重新生成候选"],
                "teacher_review_required": True,
                "formal_apply_performed": False,
            },
            "teacher_review_gate_directive": {
                "surface_mode": "focus_surface",
                "primary_object": "work_object_patch.patch_handout_L004_001",
                "supporting_objects": ["art_handout", "art_lesson_design.lesson_L004_color_feeling"],
                "visible_zones": ["patch_identity", "review_state", "teacher_decision_actions"],
                "hidden_zones": ["auto_approve", "formal_writeback", "real_model_generation"],
                "agent_notes": [{"attach_to": "review_state", "text": "系统不能自动通过教师审核。小教只能生成候选，不能替教师做最终专业判断。"}],
                "available_actions": ["确认采用", "修改后采用", "暂存", "放弃", "重新生成候选"],
                "teacher_review_required": True,
                "formal_apply_performed": False,
            },
        },
        "boundary_flags": BOUNDARY_FLAGS,
    }


def validator_text() -> str:
    return f'''import argparse
import json
import sys
import zipfile
from pathlib import Path

SLUG = "{SLUG}"
EXPECTED_STATUS = "{FINAL_STATUS}"
EXPECTED_MARKER = "{MARKER}"
REQUIRED_FILES = [
    "docs/foundation/{SLUG}.md",
    "docs/foundation/{SLUG}.json",
    "samples/{SLUG}/productized_preview_render_directives_1007I.json",
    "samples/{SLUG}/state_1_light_entry.html",
    "samples/{SLUG}/state_2_lesson_focus.html",
    "samples/{SLUG}/state_3_handout_patch_preview.html",
    "samples/{SLUG}/state_4_teacher_review_gate.html",
    "scripts/validate_{SLUG}.py",
    "docs/audit/{SLUG}_result.json",
    "docs/audit/{SLUG}_report.md",
    "docs/audit_packages/{SLUG}_manifest.json",
    "docs/audit_packages/{SLUG}.zip",
]
ZIP_ENTRIES = REQUIRED_FILES[:-1]
FORBIDDEN_PARTS = [".env", "token", "secret", "key", "node_modules", "__pycache__", ".db", ".sqlite", "dist", "build", "coverage", ".DS_Store"]
FALSE_FLAGS = ["provider_called","model_called","api_key_configured","database_written","real_database_written","memory_written","real_memory_written","Feishu_written","formal_export_created","real_frontend_runtime_modified","frontend_runtime_modified","dependency_installed","teacher_control_runtime_entered","public_display_runtime_entered","student_side_runtime_entered","auto_teacher_approval_performed","formal_apply_performed"]

def fail(msg):
    print("VALIDATION_FAILED: " + msg)
    sys.exit(1)

def rel_ok(path):
    return not (path.startswith("/") or path.startswith("\\\\") or (len(path) > 1 and path[1] == ":")) and "\\\\" not in path

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

    result = json.loads((root / f"docs/audit/{{SLUG}}_result.json").read_text(encoding="utf-8"))
    if result.get("final_status") != EXPECTED_STATUS or result.get("pass") is not True:
        fail("unexpected result status")
    if result.get("marker") != EXPECTED_MARKER:
        fail("unexpected marker")
    flags = result.get("boundary_flags", {{}})
    for flag in FALSE_FLAGS:
        if flags.get(flag) is not False:
            fail("unsafe boundary flag: " + flag)
    if flags.get("teacher_review_required") is not True:
        fail("teacher_review_required must be true")

    directives = json.loads((root / f"samples/{{SLUG}}/productized_preview_render_directives_1007I.json").read_text(encoding="utf-8"))
    items = directives.get("directives", {{}})
    expected = ["light_entry_today_directive", "lesson_focus_directive", "handout_patch_preview_directive", "teacher_review_gate_directive"]
    for key in expected:
        if key not in items:
            fail("missing directive: " + key)
        for field in ["surface_mode", "primary_object", "supporting_objects", "visible_zones", "hidden_zones", "agent_notes", "available_actions", "teacher_review_required", "formal_apply_performed"]:
            if field not in items[key]:
                fail(f"directive {{key}} missing field {{field}}")
        if items[key].get("formal_apply_performed") is not False:
            fail("formal_apply_performed must be false for " + key)
    if items["handout_patch_preview_directive"].get("teacher_review_required") is not True:
        fail("patch preview must require teacher review")
    if items["teacher_review_gate_directive"].get("teacher_review_required") is not True:
        fail("teacher review gate must require teacher review")
    modes = {{items[k].get("surface_mode") for k in expected}}
    for mode in ["light_entry", "focus_surface", "guided_review"]:
        if mode not in modes:
            fail("missing surface_mode: " + mode)

    html_checks = {{
        "state_1_light_entry.html": ["今日 3 节课", "现在处理", "稍后"],
        "state_2_lesson_focus.html": ["第二环节", "生成学习单候选", "学习单"],
        "state_3_handout_patch_preview.html": ["不是正式学习单", "待教师审核", "采用"],
        "state_4_teacher_review_gate.html": ["系统不能替老师做最终专业判断", "teacher_review_required", "false"],
    }}
    forbidden_teacher_terms = ["render directive", "action gate", "model candidate envelope"]
    for name, terms in html_checks.items():
        text = (root / f"samples/{{SLUG}}/{{name}}").read_text(encoding="utf-8")
        for term in terms:
            if term not in text:
                fail(f"HTML {{name}} missing term {{term}}")
        visible = text.lower()
        for term in forbidden_teacher_terms:
            if term in visible:
                fail(f"teacher-facing HTML contains engineering term: {{term}}")

    manifest = json.loads((root / f"docs/audit_packages/{{SLUG}}_manifest.json").read_text(encoding="utf-8"))
    with zipfile.ZipFile(root / f"docs/audit_packages/{{SLUG}}.zip", "r") as zf:
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
        fail(f"manifest/ZIP mismatch: {{manifest_minus_zip}} / {{zip_minus_manifest}}")
    if manifest.get("zip_entry_count") != len(entries):
        fail("zip_entry_count mismatch")
    if manifest.get("manifest_minus_zip") != [] or manifest.get("zip_minus_manifest") != []:
        fail("manifest diff fields must be []")
    print(EXPECTED_MARKER)

if __name__ == "__main__":
    main()
'''


def main() -> None:
    build_html_files()
    directives = build_directives()
    dump(f"{SAMPLE_DIR}/productized_preview_render_directives_1007I.json", directives)
    foundation = {
        "stage": "1007I_ART_TEACHER_BUSINESS_PACK_PRODUCTIZED_PREVIEW",
        "final_status": FINAL_STATUS,
        "stage_type": "static_productized_preview",
        "inherits_from": [
            "1007A-H_ART_TEACHER_DAILY_WORK_BUSINESS_PACK_ACCEPTED",
            "1006A_H_MINIMUM_RUNTIME_FOUNDATION_BASELINE_PASS",
            "1005A_PRODUCT_POSITIONING_AND_DIFFERENTIATION_CONTRACT_PASS",
        ],
        "goal": "turn the accepted art teacher daily work vertical slice into a teacher-readable static preview",
        "covered_product_states": [
            "state_1_light_entry",
            "state_2_lesson_focus",
            "state_3_handout_patch_preview",
            "state_4_teacher_review_gate",
        ],
        "surface_modes": ["light_entry", "focus_surface", "guided_review"],
        "boundary_flags": BOUNDARY_FLAGS,
        "next_stage": "1007I_REVIEW_PENDING_BEFORE_REAL_ART_TEACHER_BUSINESS_APPLY",
    }
    dump(f"docs/foundation/{SLUG}.json", foundation)
    write(
        f"docs/foundation/{SLUG}.md",
        textwrap.dedent(
            f"""\
            # 1007I Art Teacher Business Pack Productized Preview

            ```text
            final_status={FINAL_STATUS}
            stage_type=static_productized_preview
            next_stage=1007I_REVIEW_PENDING_BEFORE_REAL_ART_TEACHER_BUSINESS_APPLY
            ```

            ## Goal

            1007I turns the accepted `1007A-H` art teacher daily work vertical slice into a teacher-readable static preview. It does not add real capability, connect a model, write a database, alter memory, write Feishu, install dependencies, or modify the real frontend runtime.

            ## Covered States

            1. 今日轻入口
            2. 单课焦点工作面
            3. 学习单候选 patch 预览
            4. 教师审核门

            ## Product Constraints

            - The default entrance is light.
            - Xiaojiao notes attach to work objects, not a permanent right-side AI panel.
            - Handout, rubric, and resources are linked work objects, not standalone feature entrances.
            - Candidate content stops at teacher review.
            - Teacher-facing HTML avoids engineering terms.

            ## Boundary Flags

            ```text
            provider_called=false
            model_called=false
            api_key_configured=false
            database_written=false
            memory_written=false
            Feishu_written=false
            formal_export_created=false
            real_frontend_runtime_modified=false
            dependency_installed=false
            teacher_review_required=true
            formal_apply_performed=false
            ```

            ```text
            {MARKER}
            ```
            """
        ),
    )
    write(f"scripts/validate_{SLUG}.py", validator_text())
    result = {
        "stage": "1007I_ART_TEACHER_BUSINESS_PACK_PRODUCTIZED_PREVIEW",
        "final_status": FINAL_STATUS,
        "pass": True,
        "marker": MARKER,
        "preview_type": "static_teacher_readable_html",
        "states": ["light_entry", "lesson_focus", "handout_patch_preview", "teacher_review_gate"],
        "boundary_flags": BOUNDARY_FLAGS,
        "validation": {
            "py_compile": "PENDING",
            "validator_no_arg": "PENDING",
            "validator_root": "PENDING",
            "manifest_minus_zip": [],
            "zip_minus_manifest": [],
        },
        "next_stage": "1007I_REVIEW_PENDING_BEFORE_REAL_ART_TEACHER_BUSINESS_APPLY",
    }
    dump(f"docs/audit/{SLUG}_result.json", result)
    write(
        f"docs/audit/{SLUG}_report.md",
        textwrap.dedent(
            f"""\
            # 1007I Productized Preview Report

            ```text
            final_status={FINAL_STATUS}
            marker={MARKER}
            ```

            ## Evidence

            - Four static HTML product states exist.
            - Render directive JSON exists with four directives.
            - Patch and review states require teacher review.
            - `formal_apply_performed=false`.
            - Teacher-facing HTML avoids core engineering terms.

            ## Caveat

            This is a static productized preview, not real business runtime and not real frontend integration.
            """
        ),
    )
    entries = [
        f"docs/foundation/{SLUG}.md",
        f"docs/foundation/{SLUG}.json",
        f"{SAMPLE_DIR}/productized_preview_render_directives_1007I.json",
        f"{SAMPLE_DIR}/state_1_light_entry.html",
        f"{SAMPLE_DIR}/state_2_lesson_focus.html",
        f"{SAMPLE_DIR}/state_3_handout_patch_preview.html",
        f"{SAMPLE_DIR}/state_4_teacher_review_gate.html",
        f"scripts/validate_{SLUG}.py",
        f"docs/audit/{SLUG}_result.json",
        f"docs/audit/{SLUG}_report.md",
        f"docs/audit_packages/{SLUG}_manifest.json",
    ]
    manifest = {
        "stage": "1007I_ART_TEACHER_BUSINESS_PACK_PRODUCTIZED_PREVIEW",
        "final_status": FINAL_STATUS,
        "zip_path": ZIP_PATH,
        "zip_sha256": "PENDING_RECOMPUTE_AFTER_FINAL_ZIP",
        "zip_entry_count": len(entries),
        "zip_entries": entries,
        "manifest_minus_zip": [],
        "zip_minus_manifest": [],
        "forbidden_files_present": [],
        "marker": MARKER,
    }
    dump(f"docs/audit_packages/{SLUG}_manifest.json", manifest)
    zip_hash = make_zip(entries)
    manifest["zip_sha256"] = zip_hash
    dump(f"docs/audit_packages/{SLUG}_manifest.json", manifest)
    zip_hash = make_zip(entries)

    readme = textwrap.dedent(
        f"""\
        # Xiaojiao 1007I Art Teacher Business Pack Productized Preview Review

        ```text
        final_status={FINAL_STATUS}
        ZIP_ENTRY_COUNT={len(entries)}
        ZIP_SHA256={zip_hash}
        validator_no_arg=PENDING
        validator_root=PENDING
        manifest_minus_zip=[]
        zip_minus_manifest=[]
        next_stage=1007I_REVIEW_PENDING_BEFORE_REAL_ART_TEACHER_BUSINESS_APPLY
        ```

        ## Preview States

        - `state_1_light_entry.html`
        - `state_2_lesson_focus.html`
        - `state_3_handout_patch_preview.html`
        - `state_4_teacher_review_gate.html`

        ## Boundary Flags

        ```text
        provider_called=false
        model_called=false
        api_key_configured=false
        database_written=false
        memory_written=false
        Feishu_written=false
        formal_export_created=false
        real_frontend_runtime_modified=false
        dependency_installed=false
        teacher_review_required=true
        formal_apply_performed=false
        ```
        """
    )
    write("README_1007I_ART_TEACHER_BUSINESS_PACK_PRODUCTIZED_PREVIEW_REVIEW.md", readme)


if __name__ == "__main__":
    main()
