#!/usr/bin/env python3
import argparse
from pathlib import Path

REQUIRED = ["先看结论", "你已经具备的能力", "职业方向全景", "招聘市场与薪资", "还需要补什么", "投递与面试建议", "信息来源"]
ACADEMIC_TONE = ["置信区间", "先验概率", "适配函数", "职业资本折现", "劳动力市场溢价"]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", required=True)
    args = parser.parse_args()
    text = Path(args.report).read_text(encoding="utf-8")
    errors = [f"缺少必要部分：{h}" for h in REQUIRED if h not in text]
    errors += [f"存在不适合面向求职者的学术化表达：{t}" for t in ACADEMIC_TONE if t in text]
    if len(text.strip()) < 1200:
        errors.append("求职策略报告过短，未达到详细研究要求")
    if errors:
        raise SystemExit("\n".join(errors))
    print("Strategy report validation passed")


if __name__ == "__main__":
    main()

