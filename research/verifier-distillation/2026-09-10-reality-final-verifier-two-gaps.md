# Reality Is the Final Verifier：Agent 软件工程的“两类差距”

## 基本信息

- **论文标题**：Reality Is the Final Verifier: On Two Key Gaps in Agentic Software Engineering
- **作者**：Alexander Krentsel, Shubham Agarwal, Mert Cemri, Shu Liu, Sidharth Sankhe, Ziming Mao, Matei Zaharia, Ion Stoica
- **首次公开日期**：2026-09-10
- **版本日期**：2026-09-10（v1）
- **原始论文**：https://arxiv.org/abs/2609.12039
- **DOI**：https://doi.org/10.48550/arXiv.2609.12039
- **代码**：无

## 一句话结论

【论文原文】测试、形式证明和预部署 evaluator 都只是代理；Agent 软件工程必须持续用部署现实收窄“需求—意图差距”和“模型—环境差距”。

## 真正新增的内容

【论文原文】以 two-gap framework 统一 reward hacking 与 hallucination：前者利用需求或环境模型遗漏，后者通过虚构需求/环境假设扩大差距；据此提出 assurance-revision loop，用部署证据修订需求、模型或 evaluator，而不是声称一次性验证闭合。

## 核心方法

这是概念与框架论文：把实现—验证循环形式化为需求、环境模型和 evaluator 的代理链；再将可靠 Agent 开发视为在人类判断、Agent 能力和计算预算之间的资源分配问题。

## 关键实验结果

【论文原文】摘要未报告新的对照实验或量化基准；主要贡献是概念框架和工程议程，因此不应把它解读为已验证的算法提升。

## 证据质量与局限

【论文原文】论证直接对应开放、变化环境中的验证边界，作者背景与问题设定具有参考价值；但缺少实证、可复现实验和具体算法，two-gap 的可测量性与预算策略仍待检验。

## 最接近的相关工作

Reward hacking、Goodhart 定律、specification gaming、Proof-Carrying Cognition、Harness-of-Harness、Cheap Verifiers Large Blind Spots、RecurSE，以及 sealed deployment evaluation。

## 如何复用或推进 LLM-as-a-Verifier

【分析推断】将 verifier 输出拆成两套分布：需求满足度与环境模型可信度；任何一项证据不足即返回 T/INCONCLUSIVE。程序化检查只能门控模型内可验证部分，部署反馈应保留不可被 LLM Judge 覆盖的否决权。

## 对 Agent verifier × OPD 实验路线的具体影响

【分析推断】score-level OPD 不应优化单一“成功分”，而应分别蒸馏 requirement-gap 与 model-gap 风险。student-generated critique 要标注依据来自规范、模拟器还是现实结算；高熵分叉在两类差距未收敛时继续探索。sealed eval 除冻结 evaluator 外，还要使用独立需求审查和环境外现实回放，监测 evaluator 共适应。