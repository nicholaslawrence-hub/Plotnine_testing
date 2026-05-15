# primitive-jitter

Geom: `geom_jitter()`

Use to show individual observations over a grouped summary.

```python
+ geom_jitter(width=0.15, alpha=0.4)
```

Pairs with: `primitive-boxplot`.

Keep jitter width small enough that points still belong visually to their group.

## Examples

### Jitter Over Groups

```python
+ geom_jitter(width=0.15, alpha=0.4)
```

### Jitter With Category Color

```python
ggplot(df, aes(x='factor(cyl)', y='mpg', color='factor(cyl)')) + geom_jitter(width=0.15, alpha=0.4)
```

### Boxplot Overlay

```python
+ geom_boxplot(alpha=0.6)
+ geom_jitter(width=0.15, alpha=0.4)
```
