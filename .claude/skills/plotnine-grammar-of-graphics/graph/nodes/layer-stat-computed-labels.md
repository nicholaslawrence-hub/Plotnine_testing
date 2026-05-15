# layer-stat-computed-labels

Use for labels computed by a stat layer, especially bar counts and percentages.

Preferred pattern:

```python
+ geom_text(
    aes(label=after_stat('prop*100'), group=1),
    stat='count',
    nudge_y=0.5,
    format_string='{:.1f}%'
)
```

Do not use f-strings for values computed by Plotnine stats.

## Examples

### Percent Labels On Counts

```python
+ geom_text(
    aes(label=after_stat('prop*100'), group=1),
    stat='count',
    nudge_y=0.5,
    format_string='{:.1f}%'
)
```

### Count Labels On Bars

```python
+ geom_text(
    aes(label=after_stat('count')),
    stat='count',
    va='bottom',
    format_string='{:.0f}'
)
```

### Proportion Labels With Fill Groups

```python
+ geom_text(
    aes(label=after_stat('prop'), group=1),
    stat='count',
    format_string='{:.1%}'
)
```
