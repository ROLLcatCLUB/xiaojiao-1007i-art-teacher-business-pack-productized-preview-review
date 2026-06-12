# 1007I Art Teacher Business Pack Productized Preview

```text
final_status=XIAOJIAO_ART_TEACHER_BUSINESS_PACK_PRODUCTIZED_PREVIEW_PASS
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
ALL_1007I_ART_TEACHER_BUSINESS_PACK_PRODUCTIZED_PREVIEW_CHECKS_OK
```
