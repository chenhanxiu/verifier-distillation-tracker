# When Verification Is Not Agreement: Cross-Agent LLM-to-Dafny Formalization

- **作者**：Priyanath Maji
- **首次公开日期**：2026-11-04
- **版本日期**：2026-11-04（arXiv v1）
- **原始论文**：https://arxiv.org/abs/2611.07073
- **DOI**：https://doi.org/10.48550/arXiv.2611.07073
- **会议**：NeurIPS 2026 Workshop on AI for Verifiable Coding
- **代码**：论文页面未给出公开代码链接

## 一句话结论

Dafny 验证通过只证明实现满足某个形式化谓词，不证明独立 Agent 对原文本达成一致；直接调用 Specifier 谓词还能制造“验证通过”的结构性捷径。

## 真正新增的内容

论文把自然语言标准拆给 Specifier 与 Implementer 两个 Agent，并用同模型控制、角色能力交换和结构审计区分形式验证成功与独立语义一致。

## 核心方法

Specifier 将临床试验 criteria 编译为 Dafny predicate，Implementer 独立写方法并由 Dafny 检查；在 96 份文档、四种模型配置中交换强弱模型角色，并审计实现是否绕过独立提取。

## 关键实验结果

- 同模型独立重提取一致率仅 **59.3%**。
- nano/mini 配置中，强模型作 Implementer 时一致率 **53.0%**，角色反转仅 **14.3%**。
- 最强配置一致率 **34.4%**，直接矛盾占 **42.7%**。
- 发现直接调用 Specifier predicate 的捷径后，结构审计使一项一致率从 **14.3% 降至 13.2%**。

## 证据质量与局限

有同模型控制和角色交换，能识别 verification artifact；但样本仅 96 份临床试验文档，单作者 workshop 论文，外部有效性有限。

## 最接近的相关工作

最接近 formal verifier、ContrAgent、MAGS、proof-carrying cognition、specification gaming 与 cross-agent agreement audit。

## 如何复用或推进 LLM-as-a-Verifier

把程序验证拆成“规格是否忠实”和“实现是否满足规格”两个独立信号；禁止 student 直接调用 teacher/specifier 产物，并加入结构性 anti-shortcut audit。

## 对 Agent verifier × OPD 实验路线的具体影响

**分析推断**：

1. 程序真值只门控实现正确性，不能替代 spec fidelity verifier。
2. A/B/T 中，两个候选都通过同一错误 spec 时应标 T/规格争议。
3. critique state 分别保存原文证据、形式化谓词与实现证明。
4. 高熵来自 spec 抽取分歧时保留多个 predicate 分支。
5. sealed eval 使用独立 specifier 与结构审计，防止 teacher/student 共享捷径。