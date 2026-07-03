# RQ2 Correlation Metrics Explanation

## 这些列在回答什么

在 RQ2 中，我们主要看：

```text
similarity drift 是否能够指示 correctness drift
```

表格里的这几列用于描述二者之间的相关关系：

| Column | 中文含义 | 主要作用 |
|---|---|---|
| `pearson` | Pearson 相关系数 | 看两个变量是否呈线性关系 |
| `spearman` | Spearman 排名相关系数 | 看两个变量的排序是否一致 |
| `spearman_ci95_low` | Spearman 95% 置信区间下界 | 看 Spearman 估计的稳定范围下限 |
| `spearman_ci95_high` | Spearman 95% 置信区间上界 | 看 Spearman 估计的稳定范围上限 |

## Pearson 是什么

`pearson` 衡量两个变量之间的线性关系。

范围：

```text
-1 到 1
```

解释：

| Pearson 值 | 含义 |
|---:|---|
| 接近 1 | 一个变量增大，另一个变量也近似线性增大 |
| 接近 0 | 没有明显线性关系 |
| 接近 -1 | 一个变量增大，另一个变量近似线性减小 |

在 RQ2 里：

```text
pearson = similarity drift 和 correctness drift 的线性关联强度
```

例如：

```text
pearson = 0.328
```

表示 similarity drift 越大，correctness drift 通常也越大，但线性关系不是很强。

## Spearman 是什么

`spearman` 衡量两个变量之间的排名关系，也叫 rank correlation。

它不要求两个变量呈线性关系，只看排序是否一致。

在 RQ2 里：

```text
spearman = similarity drift 排名前面的 cases，correctness drift 是否也通常排在前面
```

例如：

```text
spearman = 0.346
```

表示 semantic drift 较大的 case，通常 correctness drift 也较大，存在中等偏弱的正向排序关系。

## 为什么 RQ2 更重视 Spearman

RQ2 的 correctness drift 通常是离散值。

例如 3 samples per prompt version 时，correctness mean 只能是：

```text
0, 0.333, 0.667, 1.0
```

所以 correctness drift 也不是连续平滑变量。

这种情况下，Pearson 的线性假设比较强，而 Spearman 只看排序，更稳健。

因此 RQ2 里通常建议：

```text
Spearman 作为主解释指标，Pearson 作为辅助指标。
```

## spearman_ci95_low 和 spearman_ci95_high 是什么

这两个值是 Spearman 相关系数的 95% bootstrap confidence interval。

意思是：

```text
在重复抽样估计下，真实 Spearman 相关系数大致落在这个区间内。
```

例如：

```text
spearman = 0.346
spearman_ci95_low = 0.188
spearman_ci95_high = 0.503
```

可以解释为：

```text
Spearman 的估计值是 0.346，95% bootstrap 区间大约是 [0.188, 0.503]。
```

这说明：

- 相关关系是正向的。
- 区间没有跨过 0。
- 因此这个正相关比较稳定。

## CI 怎么读

| CI 情况 | 解释 |
|---|---|
| 整个区间都大于 0 | 稳定正相关 |
| 整个区间都小于 0 | 稳定负相关 |
| 区间跨过 0 | 相关方向不稳定，证据较弱 |
| 区间很窄 | 估计较稳定 |
| 区间很宽 | 不确定性较大 |

例如：

```text
[0.188, 0.503]
```

说明结果比较稳定，是正相关。

再比如：

```text
[-0.162, 0.535]
```

说明区间跨过 0，不能稳定判断是正相关还是无关系。

## 在当前 RQ2 结果中的例子

总体主结果：

| pearson | spearman | spearman_ci95_low | spearman_ci95_high |
|---:|---:|---:|---:|
| 0.328 | 0.346 | 0.188 | 0.503 |

解释：

```text
similarity drift 和 correctness drift 存在稳定的中等偏弱正相关。
```

更具体地说：

- Pearson = 0.328：线性关联为正，但不是强线性关系。
- Spearman = 0.346：排序关系为正，semantic drift 较大的 case 通常 correctness drift 也较大。
- CI = [0.188, 0.503]：bootstrap 区间不跨 0，说明正相关比较稳定。

## 推荐写法

论文或报告里可以这样写：

> The primary RQ2 result shows a moderate positive association between noise-corrected semantic drift and correctness drift. The Spearman correlation is 0.346 with a 95% bootstrap confidence interval of [0.188, 0.503], indicating a stable positive rank association.

中文可以写成：

> RQ2 主结果显示，noise-corrected semantic drift 与 correctness drift 存在中等偏弱的正相关。Spearman 相关系数为 0.346，95% bootstrap 置信区间为 [0.188, 0.503]，说明 semantic drift 较大的 case 通常 correctness drift 也较大，并且这一正相关较稳定。

## 补充：spearman_ci95_low / spearman_ci95_high 更具体是什么意思

`spearman_ci95_low` 和 `spearman_ci95_high` 是一对值，必须放在一起看。

它们表示：

```text
Spearman correlation 的 95% bootstrap confidence interval
```

也就是：

```text
如果我们从当前 150 个 case 中反复有放回抽样，重新计算很多次 Spearman，
那么中间 95% 的 Spearman 估计值大致落在 [low, high] 这个范围里。
```

在当前脚本里，做法可以理解为：

1. 从 150 个 case-level rows 中随机抽样 150 个，允许重复抽到同一个 case。
2. 用这批 bootstrap sample 重新计算一次 Spearman。
3. 重复很多次。
4. 把这些 Spearman 值排序。
5. 取第 2.5% 位置作为 `spearman_ci95_low`。
6. 取第 97.5% 位置作为 `spearman_ci95_high`。

所以：

```text
spearman_ci95_low = 这个相关性估计的合理下界
spearman_ci95_high = 这个相关性估计的合理上界
```

## 为什么需要 CI

单独看一个 Spearman 值不够。

例如：

```text
spearman = 0.35
```

这只说明当前样本上相关系数是 0.35。

但我们还需要知道：

```text
这个 0.35 稳不稳定？
换一批类似样本后，它还会是正的吗？
```

CI 就是用来表达这种不确定性的。

## 三种典型情况

### 情况 1：CI 完全大于 0

例如：

```text
spearman = 0.346
spearman_ci95_low = 0.188
spearman_ci95_high = 0.503
```

解释：

```text
95% bootstrap 区间是 [0.188, 0.503]，整个区间都大于 0。
```

这说明：

- 相关方向稳定为正。
- semantic drift 较大的 case 通常 correctness drift 也较大。
- 可以较有信心地说存在正向 rank association。

### 情况 2：CI 跨过 0

例如：

```text
spearman = 0.224
spearman_ci95_low = -0.162
spearman_ci95_high = 0.535
```

解释：

```text
95% bootstrap 区间是 [-0.162, 0.535]，包含 0。
```

这说明：

- 当前样本上的 Spearman 是正的。
- 但 bootstrap 后，有些样本会得到负相关或接近 0 的结果。
- 因此不能稳定声称有正相关。

这种结果应该写得保守：

```text
The association is positive in point estimate but uncertain, with a confidence interval crossing zero.
```

中文：

```text
点估计为正，但置信区间跨过 0，因此该正相关证据不稳定。
```

### 情况 3：CI 很宽

例如：

```text
spearman = 0.30
spearman_ci95_low = -0.10
spearman_ci95_high = 0.70
```

这说明：

- 样本量可能不够。
- 数据噪声较大。
- 不同 bootstrap sample 得到的相关性差异很大。
- 结论需要谨慎。

## CI 宽窄说明什么

| CI 宽度 | 含义 |
|---|---|
| 窄 | 估计稳定，样本扰动后结果变化不大 |
| 宽 | 估计不稳定，样本扰动后结果变化较大 |
| 跨 0 | 相关方向不稳定 |
| 不跨 0 | 相关方向较稳定 |

## CI 和 p-value 的区别

`spearman_ci95_low/high` 和 `spearman_permutation_p_two_sided` 都和统计可靠性有关，但回答的问题不同。

| 指标 | 回答的问题 |
|---|---|
| CI | 相关系数的可能范围是多少？ |
| p-value | 如果真实没有关系，观察到这么强相关的概率有多小？ |

例如：

```text
spearman = 0.346
CI = [0.188, 0.503]
p = 0.001
```

可以解释为：

- CI 告诉我们：Spearman 的合理范围大约是 0.188 到 0.503。
- p-value 告诉我们：如果两个变量完全无关，随机打乱后得到这么强相关的概率很小。

## 在 RQ2 中的推荐判断规则

建议这样读：

1. 先看 `spearman` 的方向和大小。
2. 再看 `spearman_ci95_low/high` 是否跨 0。
3. 如果 CI 不跨 0，再看区间宽不宽。
4. 最后用 permutation p-value 作为补充证据。

简化判断：

| 结果模式 | 建议解释 |
|---|---|
| Spearman > 0, CI > 0 | 稳定正相关 |
| Spearman > 0, CI 跨 0 | 正相关证据不稳定 |
| Spearman 接近 0, CI 跨 0 | 没有稳定关系 |
| Spearman < 0, CI < 0 | 稳定负相关 |

