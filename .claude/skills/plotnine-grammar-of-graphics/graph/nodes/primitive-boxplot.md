# primitive-boxplot

Geom: `geom_boxplot()`

Use for comparing numeric distributions by category.

```python
+ geom_boxplot()
```

Required mappings: categorical `x`, numeric `y`.

Common mappings: `fill='factor(group)'`.

Pairs with: `primitive-jitter`.

## Examples

### Boxplot By Numeric Category

```python
ggplot(df, aes(x='factor(cyl)', y='mpg')) + geom_boxplot()
```

### Filled Boxplot

```python
ggplot(df, aes(x='factor(cyl)', y='mpg', fill='factor(cyl)')) + geom_boxplot()
```

### Boxplot With Jitter

```python
+ geom_boxplot()
+ geom_jitter(width=0.15, alpha=0.4)
```
