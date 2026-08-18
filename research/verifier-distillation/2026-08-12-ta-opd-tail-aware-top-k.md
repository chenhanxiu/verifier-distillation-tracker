# TA-OPD：保留尾部概率的 Top-k On-Policy Distillation

## 基本信息
- **论文标题**：Tail-Aware Top-k On-Policy Distillation
- **作者**：Huipeng Huang, Hongxin Wei
- **首次公开日期**：2026-08-12
- **版本日期**：2026-08-12（v1）
- **原始论文**：https://arxiv.org/abs/2608.14728
- **DOI**：10.48550/arXiv.2608.14728
- **代码**：https://github.com/HuipengHuang/TA-OPD

## 一句话结论
常见 top-k OPD 归一化会丢掉 teacher 的尾部总质量，导致 student 尾部概率和熵异常上升；TA-OPD 用一个 tail token 显式承载剩余概率，直接关系到高熵分叉下“保留探索但不制造虚假尾部”的目标。

## 真正新增的内容
**论文原文**：在 teacher top-k token 外增加一个聚合 tail 类，最小化 top-k+tail 上的 reverse KL；无需额外 teacher query，即可恢复被 top-k 归一化抹掉的概率约束。

**分析推断**：Agent verifier 的 ordinal bins/A/B/T 也应显式保留“其他/未知/不可判”质量，避免截断后重新归一化造成虚假确信。

## 核心方法
teacher 提供 top-k 概率及其和，剩余概率写入 tail token；student 对相同分组计算 reverse KL。论文还给出 sampled variant，在可获得 sampled token 概率时无偏估计 full-vocabulary RKL。

## 关键实验结果
三组 student–teacher 配对、六个数学基准与 ARC-c/MMLU-Pro OOD 评测上，TA-OPD 的平均准确率均优于 normalized top-k。相对后者，Qwen2.5-7B 数学平均 +5.26，Llama-3.1-8B +8.05；Llama MATH500 从 31.30 到 50.83。normalized top-k 训练中 tail probability 约升至 0.5–0.6、student entropy 约 6；TA-OPD 将 tail 接近 0、entropy 低于 1.5。

## 证据质量与局限
有理论分析、多个模型对、ID/OOD 评测、训练动态与代码。局限是最大 8B；当 k 增大或师生差距减小时收益变小；“尾部接近零”不代表所有任务都应压低探索，尤其 Agent 高熵节点可能有真实多解。

## 最接近的相关工作
top-k/sampled-token OPD、MiniLLM、GKD、sparse KL、SPOT、EOPD/AED。TA-OPD 解决的是被归一化遗失的总概率质量，而非候选的下游价值。

## 如何复用或推进 LLM-as-a-Verifier
对 A/B/T 外增加 Unknown/Other mass；对序数分布只暴露 top bins 时保留 omitted mass。训练和接口同时报告 entropy 与 tail mass，避免把“未覆盖”误当 Tie 或低分。

## 对 Agent verifier × OPD 路线的影响
1. **score-level**：完整保存分布总质量，不只蒸馏 top buckets。
2. **A/B/T**：加入 Unknown；环境证据不足时不强行归一化到 A/B/T。
3. **真值门控**：真实成功分支若落入 tail，应提升而非压掉。
4. **critique states**：追踪 critique 候选的 tail mass，识别分布外状态。
5. **探索**：区分“虚假尾部膨胀”与“真实高熵多解”，结合 SPOT 式 continuation 验证。
6. **sealed eval**：单独测 tail calibration、coverage 与 OOD ranking。

## 结论边界
论文证明 top-k 归一化可造成严重尾部漂移，但不证明低熵总是更好；Agent 场景必须用环境 outcome 校验尾部候选的真实价值。
