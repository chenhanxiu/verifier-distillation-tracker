# Post-Audit Mirage：离线 Agent Verification 的可识别性边界

- **论文标题**：Post-Audit Mirage: Identifiability Limits of Offline Agent Verification
- **作者**：Aman Behera, Payal Payal
- **首次公开日期**：2026-10-22
- **版本日期**：2026-10-22（v1）
- **原始论文**：https://arxiv.org/abs/2610.31130
- **DOI / canonical URL**：https://doi.org/10.48550/arXiv.2610.31130
- **代码**：https://github.com/beingamanforever/Post-Audit-Mirage

## 一句话结论

若安全与有害部署向离线 verifier 暴露完全相同的证据，任何离线计算都无法区分它们；sealed eval 必须引入隔离的部署真值或明确输出 cannot determine。

## 真正新增的内容

**论文原文结论**：作者构造安全/有害成对 lifecycle，使 verifier 可见记录逐字节相同而隔离 scorer 的部署真值相反，并给出错误—弃权权衡；随后用 fresh group-labelled outcomes 的 IdentifiedRangeMonitor 输出 deploy、hold、cannot determine 或 unsupported。

**分析推断**：该工作把“评测泄漏/共适应”提升为可识别性问题：没有新增信息时，换更强 judge、更多推理 token 或更多投票都不能修复缺失真值。

## 核心方法

1. 在授权、调度、共享容量三个环境中构造 matched safe/harmful lifecycle。
2. 对公共审计记录实施精确等同，真实伤害只留在隔离 scorer。
3. 证明只见公共证据的规则存在不可避免的错误—弃权下界。
4. 更新固定后采集分组的真实伤害 observation。
5. 用置信范围返回四态决策，并对缺失组或违反采样假设 fail closed。

## 关键实验结果

**论文原文结论**：发布仓库报告 272 组成对 lifecycle、13,600 个逐字节相同公共轮次和 9 个离线诊断规则；在合成固定 panel 中，fresh monitoring 可在有利条件下恢复区分，但在稀有群体、小效应或缺失 observation 下经常只能返回 cannot determine。作者明确说明零观测 false-safe 不等于零部署风险。

## 证据质量与局限

有形式论证、可执行 benchmark、完整代码与合成实验，边界条件透明。局限是环境和监测数据为合成、假设分组与采集机制预先声明；不能证明现实部署的样本复杂度，也不能发现未声明选择偏差、MNAR 缺失或目标漂移。

## 最接近的相关工作

最接近 AutoTuneBench 的 sealed measurement、Proof-Carrying Cognition 的 reality settlement、Calibration Is Not Verification、ContrAgent/MAGS 的外部规范层，以及 distribution shift 下的 selective prediction。

## 如何复用或推进 LLM-as-a-Verifier

为 verifier 增加证据充分性头：输出 verdict 之前先判断该状态是否可识别；训练标签包含 cannot determine 与 unsupported。对长轨迹保留隔离环境结算通道，不让 policy、teacher 或训练 evaluator访问。

## 对 Agent verifier × OPD 实验路线的具体影响

**分析推断**：

- **score-level OPD**：不可识别样本的 teacher score 不应进入蒸馏；否则 student 只会学习任意决策边界。
- **A/B/T**：T 不只是“分数接近”，还应表示观测等价导致的结构性不可判定。
- **硬真值门控**：需要 post-update fresh outcome 或环境 settlement；离线日志不能替代。
- **critique states**：critique 必须声明依赖哪些未观测事实；缺证据时进入 unsupported 而非自信修复。
- **高熵探索**：对 cannot determine 状态保留探索并主动采集能打破等价性的 observation。
- **sealed eval**：隔离 scorer、公共轨迹与真实部署结果三者必须分权；评测应报告正确、错误、弃权和 unsupported 四类。
