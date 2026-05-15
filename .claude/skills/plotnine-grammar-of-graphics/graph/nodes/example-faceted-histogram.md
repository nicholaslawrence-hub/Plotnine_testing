# example-faceted-histogram

Rendered asset:

```text
assets/fewshots/faceted_histogram.png
```

Use this as the canonical few-shot for:

```text
intent-distribution -> primitive-histogram -> layer-facets -> layer-aesthetic-mapping -> layer-labels-theme -> output-save
```

Prompt:

```text
Create a histogram of usage hours filled by gender, faceted by academic level, and save to output.png.
```

Code:

```python
from plotnine import *
import pandas as pd

df = pd.read_csv('example_datasets/Social_media_impact_on_life.csv')
p = (
    ggplot(df, aes(x='Avg_Daily_Usage_Hours', fill='Gender'))
    + geom_histogram(bins=20, alpha=0.7)
    + facet_wrap('Academic_Level')
    + labs(title='Daily Social Media Usage', x='Average daily usage hours', y='Count', fill='Gender')
    + theme_bw()
)
p.save('output.png', dpi=150, width=8, height=6)
```

Judge expectation:

The chart should show a distribution of `Avg_Daily_Usage_Hours`, use `fill='Gender'`, facet by academic level, and render a nonblank saved image.

