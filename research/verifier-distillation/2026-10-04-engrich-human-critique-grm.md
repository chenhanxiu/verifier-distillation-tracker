# EnGRICH: Enhancing Generative Reward Modeling with Critiques from Humans

- 作者：Xuancheng Li、Beining Wang、Haitao Li、Heng Wang、Yujia Zhou、Qingyi Pan、Blaze Chen、Yiqun Liu、Min Zhang、Qingyao Ai
- 首次公开日期：2026-10-04
- 当前版本日期：2026-10-04（v1）
- arXiv：2610.05370
- 原始论文：https://arxiv.org/abs/2610.05370
- Canonical URL：https://doi.org/10.48550/arXiv.2610.05370
- 代码：未发现公开代码链接

## 一句话结论

【论文原文】EnGRICH 用少量人类 critique 训练 MetaCritic，检查 GRM 生成 critique 的证据覆盖与正确性，再把这些准则推广到只有最终偏好的大规模数据。

## 真正新增的内容

【论文原文】论文指出“偏好判对”不能证明 critique 可靠：有限的二元结果可能让错误解释被强化。MetaCritic 为每个回答构造专属 rubric，输出过程奖励和结构化探索指导，推理时 GRM 可独立运行。

## 核心方法

【论文原文】人类 critique 监督 MetaCritic；MetaCritic 评估生成 critique 的 evidence coverage/correctness，并在 GRM 训练中继续学习如何把人类评价准则迁移到 outcome-only preference 数据。

## 关键实验结果

【论文原文】在七个 reward-model 基准上，EnGRICH 一致优于竞争基线；机制分析支持 MetaCritic、过程奖励与结构化指导的有效性。摘要未给出统一绝对提升值。

## 证据质量与局限

【论文原文】跨七个基准且含机制分析，覆盖较广。局限是 MetaCritic 与 GRM 可能形成训练期共适应；人类 critique 的分布和质量决定可迁移边界；偏好基准未必检验真实 Agent 环境后果。

## 最接近的相关工作

最接近 UniRRM、PaperDoctor、EquiReview-R、FLARE，以及 outcome-supervised generative process verifier。

## 如何复用或推进 LLM-as-a-Verifier

【分析推断】把现有人工抽检的不一致样本写成“证据指针—错误类型—修复条件”critique，用 MetaCritic 蒸馏到大规模三 Judge 轨迹；MetaCritic 只作训练监督，最终仍由环境真值验收。

## 对 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：【分析推断】分别蒸馏 verdict score 与 critique-quality score，避免联合分数掩盖坏解释。
- **A/B/T 与序数分布**：【分析推断】证据不足的 critique 标 T；按覆盖与正确性形成二维序数标签。
- **硬真值门控**：【分析推断】MetaCritic 不能覆盖程序失败；环境证书拥有否决权。
- **critique states**：【分析推断】直接提供 student-generated critique 的准入模型与过程监督模板。
- **高熵探索**：【分析推断】MetaCritic 可指导探索不同 critique，但不得只保留单一高分解释。
- **sealed eval**：【分析推断】人类/环境封存集需独立于 MetaCritic 更新，单测 critique faithfulness。
