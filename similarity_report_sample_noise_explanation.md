# similarity_report_four_task_similarity_sweep_50x3.md 中 Sample Noise 的计算方式

## 对应指标

`results/similarity_report_four_task_similarity_sweep_50x3.md` 中的 sample noise 对应表格里的这一列：

```text
noise baseline
```

它来自每个 case 的 `noise_baseline` 字段。

## 核心公式

修改后的 RQ1 代码中，每个 case 的 sample noise 计算方式是：

```text
noise_baseline = original_noise
```

其中：

```text
original_noise = original prompt 下重复生成之间的平均 pairwise embedding distance

perturbed_noise = perturbed prompt 下重复生成之间的平均 pairwise embedding distance，仅作为诊断字段保留，不参与 RQ1 的 noise_baseline 计算
```

在 50x3 实验中，每个 prompt version 生成 3 次，所以每个 case 会有：

```text
original prompt outputs:  O1, O2, O3
perturbed prompt outputs: P1, P2, P3
```

## original_noise 如何计算？

对同一个 original prompt 的 3 个输出：

```text
O1, O2, O3
```

计算所有两两组合之间的 embedding distance：

```text
distance(O1, O2)
distance(O1, O3)
distance(O2, O3)
```

然后取平均：

```text
original_noise =
mean(
  distance(O1, O2),
  distance(O1, O3),
  distance(O2, O3)
)
```

它的含义是：

```text
在 original prompt 完全不变的情况下，模型重复生成本来会产生多少输出差异。
```

## perturbed_noise 如何计算？

对同一个 perturbed prompt 的 3 个输出：

```text
P1, P2, P3
```

计算所有两两组合之间的 embedding distance：

```text
distance(P1, P2)
distance(P1, P3)
distance(P2, P3)
```

然后取平均：

```text
perturbed_noise =
mean(
  distance(P1, P2),
  distance(P1, P3),
  distance(P2, P3)
)
```

它的含义是：

```text
在 perturbed prompt 固定不变的情况下，模型重复生成本来会产生多少输出差异。
```

## 为什么现在只使用 original_noise？

RQ1 的目标是建立一个不依赖扰动 prompt 的 sample-noise baseline。

因此，sample noise 应该只来自 original prompt 在未扰动条件下的重复生成差异：

```text
noise_baseline = original_noise
```

这样做的含义是：

```text
sample noise baseline 表示在没有 prompt perturbation 时，模型自身重复生成会产生多少语义漂移。
```

`perturbed_noise` 仍然可以被保留在结果表中，用于检查 perturbed prompt 下的重复生成稳定性，但它不再参与 RQ1 的主 sample-noise correction。

旧算法是：

```text
noise_baseline = (original_noise + perturbed_noise) / 2
```

新算法是：

```text
noise_baseline = original_noise
```

## embedding distance 如何计算？

代码中的距离函数是：

```text
distance = max(0, 1 - dot(embedding_i, embedding_j))
```

因为 embedding 向量已经用于 cosine-style comparison，所以这相当于：

```text
embedding distance = 1 - cosine similarity
```

数值含义：

```text
distance 越小，两个输出语义越相似。
distance 越大，两个输出语义差异越大。
```

## report 中的 noise baseline 如何聚合？

`similarity_report_four_task_similarity_sweep_50x3.md` 不是直接展示每个 case 的 `noise_baseline`，而是按：

```text
task × perturbation
```

分组后取平均。

例如 report 中这一行：

```text
factual_qa | SQuAD V2 | paraphrase | n=50 | noise baseline = 0.0373
```

含义是：

```text
在 factual_qa + paraphrase 这 50 个 case 中，
每个 case 先各自计算一个 noise_baseline，
然后对这 50 个 noise_baseline 取平均，
得到 report 中的 0.0373。
```

## 对应代码位置

每个 case 的 sample noise 计算在：

```text
four_task_similarity_sweep.py
```

修改后的关键代码：

```python
original_noise = avg_pairwise_distance(original_vectors)
perturbed_noise = avg_pairwise_distance(perturbed_vectors)
noise_baseline = original_noise
```

pairwise distance 函数：

```python
def avg_pairwise_distance(vectors):
    distances = [
        max(0.0, 1.0 - dot(vectors[i], vectors[j]))
        for i, j in all_pairwise_combinations
    ]
    return mean(distances)
```

report 中按 task × perturbation 聚合平均在：

```text
merge_similarity_batches.py
```

关键逻辑：

```python
"noise_baseline": statistics.mean(row["noise_baseline"] for row in rows)
```

## 一句话总结

```text
similarity_report_four_task_similarity_sweep_50x3.md 里的 sample noise，
是同一 prompt 下重复生成之间的平均 embedding drift。
修改后的 RQ1 代码只使用 original prompt 内部的重复生成漂移作为每个 case 的 noise_baseline，
最后在 report 中按 task × perturbation 分组取均值。
```
