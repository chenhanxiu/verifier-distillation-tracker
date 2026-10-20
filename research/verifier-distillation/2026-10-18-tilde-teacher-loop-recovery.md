# TILDE: Teacher-in-the-Loop Distillation from Embodied Foundation Models

- **作者**：Yuxiang Lu、Yantong Liu、Jinghua Hou、Xueli Sun、Ruihua Han、Zhe Liu、Hengshuang Zhao
- **首次公开日期**：2026-10-18
- **版本日期**：2026-10-18（v1）
- **原始论文**：https://arxiv.org/abs/2610.25376
- **arXiv ID**：2610.25376
- **DOI**：https://doi.org/10.48550/arXiv.2610.25376
- **代码/项目**：https://hku-sail.github.io/TILDE/

## 一句话结论

把 student-induced state 上的 OPD 与 teacher 实际执行的恢复轨迹结合，并由机器人 reward model 自动决定何时介入。

## 真正新增的内容

不仅让 teacher 对 student 状态打标签，还收集 teacher 从失败边缘恢复到成功的闭环行为，形成真实 recovery supervision。

## 核心方法

AutoDAgger 用机器人 RM 监控任务进度、触发 teacher 接管；训练统一使用示范、on-policy teacher 监督与 teacher corrective behavior。

## 关键实验结果

相对人工在环，恢复轨迹收集速度超过 2 倍；三个真实机器人任务中相对行为克隆最高提升 4.1 倍，并支持跨架构蒸馏。

## 证据质量与局限

真实机器人闭环与跨架构结果增强外部有效性；但 RM 的误触发/漏触发校准、硬件范围和安全失败成本仍需更细审计。

## 最接近的相关工作

与 Persistent Teacher Anchoring、STRIDE、AC-OPD、AutoGym 和 DAgger 最接近。

## 如何复用或推进 LLM-as-a-Verifier

把 student-generated critique state 与恢复动作绑定：只有 teacher 恢复后被环境验证成功，critique 才进入训练；RM 只负责路由介入，不单独定义真值。

## 对 Agent verifier × OPD 实验路线的具体影响

【分析推断】长时程 Agent OPD 应加入“失败检测—teacher takeover—环境结算—恢复片段蒸馏”分支，并单独评估触发策略，防止 verifier 与 policy 共同适应。

## 结论边界

除明确标注“分析推断”的段落外，上述方法与实验结论均来自论文原文或公开摘要；推断部分是面向现有研究路线的可检验假设，不应视为论文作者已经证明的结论。
