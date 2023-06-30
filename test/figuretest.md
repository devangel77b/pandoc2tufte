---
title: figure test
author: D Evangelista
date: \today
cref: true
---

# empty figure
<figure>
</figure>

<!-- can i make this? --> 
<figure class="figure">
</figure>

# plain figure
Check out [@fig:plain1].

<!-- default tufte-css form -->
<figure>
![caption can be kind of long actually](image.png){#fig:plain1}
</figure>

# fullwidth
Check out [@fig:fullwidth2]. [@Fig:fullwidth3] is also cool. 

<!-- default tufte-css form -->
<figure class="fullwidth">
![figure after (@darwin1852origin)](image.png){#fig:fullwidth2}
</figure>

<!-- can i make this? --> 
<figure class="figure*">
![caption caption $1+1=2$ **text like this**](image.png){#fig:fullwidth3}
</figure>

# marginfigure?
Refer to [@fig:plain1]--[-@fig:marginfigure4] We can also get this as a list of [@fig:plain1;@fig:fullwidth2;@fig:fullwidth3;@fig:marginfigure4]

<!-- can i make this? --> 
<figure class="marginfigure">
![caption](image.png){#fig:marginfigure4}
</figure>

