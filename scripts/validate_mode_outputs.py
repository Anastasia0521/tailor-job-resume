#!/usr/bin/env python3
import argparse
from pathlib import Path


LEGACY_VISIBLE = {
    "能力确认表.md", "能力证据库.json", "论文方法数据审计表.json",
    "科研能力检索词包.json", "职业方向与岗位关键词.md", "岗位匹配分析.md", "求职策略报告.md",
}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", required=True, choices=["exploration", "target"])
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    root = Path(args.output_dir)
    errors = []
    visible_legacy = sorted(name for name in LEGACY_VISIBLE if (root / name).is_file())
    if visible_legacy:
        errors.append("存在不应继续作为可见交付物的旧文件：" + "、".join(visible_legacy))
    if list(root.glob("*.pdf")):
        errors.append("默认交付不得同时生成PDF；请使用HTML内的打印或导出PDF功能")

    if args.mode == "exploration":
        decisions = list(root.glob("*_求职决策中心.html"))
        if len(decisions) != 1:
            errors.append("职业探索模式必须且只能交付一个 姓名_求职决策中心.html")
        external = list(root.glob("*_简历.html"))
        if external:
            errors.append("职业探索模式未指定具体岗位时不自动生成对外简历")
    else:
        decisions = list(root.glob("*_求职决策.html"))
        resumes = list(root.glob("*_简历.html"))
        if len(decisions) != 1:
            errors.append("岗位定制模式必须且只能交付一个 姓名_单位_岗位_求职决策.html")
        if len(resumes) != 1:
            errors.append("岗位定制模式必须且只能交付一个 姓名_单位_岗位_简历.html")
    if errors:
        raise SystemExit("\n".join(errors))
    print(f"Mode output validation passed: {args.mode}")


if __name__ == "__main__":
    main()

