# SARA：用 On-Policy Self-Distillation 缓解 LLM Judge 的 Rubric 干扰

## 基本信息
- **论文标题**：Mitigating Rubric Interference in LLM Judges via On-Policy Self-Distillation
- **作者**：Dingyao Yu, Tong Zhang, Yutao Mou, Yunxiao Zhang, Wei Ye, Shikun Zhang
- **首次公开日期**：2026-08-05（本次进入 arXiv new submissions 检索窗口）
- **版本日期**：2026-08-05（v1）
- **原始论文**：https://arxiv.org/abs/2608.14684
- **DOI**：10.48550/arXiv.2608.14684
- **代码**：未发现公开链接

## 一句话结论
SARA 把单 rubric 判断当作稳定 anchor，再沿模型自己生成的 multi-rubric 输出进行 on-policy self-distillation，直接命中 LLM-as-a-Verifier 的“多维指标相互污染”问题；但一致性提升不等于正确性提升。

## 真正新增的内容
**论文原文**：rubric 扩展、删减、重排和噪声注入都会改变其他 rubric 的 verdict，初步实验仅约三分之一样本在不同 rubric 组合下完全一致。SARA 用单 rubric isolation verdict/analysis 指导 joint-mode，并对结构 token 做 preservation。

**分析推断**：可将现有 Agent verifier 的能力、合规、工具正确性、最终贡献度等 rubric 分头打分后，再蒸馏成一次性多维 judge；sealed eval 必须用人工或独立 judge 验证，否则可能只学会自洽。

## 核心方法
EMA teacher 提供隔离 rubric 下的 analysis/verdict；student 在完整 rubric 集下生成。只对 rubric 对应分析片段做 JSD 对齐，结构 token 用 full-context teacher 保持；训练时随机 rubric 顺序并加入无关 rubric 噪声。

## 关键实验结果
覆盖 HealthBench（二元、每样本 2–32 rubrics）、FLASK（3 个 1–5 分维度）和 ResearchQA（1–8 个、0–4 分 rubric），模型为 Qwen3 8B/14B/32B 与 Llama-3.1-8B。论文报告各数据集与模型上改善 shuffle/subset/noise consistency，同时维持与 base model 和 GPT-4.1 的一致性，并存在跨数据集迁移。

## 证据质量与局限
优点是干预类型完整、多评分格式、多模型家族，并用 attention 分析解释跨 rubric 流抑制。局限是 isolation verdict 被假设为无干扰 anchor；共同上下文有时能带来有益交互，SARA 无法区分。thinking-mode 分段较不可靠、收益较小。论文明确指出 consistency 不保证 correctness。

## 最接近的相关工作
multi-rubric reward modeling、rubric dropout/interference、self-anchored distillation、LLM-as-a-Judge calibration、multi-task gradient interference。

## 如何复用或推进 LLM-as-a-Verifier
先分别运行 action relevance、tool validity、constraint compliance、long-term contribution 等单 rubric teacher，得到序数分布与 critique；再蒸馏到一次性 multi-rubric student。训练目标应同时保留 rubric 间相关性与独立性。

## 对 Agent verifier × OPD 路线的影响
1. **score-level**：每个 rubric 独立生成 teacher score distribution，再联合蒸馏。
2. **A/B/T**：每个 rubric 输出 A/B/T，聚合层不得覆盖原始分布。
3. **真值门控**：工具/环境可验证 rubric 以程序真值覆盖 self-anchor。
4. **critique states**：student 生成联合 critique，teacher 分 rubric 回标。
5. **探索**：若 rubric 间冲突导致高熵，应保留而非强制一致。
6. **sealed eval**：人工/冻结 judge 分别评估正确性和一致性，防止 evaluator 自我复制。

## 结论边界
论文证明可减少 rubric 干扰，不证明 judge 更接近人类或环境真值；现有路线应把 SARA 视为接口稳定化层，而不是最终质量保证。
