---
layout: default
nav_order: 4
---

# Known Limitations

* More than 10 token matches will result in no embed being sent, there is a TODO in the code to batch the sending when there are more than 10 token matches.
* Right now the only way to select jobs to query logs from is through the `job` label (as opposed to any other label).
