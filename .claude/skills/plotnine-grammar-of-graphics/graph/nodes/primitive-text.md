# primitive-text

Geom: `geom_text()`

Use for labels. With computed bar labels, pair with `layer-stat-computed-labels`.

```python
+ geom_text(aes(label='label_col'), va='bottom')
```

For stat-computed labels, use `stat='count'`, `after_stat(...)`, and `format_string`.

## Examples

### Label From A Column

```python
+ geom_text(aes(label='car_name'), va='bottom')
```

### Count Labels

```python
+ geom_text(aes(label=after_stat('count')), stat='count', format_string='{:.0f}')
```

### Percent Labels

```python
+ geom_text(aes(label=after_stat('prop*100'), group=1), stat='count', format_string='{:.1f}%')
```
