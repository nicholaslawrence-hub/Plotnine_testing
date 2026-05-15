# example-scatter-trend

Rendered asset:

```text
assets/fewshots/scatter_with_trend.png
```

Use this as the canonical few-shot for:

```text
intent-relationship -> primitive-point -> primitive-smooth -> layer-aesthetic-mapping -> layer-labels-theme -> output-save
```

Prompt:

```text
Create a scatter plot of hp vs mpg, color by cyl as a category, add a linear trend line, and save to output.png.
```

Code:

```python
from plotnine import *
from plotnine.data import mtcars
import pandas as pd

df = pd.DataFrame(mtcars)
p = (
    ggplot(df, aes(x='hp', y='mpg', color='factor(cyl)'))
    + geom_point(alpha=0.8, size=3)
    + geom_smooth(method='lm', se=False)
    + labs(title='Horsepower vs MPG', x='Horsepower', y='Miles per gallon', color='Cylinders')
    + theme_minimal()
)
p.save('output.png', dpi=150, width=8, height=6)
```

Judge expectation:

The chart should visibly show points, a linear trend line, categorical cylinder coloring, useful labels, and a saved nonblank image.

