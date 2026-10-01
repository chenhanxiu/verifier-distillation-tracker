# OPSRD: On-Policy Self-Role Distillation

- **作者**：Weijie Ren, Yanwen Zhang, Hao Li, Zhuolin Qi, Hengyi Zhang, Naibo Wang
- **首次公开日期**：2026-09-30
- **版本日期**：2026-09-30（v1）
- **原始论文**：https://arxiv.org/abs/2609.39884
- **代码**：https://github.com/zhansan114514/OPSRD

## 一句话结论

OPSRD 用同一模型的固定专家角色作为 privileged teacher，只在 student 最高熵的一半位置做 forward-KL，自蒸馏无需参考解。

## 真正新增的内容

【论文原文】完整答案错误并不代表 role-conditioned teacher 在每个前缀上的 next-token preference 无用。OPSRD 在 student 原始前缀上查询同模型的专家角色分布，以 teacher-weighted forward KL 覆盖 student 低估的替代 token，并限制单词表项贡献。

【分析推断】它提供一种廉价多角色 verifier teacher，但角色知识没有外部真值锚定，适合作为探索建议而不是裁决层。

## 核心方法

role-free student 生成 on-policy 轨迹；冻结的同基座模型带专家角色重评分；只对最高熵 50% token 蒸馏，使用带 clipping 的 teacher-weighted forward KL。

## 关键实验结果

【论文原文】Qwen3-1.7B、4B、8B 在三个竞赛数学基准上均优于无 role 的 base；三种 KL 中 forward KL 在每个尺度的宏平均准确率最高。

## 证据质量与局限

有多尺度和 KL 对照，代码公开；但仅数学任务，且 teacher 与 student 同源，角色提示可能放大共同错误，未验证长轨迹或 reward hacking。

## 最接近的相关工作

OPSD、SCOPE-OPSD、VG-OPD、MOPD-Router、Data-free OPD。

## 如何复用或推进 LLM-as-a-Verifier

为不同评价维度建立角色 teacher，并把它们的分歧蒸馏成序数分布；任何影响执行方向的信号必须再由环境验证。

## 对 Agent verifier × OPD 实验路线的具体影响

【分析推断】

- **score-level OPD**：高熵门控可作为低成本状态筛选，再叠加 verifier score。
- **A/B/T 与序数分布**：多角色输出形成 panel；同源相关性需校正，分歧时保留 T。
- **硬真值门控**：角色 teacher 只定幅度/候选，不得覆盖程序真值。
- **student-generated critique states**：可让 student 生成 critique 后由多角色重评分。
- **高熵分叉**：只监督高熵位置契合探索预算，但 forward KL 仍需防过度扩散。
- **sealed eval**：使用不同模型族和冻结环境做最终验证，避免自评自证。
