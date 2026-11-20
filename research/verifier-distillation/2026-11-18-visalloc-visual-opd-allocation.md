# VisAlloc: Allocating Visual Supervision for On-Policy Self-Distillation

- **作者**：Haoran Xu, Tian Chen, Yuhe Wu, Yanbo Zhao, Junchi Liao, Hongyu Wang, Jiaze Li, Wentao Wang, Yanfeng Li, Rui Qian
- **首次公开日期**：2026-11-18
- **版本日期**：2026-11-18（v1）
- **原始论文**：[arXiv:2611.25069](https://arxiv.org/abs/2611.25069)
- **DOI**：[10.48550/arXiv.2611.25069](https://doi.org/10.48550/arXiv.2611.25069)
- **代码**：[Kaelyn01/VisAlloc](https://github.com/Kaelyn01/VisAlloc)

## 一句话结论

【论文原文】VisAlloc 用正/负视觉裁剪的反事实差异在样本级筛选、token 级分配 OPSD 监督；【分析推断】其“对同一 student rollout 做成对 teacher 干预，再按差分分配额外权重”可直接迁移到 Agent verifier 的环境证据门控与高熵状态 credit allocation。

## 真正新增的内容

【论文原文】相对均匀 token 蒸馏，VisAlloc 同时决定“哪些样本值得视觉 privileged supervision”和“同一样本哪些 token 真正依赖证据”。它用证据中心正裁剪与空间错位负裁剪构造可控反事实，而非仅依赖 teacher–student gap。

【分析推断】该设计把 verifier 信号从一个结果分数拆成“样本准入 + token 幅度”两级，适合复用到长轨迹的状态/动作监督预算分配。

## 核心方法

【论文原文】

1. 固定成对 teacher：正裁剪含关键证据，负裁剪空间错位；
2. 仅保留正 teacher 答对且负 teacher 答错的样本；
3. 两个 EMA teacher 对同一 student-generated response 打分；
4. 用绝对 log-prob 差衡量 view sensitivity，并结合 teacher 分布分歧、冻结 prior、模板 bigram 与 student–teacher divergence 门控 token；
5. 逆频率重分配保持每个 micro-batch 的额外权重总量，正 teacher 是唯一蒸馏目标。

## 关键实验结果

【论文原文】

- 4B 与 9B 模型在八个 benchmark 上 macro-average 分别为 81.44 与 84.92。
- 相对 Vision-OPD 复现分别提升 0.97 与 0.52 点。
- 推理时只需全图 student，不保留成对 teacher。

## 证据质量与局限

【论文原文】包含两种规模、八个 benchmark、明确的反事实筛选和可复现代码。局限是提升幅度中等，任务为视觉推理而非长时程工具 Agent；正/负裁剪依赖已有空间证据定位，未证明在开放环境中可自动构造可靠反事实。

【分析推断】绝对 log-prob 差能衡量敏感性，但不保证方向正确；必须由环境真值或因果干预验证“差异来自任务证据而非伪特征”。

## 最接近的相关工作

- Vision-OPD 与 OPD-Aha：使用 privileged visual evidence 做 on-policy distillation。
- AC-OPD：在高分歧 student 状态自适应请求 teacher continuation。
- Unified Per-Token OPD Gating：组合熵、teacher–student gap 与样本不确定性。
- IWD：按 teacher 在语义保持扰动下的不变性加权蒸馏。

## 如何复用或推进 LLM-as-a-Verifier

【分析推断】在 Agent 轨迹上构造正/负证据视图：正视图含真实工具回执、环境状态或成功证书；负视图删除、错位或替换关键证据。对同一 student rollout 计算 verifier 分布差，把差异大的状态/动作送入 score-level OPD；仅当正视图通过硬真值且负视图失败时准入。

## 对现有 Agent verifier × OPD 实验路线的具体影响

【分析推断】

- **score-level on-policy verifier distillation**：把额外监督预算集中到环境证据敏感的 token/状态，而非全轨迹均匀 KL。
- **pairwise A/B/T 与序数评分分布**：正/负视图可形成 A/B；两者都通过或都失败时标 T/不可辨，而非硬排序。
- **程序化/环境真值门控**：沿用“正对负错”筛选，但把视觉裁剪换成可执行证据干预。
- **student-generated critique states**：仅在 critique 对真实证据敏感且对错位证据不敏感时准入。
- **高熵分叉保留探索**：teacher 分歧或 view sensitivity 高时提高分叉预算，不强制单一路径。
- **独立 sealed eval**：使用未参与正/负干预生成的环境实例和冻结 oracle，防止学会干预模板。
