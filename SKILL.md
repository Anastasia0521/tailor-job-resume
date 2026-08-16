---
name: tailor-job-resume
description: 为科研人员和研究生提供两种工作流：从综合简历、论文与公开招聘市场识别数据、方法、软件、完整职业边界及薪资并生成求职策略，或针对具体岗位制作可编辑HTML简历与匹配分析。仅在用户明确提出完整句子“请根据我的履历制定求职策略”或“请根据这个岗位帮我制作针对性简历”时使用；不要因普通简历咨询、岗位分析、文字润色、HTML编辑或相似但不完整的请求触发。
---

# 科研能力转化与求职策略

严格执行以下流程。只优化表达与结构，不改变事实性质。

## 1. 识别模式并检查输入

首先读取 [references/mode-routing.md](references/mode-routing.md) 和 [references/input-checklist.md](references/input-checklist.md)。

- 用户说 `请根据我的履历制定求职策略`：进入职业探索模式。只要求综合简历和输出目录；不得因没有岗位信息而索要岗位或停止。
- 用户说 `请根据这个岗位帮我制作针对性简历`：进入岗位定制模式。要求综合简历、具体岗位信息和输出目录。

照片、论文全文、项目材料和参考模板均为可选。缺少必要输入且无法从上下文定位时，一次性列出缺失项，不重复索取已提供材料。

## 2. 提取事实并自动获取论文资料

完整提取简历中的教育、任职、项目、论文、荣誉、数据、方法、软件和成果。读取 [references/research-capability-extraction.md](references/research-capability-extraction.md) 和 [references/paper-doi-rules.md](references/paper-doi-rules.md)。

从综合简历识别论文题目，自动查找 DOI、期刊官网文章页、摘要、HTML全文、官方PDF、补充材料或合法公开版本。中文论文优先进入期刊官网查找。公开渠道仍无法获得全文时，才说明缺少内容并请求用户上传；用户不提供时只使用公开证据。

不得要求用户预先整理 DOI、摘要、全文或招聘数据。

读取 [references/paper-method-data-audit.md](references/paper-method-data-audit.md)，逐篇完成全文级字段审计，并将结果写入求职决策HTML的嵌入数据。不得只摘录摘要或少数显眼的方法。审计未完成、缺失范围未向用户说明时，不得进入职业方向和招聘市场分析。

## 3. 建立科研与职业能力证据库

不要只按研究主题判断能力。逐篇提取数据类型、数据范围、清洗过程、研究设计、统计方法、模型算法、软件程序包、验证解释、可视化和成果交付，并翻译成企业任务语言。

读取 [references/evidence-confirmation.md](references/evidence-confirmation.md)，按 A、B、C 级集中展示：

- A级为材料直接证明的事实。
- B级为由已确认方法关系直接推出的能力，必须解释关系。
- C级为可能具备但不能证明的能力，必须由用户确认。

只让用户确认事实与个人贡献，不让用户预先选择行业、企业性质、城市或薪资。未确认的 C 级能力不得写入简历。将能力确认、能力证据库、论文方法数据审计和职业策略作为结构化数据嵌入最终求职决策HTML，不再把MD或JSON作为用户可见交付物。

论文署名采用固定归属规则：求职者为第一作者、共同第一作者或通讯作者时，默认论文全文中实际使用的数据、模型、方法、软件和分析流程均由本人使用，并按熟练能力记为A级；除非材料或用户明确排除。其他署名不使用该默认规则，必须依据作者贡献声明、简历描述或用户确认确定个人贡献。

## 4. 研究完整职业边界和招聘市场

读取 [references/career-boundary-analysis.md](references/career-boundary-analysis.md) 和 [references/job-market-and-salary-research.md](references/job-market-and-salary-research.md)。

根据全部已确认能力主动识别所有有实质依据的优先方向、迁移方向、求职边界和暂不建议方向。识别出几个就研究几个，不要求用户预选，也不因用户暂时不了解某类企业而提前排除。

逐个方向搜索近期公开岗位，说明实际工作、行业与公司、常见岗位名、招聘需求、薪资、匹配证据、当前缺口、简历策略和面试风险。不得要求用户自己爬取招聘网站或提供账号、密码、Cookie。

生成通俗详细的求职决策内容。首页直接回答最值得尝试什么、还能尝试什么、暂不建议什么、大致薪资和下一步行动。薪资必须注明城市、时间、样本数量、月薪或年薪口径和来源；证据不足时明确写只能初步参考。

## 5. 完成职业探索模式

职业探索模式只生成一个用户可见文件：`姓名_求职决策中心.html`。其中整合能力确认、能力证据、论文全文审计、职业方向、岗位关键词、招聘市场、薪资、补强计划和面试策略，并嵌入可供后续复用的结构化数据。职业探索模式不要求岗位材料，也不自动生成对外简历。

运行：

```powershell
python scripts/build_career_decision_center.py --input decision.json --output "姓名_求职决策中心.html"
python scripts/validate_decision_center_html.py --html "姓名_求职决策中心.html" --kind exploration
python scripts/validate_mode_outputs.py --mode exploration --output-dir <输出目录>
```

## 6. 完成岗位定制模式

完整拆解具体岗位的硬性门槛、核心职责、业务能力、方法工具、协作表达和优先条件。读取 [references/matching-framework.md](references/matching-framework.md)，建立“岗位要求—履历证据—表达策略”关系；无证据要求必须明确标记，不得补写。

按招聘方阅读顺序组织个人概述、岗位匹配能力、教育背景、重点经历、代表成果、方法技能和荣誉协作。正文正式精简，不使用引号强调，也不使用乘号或加号连接描述。对话中另行提供一段 200至350 字的针对性个人总结。

只生成两个用户可见文件：

- `姓名_单位_岗位_求职决策.html`：仅供求职者本人阅读，整合岗位匹配、证据、缺口、薪资、简历取舍和面试策略。
- `姓名_单位_岗位_简历.html`：用于对外投递，不得包含内部能力缺口、薪资判断或投递策略。

论文必须通过构建脚本生成单行：`标题或省略标题｜DOI｜期刊名称（等级）｜第几作者｜年份`。DOI 超链接只显示 `DOI`；标题可按宽度缩短，其余四项必须完整，标题左侧与年份右侧分别贴齐版心。

运行：

```powershell
python scripts/build_career_decision_center.py --input decision.json --output "姓名_单位_岗位_求职决策.html"
python scripts/validate_decision_center_html.py --html "姓名_单位_岗位_求职决策.html" --kind target
python scripts/build_editable_resume.py --input resume.json --output "姓名_单位_岗位_简历.html" --photo photo.jpg
python scripts/validate_resume_html.py --input resume.json --html "姓名_单位_岗位_简历.html"
python scripts/validate_mode_outputs.py --mode target --output-dir <输出目录>
```

两个HTML都必须支持文字编辑、自动暂存、撤销、下载和打印或导出PDF。简历HTML还必须支持照片大小、位置和裁切调整。默认不另行生成PDF、DOCX、Markdown或独立JSON。

## 7. 守住事实和隐私边界

读取 [references/fact-boundaries.md](references/fact-boundaries.md)。不得把参与改为主持、协助改为独立负责，不得编造软件、数据、奖项、任职时间、论文状态或成果影响。区分个人贡献与团队成果。

不得向公开仓库、第三方网站或无关输出复制个人材料。客户简历、论文全文、照片、能力证据库和本次输出只能保存在用户指定目录。

## 8. 最终验证

- 确认模式、必需输入和交付物一致。
- 确认没有重复询问已在能力证据库中确认的事实。
- 确认策略报告覆盖全部识别方向并使用通俗语言。
- 岗位定制模式确认HTML无重叠、裁切、论文换行或失效DOI。
- 运行 `python scripts/privacy_scan.py <skill-or-output-directory>`。

只有对应模式的校验、隐私扫描和视觉检查全部通过时才交付。



