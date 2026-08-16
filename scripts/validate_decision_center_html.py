#!/usr/bin/env python3
import argparse
import json
import re
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--html", required=True)
    parser.add_argument("--kind", choices=["exploration", "target"], required=True)
    args = parser.parse_args()
    text = Path(args.html).read_text(encoding="utf-8")
    errors = []
    for marker in ['data-decision-schema="1"', 'id="career-data"', "downloadHtml()", "window.print()", "toggleEdit()", "searchReport("]:
        if marker not in text:
            errors.append(f"缺少决策中心功能：{marker}")
    match = re.search(r'<script id="career-data" type="application/json">(.*?)</script>', text, re.S)
    embedded = None
    if not match:
        errors.append("缺少嵌入式career-data")
    else:
        try:
            embedded = json.loads(match.group(1).replace("<\\/", "</"))
        except json.JSONDecodeError:
            errors.append("嵌入式career-data不是有效JSON")
    if not isinstance(embedded, dict):
        errors.append("career-data必须是JSON对象")
    else:
        required = ["capability_evidence", "paper_audit", "career_strategy"]
        errors += [f"career-data缺少：{key}" for key in required if key not in embedded]
        if not isinstance(embedded.get("capability_evidence"), list) or not embedded.get("capability_evidence"):
            errors.append("career-data.capability_evidence必须是非空数组")
        if not isinstance(embedded.get("career_strategy"), list) or not embedded.get("career_strategy"):
            errors.append("career-data.career_strategy必须是非空数组")
        audit = embedded.get("paper_audit")
        papers = audit.get("papers") if isinstance(audit, dict) else None
        if not isinstance(audit, dict) or audit.get("schema_version") != "1.0" or not isinstance(papers, list) or not papers:
            errors.append("career-data.paper_audit缺少schema_version=1.0或非空papers数组")
        else:
            required_paper_keys = [
                "title", "author_role", "attribution_rule", "materials_obtained", "audit_level",
                "data_sources", "data_types", "preprocessing", "valuation_methods", "models",
                "statistical_methods", "spatial_methods", "machine_learning_methods", "software",
                "languages", "packages_or_modules", "validation", "evidence_locations", "personal_capabilities",
            ]
            valid_levels = {"full_text", "abstract_only", "resume_only", "pending_user_file"}
            for paper in papers:
                if not isinstance(paper, dict) or not all(key in paper for key in required_paper_keys):
                    errors.append("career-data.paper_audit存在字段不完整的论文")
                    break
                if paper.get("audit_level") not in valid_levels:
                    errors.append("career-data.paper_audit存在无效audit_level")
                    break
                if (paper.get("author_role") in ["第一作者", "共同第一作者", "通讯作者"]
                        and paper.get("audit_level") == "full_text"
                        and paper.get("attribution_rule") != "lead_author_default_skilled"):
                    errors.append("主要作者的全文审计未应用lead_author_default_skilled")
                    break
        if args.kind == "target" and (not isinstance(embedded.get("job_match"), list) or not embedded.get("job_match")):
            errors.append("岗位决策HTML的career-data.job_match必须是非空数组")
    if len(re.findall(r'class="report-section"', text)) < 3:
        errors.append("决策中心可读章节过少")
    if errors:
        raise SystemExit("\n".join(errors))
    print(f"Decision center validation passed: {args.kind}")


if __name__ == "__main__":
    main()

