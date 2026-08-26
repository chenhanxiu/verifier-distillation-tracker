# RecurSE: Bounded Recursive Self-Evaluation for LLM Rubric Judges

## 基本信息

- 作者：Kaiyuan Liu、Ziyuan Zhuang、Rongxiang Weng、Jieping Ye
- 首次公开日期：2026-08-25
- 版本日期：2026-08-25（v1）
- arXiv：2608.24231
- 原始论文：https://arxiv.org/abs/2608.24231
- DOI：https://doi.org/10.48550/arXiv.2608.24231
- 代码：论文公开页未提供

## 一句话结论

LLM Judge 可以在无外部 gold reward 的闭环中自我改进，但必须隔离 verdict 与 checker 分数，并用独立的 Pairwise Advantage Validity 监控器及时停止，否则递归共适应会失效。

## 真正新增的内容

**论文原文结论：** RecurSE 让可训练 Judge 按逐条 rubric 评分，再由同步 policy-copy checker 按 meta-rubric 审计推理并产生过程奖励；PAV 同时监控 Judge 准确性和 checker fidelity，定位有限的有效训练窗口。

**分析推断：** 该论文并未消除 sealed eval 的需要，反而实证支持“训练闭环可以共演化，但停止规则必须来自与 verdict 解耦的验证信号”。

## 核心方法

Pass 1 生成 rubric verdict 与理由；Pass 2 使用同步 checker 审核理由，输出标量 process reward。接口隔离禁止 checker 复制 verdict token 形成虚假自奖励；PAV 以 pairwise advantage 的有效性判断何时早停。

## 关键实验结果

在 Qwen3.5-9B、Gemma-4-E4B-it、Qwen3.6-27B 上，对医疗、pairwise、摘要与专业 held-out benchmark 均取得泛化提升；同步共演化优于冻结 checker、外部 meta-judge、自一致性和扩大 teacher 蒸馏。摘要未披露逐项绝对增益。

## 证据质量与局限

证据质量中等：跨三个模型家族和多领域并含多种消融，但缺少摘要级效应量、代码与人工一致性细节。PAV 仍属于内部验证量，不能证明 Judge 在真正未知分布上没有共适应。

## 最接近的相关工作

最接近 Rubric Dropout、JuryProbe、MuseCritic、self-rewarding judge 与 process-supervised reward modeling。差异是显式建模递归自评的停止边界和 token-copy shortcut。

## 如何复用或推进 LLM-as-a-Verifier

三 Judge 投票系统可增加独立 checker：只审计理由是否满足 meta-rubric，不读取最终分数；训练期间用 PAV 类指标监控，但模型选择仍由冻结人工锚点和环境真值决定。

## 对 Agent verifier × OPD 实验路线的具体影响

- **Score-level OPD：** 可蒸馏 checker 的过程分数，但需与最终 verdict token 解耦。
- **A/B/T：** 以 pairwise advantage validity 监控排序信号是否仍有方向性。
- **真值门控：** 可程序化维度必须作为外部 anchor，不能由递归 Judge 自证。
- **Student critique states：** checker 审计 student critique 的证据链，而不是复述其结论。
- **高熵探索：** PAV 下降时停止强化，避免低质量共识压平探索。
- **Sealed eval：** 保留完全不参与 Judge/checker 更新的人工与环境测试集，这是本文框架外仍必需的防线。
