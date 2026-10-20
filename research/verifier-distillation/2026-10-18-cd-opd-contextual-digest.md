# CD-OPD: Contextual Digest for On-Policy Distillation

- **作者**：Mingyuan Li、Yucheng Li、Xiaxia Wang、Gong Cheng
- **首次公开日期**：2026-10-18
- **版本日期**：2026-10-18（v1）
- **原始论文**：https://arxiv.org/abs/2610.25359
- **arXiv ID**：2610.25359
- **DOI**：https://doi.org/10.48550/arXiv.2610.25359
- **代码/项目**：https://github.com/nju-websoft/CD-OPD

## 一句话结论

指出 teacher 接管 student 生成前缀时可能发生协作失败，并用上下文摘要降低错误前缀对 teacher 监督的污染。

## 真正新增的内容

论文不仅考察 teacher 和 student 各自能力，还显式定义二者在 student prefix 上组合后的 Collaboration Failure Rate（CFR）。

## 核心方法

在 teacher 计算蒸馏目标前，对 student 轨迹压缩出保留任务事实与关键决策的 contextual digest，再以 digest 提供更干净的条件上下文。

## 关键实验结果

论文报告 CD-OPD 在多项推理设置中降低协作失败并优于标准 OPD；公开摘要未给出完整数值，具体幅度需以正文表格复核。

## 证据质量与局限

问题设定直接命中 on-policy prefix mismatch，且代码公开；但摘要证据不足以判断 digest 是否遗漏长程义务、是否由同源模型引入新偏差。

## 最接近的相关工作

与 Persistent Teacher Anchoring、RouteOPD、CompassOPD 及长上下文压缩蒸馏相近；独特之处是把 student prefix 本身视为 teacher 条件污染源。

## 如何复用或推进 LLM-as-a-Verifier

可把 digest 设计为 verifier-facing state：仅保留环境观测、已完成义务、未决约束和证据指针，再对原始轨迹与 digest 评分差做校准。

## 对 Agent verifier × OPD 实验路线的具体影响

【分析推断】应在长轨迹 score-level OPD 中新增 raw-prefix 与 digest-prefix 双路 teacher，对分歧输出 A/B/T；digest 只能作为软 teacher，程序真值和 sealed full-trace eval 不可被摘要替代。

## 结论边界

除明确标注“分析推断”的段落外，上述方法与实验结论均来自论文原文或公开摘要；推断部分是面向现有研究路线的可检验假设，不应视为论文作者已经证明的结论。
