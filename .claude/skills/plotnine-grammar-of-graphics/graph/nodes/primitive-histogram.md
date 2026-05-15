# primitive-histogram

Geom: `geom_histogram()`

Use for numeric distributions.

```python
+ geom_histogram(bins=20, alpha=0.7)
```

Required mapping: `x`.

Common mappings: `fill` for groups.

Common companions: `layer-facets`, `layer-labels-theme`.

## Examples

### Basic Histogram

```python
ggplot(df, aes(x='Avg_Daily_Usage_Hours')) + geom_histogram(bins=20)
```

### Filled Histogram

```python
ggplot(df, aes(x='Avg_Daily_Usage_Hours', fill='Gender')) + geom_histogram(bins=20, alpha=0.7)
```

### Faceted Histogram

```python
+ geom_histogram(bins=20, alpha=0.7)
+ facet_wrap('Academic_Level')
```
