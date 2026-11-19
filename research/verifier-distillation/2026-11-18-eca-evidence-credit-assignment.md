# Evidence-Based Credit Assignment for Search-Augmented Language Models

- **作者**：Wen Wang、Jindong Wang、Jiahua Bao、Tu Yongsiqi、Yihao Liu、Junwei He、Wenkui Fan
- **首次公开日期**：2026-11-18
- **版本日期**：2026-11-18（v1）
- **原始论文**：https://arxiv.org/abs/2611.23824
- **代码链接**：未发现公开代码
- **标识符**：arXiv:2611.23824；DOI: 10.48550/arXiv.2611.23824

## 一句话结论

【论文原文】ECA 用冻结策略在 evidence-only prompt 下测量检索文档对参考答案似然的增量，为终局全失败时仍提供局部搜索信用，并显著改善搜索增强模型的 GRPO。

## 真正新增的内容

【论文原文】提出训练期辅助 potential：只输入问题和截至当前去重后的证据文档，排除思维文本与查询措辞，测量证据对 reference answer 的贡献；比较逐步截断增量 ECA-Step 与保持 telescoping horizon gain 的 ECA-Horizon，并结合 cross-fold normalization、novelty gate 和 search-local token assignment。

## 核心方法

1. Terminal answer reward 保留为方向性 outcome 信号。
2. 冻结当前策略 snapshot，在 evidence-only context 中计算 reference-answer likelihood。
3. 证据 potential 的增量只分配给相关 search token，减少整轨迹同奖。
4. ECA-Horizon 保留从初始到终局的总证据增益，避免逐步 clipping 破坏守恒。

## 关键实验结果

【论文原文】七个 Search QA 基准上，ECA-Horizon 相对 outcome-only GRPO 的 strict macro exact match 在 Qwen2.5-3B/7B 上提高 1.03/4.80 个百分点，并超过 RLOO 与 GiGPO；MultiHop-RAG 零样本评测显示多跳迁移。

## 证据质量与局限

【论文原文】覆盖七个基准、两种规模和多个 RL baseline，并隔离证据而非语言表面；但仍需参考答案，frozen policy likelihood 只是证据价值代理，可能偏好模型已熟悉的表述。实验集中于 Search QA，尚未验证通用工具 Agent。

## 最接近的相关工作

接近 process reward、potential-based reward shaping、GiGPO/RLOO、retrieval credit assignment、BATON/RECAP 与 evidence-grounded verifier。关键差异是证据-only frozen snapshot 和 search-local 信用。

## 如何复用或推进 LLM-as-a-Verifier

【分析推断】把长轨迹中的环境观察、工具返回和 critique 视为 evidence set，用冻结 verifier 测量“新增证据对最终正确 verdict 的信息增益”；硬 outcome 定方向，evidence potential 调幅度，避免对无用工具调用平均分配信用。

## 对现有 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：采用终局硬分数 + evidence-only potential 的分层目标，并验证信用守恒。
- **pairwise A/B/T 与序数分布**：同一分叉按新增证据价值比较；两者均无增量或证据冲突时保留 T。
- **程序化/环境真值门控**：最终环境结果不可被 soft potential 反转，potential 只调整局部幅度。
- **student-generated critique states**：critique 只有在增加可验证证据或提高 reference verdict likelihood 时获得正信用。
- **高熵分叉探索**：终局全失败时仍可依据 evidence gain 保留有希望分支，而不让 group advantage 全归零。
- **sealed eval**：冻结 reference、snapshot 与 evidence parser，另用未见检索源检查代理分数是否被利用。
