# primitive-bar

Geom: `geom_bar()`

Use for counts by category.

```python
+ geom_bar()
```

Required mapping: `x`.

Common mapping: `fill='factor(category)'`.

Pairs with: `primitive-text` through `layer-stat-computed-labels`.

## Examples

### Count Bars

```python
ggplot(df, aes(x='factor(cyl)')) + geom_bar()
```

### Filled Count Bars

```python
ggplot(df, aes(x='factor(cyl)', fill='factor(cyl)')) + geom_bar()
```

### Count Bars With Text Labels

```python
+ geom_bar()
+ geom_text(aes(label=after_stat('count')), stat='count', format_string='{:.0f}')
```
