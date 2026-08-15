#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", required=True, choices=["exploration", "target"])
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    root = Path(args.output_dir)
    errors = []

    if args.mode == "exploration":
        required = ["能力确认表.md", "能力证据库.json", "论文方法数据审计表.json", "职业方向与岗位关键词.md", "求职策略报告.md"]
        errors += [f"职业探索模式缺少交付物：{name}" for name in required if not (root / name).is_file()]
        evidence_path = root / "能力证据库.json"
        if evidence_path.is_file():
            try:
                evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
                if not isinstance(evidence, dict) or not evidence:
                    errors.append("能力证据库.json 必须是非空JSON对象")
            except (UnicodeDecodeError, json.JSONDecodeError):
                errors.append("能力证据库.json 不是有效的UTF-8 JSON")
        audit_path = root / "论文方法数据审计表.json"
        if audit_path.is_file():
            try:
                audit = json.loads(audit_path.read_text(encoding="utf-8"))
                papers = audit.get("papers") if isinstance(audit, dict) else None
                if not isinstance(audit, dict) or audit.get("schema_version") != "1.0" or not isinstance(papers, list) or not papers:
                    errors.append("论文方法数据审计表.json 缺少 schema_version=1.0 或非空 papers 数组")
                required_paper_keys = ["title", "author_role", "attribution_rule", "materials_obtained", "audit_level", "data_sources", "data_types", "preprocessing", "valuation_methods", "models", "statistical_methods", "spatial_methods", "machine_learning_methods", "software", "languages", "packages_or_modules", "validation", "evidence_locations", "personal_capabilities"]
                valid_levels = {"full_text", "abstract_only", "resume_only", "pending_user_file"}
                for paper in papers or []:
                    if not all(key in paper for key in required_paper_keys):
                        errors.append("论文方法数据审计表.json 存在字段不完整的论文")
                        break
                    if paper.get("audit_level") not in valid_levels:
                        errors.append("论文方法数据审计表.json 存在无效 audit_level")
                        break
                    if paper.get("author_role") in ["第一作者", "共同第一作者", "通讯作者"] and paper.get("audit_level") == "full_text" and paper.get("attribution_rule") != "lead_author_default_skilled":
                        errors.append("第一作者、共同第一作者或通讯作者的全文审计未应用 lead_author_default_skilled")
                        break
            except (UnicodeDecodeError, json.JSONDecodeError):
                errors.append("论文方法数据审计表.json 不是有效的UTF-8 JSON")
    else:
        required = ["岗位匹配分析.md", "求职策略报告.md"]
        errors += [f"岗位定制模式缺少交付物：{name}" for name in required if not (root / name).is_file()]
        html_files = list(root.glob("*_可编辑版.html"))
        if not html_files:
            errors.append("岗位定制模式缺少姓名_单位_岗位_可编辑版.html")
        elif len(html_files) > 1:
            errors.append("岗位定制模式只能交付一个姓名_单位_岗位_可编辑版.html")

    for name in ["能力确认表.md", "职业方向与岗位关键词.md", "岗位匹配分析.md", "求职策略报告.md"]:
        path = root / name
        if path.is_file() and not path.read_text(encoding="utf-8").strip():
            errors.append(f"交付物不能为空：{name}")

    if errors:
        raise SystemExit("\n".join(errors))
    print(f"Mode output validation passed: {args.mode}")


if __name__ == "__main__":
    main()


