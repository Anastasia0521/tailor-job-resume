# 论文方法与数据全文审计

## 目的

DOI只用于定位论文。必须继续读取全文的方法、数据、结果、附录和补充材料，系统提取全部可迁移能力，避免只记录题目、摘要或少数显眼模型。

## 每篇论文的审计顺序

1. 核验题名、作者顺序、通讯作者、期刊、年份、DOI和发表状态。
2. 获取并阅读HTML全文、官方PDF、附录和补充材料；记录实际取得的材料范围。
3. 逐段检查研究区与样本、时间范围、空间尺度、数据来源、数据类型和预处理。
4. 穷举价值评估方法、生态或生物物理模型、统计计量方法、空间方法、机器学习、仿真方法和质性方法。
5. 穷举软件、平台、编程语言、程序包、模块和数据库。特别检查图表注释、公式说明、方法小节、补充材料和数据可用性声明。
6. 记录模型输入、关键参数、校准、验证、敏感性分析、不确定性处理和主要产出。
7. 把每项能力绑定到页码、章节、表格、公式或网页段落，不得只写无定位的论文级来源。
8. 完成署名归属后再写入能力证据库和职业分析。

生态系统服务论文必须主动检查InVEST及其Carbon Storage、Water Yield、Habitat Quality、Sediment Delivery Ratio、Nutrient Delivery Ratio、Urban Cooling等模块，以及当量因子法、市场价值法、替代成本法、影子工程法、机会成本法、条件价值法、最优价格法、能值分析、生态系统服务流、供需匹配和价值转移等方法。该清单用于防漏，不代表论文必然使用；只有全文证据支持时才能写入。

## 署名与能力归属

- 第一作者、共同第一作者或通讯作者：默认全文中实际使用的数据、模型、方法、软件和完整分析流程均为本人使用，熟练程度记为熟练，能力证据记为A级；材料或用户明确排除的项目除外。
- 其他作者：论文可以证明研究使用过该方法，但不能自动证明求职者本人使用。依据作者贡献声明、简历中的本人动作或用户确认归属；没有个人证据时标为待确认。
- 论文引用或综述中提及的方法不算实际使用。必须区分背景介绍、文献回顾、方法比较和本研究真正执行的方法。
- 软件与模型不能相互替代推断。例如使用InVEST可以记录具体模块，但不能在未见证据时推断ArcGIS、Python或R。

## 全文不可得

公开渠道找不到全文时，列明已检查的来源和缺失字段，一次性请求用户上传。用户不提供时可以继续，但必须把该论文标为摘要级或简历级证据，并在报告中说明可能漏项；不得标记为全文审计完成。

## 输出结构

生成 `论文方法数据审计表.json`，顶层包含 `schema_version`、`generated_at`、`papers` 和 `audit_summary`。每篇至少包含：

- `title`、`doi`、`publication_status`
- `author_role`、`attribution_rule`
- `materials_obtained`、`audit_level`、`missing_materials`
- `data_sources`、`data_types`、`sample_scope`、`time_range`、`spatial_scale`
- `preprocessing`
- `valuation_methods`、`models`、`statistical_methods`、`spatial_methods`、`machine_learning_methods`、`qualitative_methods`
- `software`、`languages`、`packages_or_modules`
- `parameters`、`calibration`、`validation`、`sensitivity_or_uncertainty`
- `outputs`、`evidence_locations`
- `personal_capabilities`、`items_requiring_confirmation`

所有列表即使为空也必须保留。`audit_level`只能为 `full_text`、`abstract_only`、`resume_only` 或 `pending_user_file`。第一作者、共同第一作者或通讯作者且完成全文审计时，`attribution_rule`写为 `lead_author_default_skilled`。

## 完成标准

- 每篇论文均有记录，没有因标题相似或研究主题相同而合并。
- 全文可得论文至少检查方法、数据、软件和验证四类内容。
- 每个提取项有证据位置。
- 论文正文实际使用的方法与仅引用的方法已经分开。
- 全文缺失论文已明确告知用户。
- 审计表生成后，才允许生成能力证据库和职业市场分析。

