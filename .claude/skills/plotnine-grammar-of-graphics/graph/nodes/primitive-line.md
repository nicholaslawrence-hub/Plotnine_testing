# primitive-line

Geom: `geom_line()`

Use for ordered trends or summarized series.

```python
+ geom_line(color='steelblue', size=1)
```

Required mappings: `x`, `y`.

Use `group` or `color` when multiple series are present.

Pairs with: `primitive-point`.

## Examples

### Single Trend Line

```python
ggplot(summary_df, aes(x='Age', y='Mental_Health_Score')) + geom_line(color='steelblue', size=1)
```

### Line With Point Markers

```python
+ geom_line(color='steelblue', size=1)
+ geom_point(color='steelblue', size=2)
```

### Multiple Series

```python
ggplot(summary_df, aes(x='Age', y='score', color='Gender', group='Gender')) + geom_line()
```
