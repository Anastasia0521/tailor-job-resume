# 输入与数据结构

## 职业探索模式

必需输入：

1. 综合简历：至少包含可核验经历，支持DOCX、PDF、HTML、Markdown或纯文本。
2. 输出目录。

岗位信息不是必需输入。缺少岗位时不得索要。照片、参考模板、论文全文、项目材料和作品均为可选。

## 岗位定制模式

必需输入：

1. 综合简历。
2. 具体岗位信息：招聘单位、岗位名称、职责和任职要求，可来自截图、网页、PDF、Word或粘贴文本。
3. 输出目录。

照片和参考模板为可选。缺少岗位信息时一次性列出缺失内容，不得以相似公开岗位代替。

## 两种模式共同规则

- 不要求用户预先提供论文 DOI、摘要或全文；先自动检索，公开渠道仍找不到时再请求上传。
- 首次分析不要求用户选择行业、企业性质、城市、薪资或职业方向。
- 已有 `能力证据库.json` 时先核对身份与材料范围，再复用确认结果。
- 已有 `论文方法数据审计表.json` 时先核对论文版本、全文材料范围和署名；全文或论文状态变化时重新审计对应论文。
- 缺少照片时生成无照片版，不使用虚构头像。
- 参考模板缺少时使用正式、克制、A4黑白研究或商业简历版式。
- 个人敏感字段只保留用户明确提供且适合求职展示的内容。

## 简历构建JSON

岗位定制模式使用：

```json
{
  "name": "示例姓名",
  "target": "示例单位｜示例岗位",
  "contact": ["电话：示例", "邮箱：example@example.com"],
  "summary": "针对性概述",
  "sections": [
    {
      "title": "岗位匹配能力",
      "items": [
        {"heading": "政策研究", "body": "以真实履历证据说明能力。"},
        {
          "kind": "paper",
          "title": "A verified full research paper title",
          "doi": "10.1234/example.2026.001",
          "doi_source_url": "https://journal.example.org/article/example",
          "journal": "Journal of Example Studies",
          "level": "SSCI",
          "author_rank": "第一作者",
          "year": "2026",
          "body": "说明本人的研究贡献和岗位价值。"
        }
      ]
    }
  ]
}
```

论文条目必须分别填写 `title`、`doi`、`doi_source_url`、`journal`、`level`、`author_rank` 和 `year`，不得手工拼接进普通标题。`summary` 和 `body` 不得使用引号强调，也不得使用乘号或加号连接描述。


