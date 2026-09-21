# SPY Quarterly Expiration Late-Close → Next-Open — Frozen Event Panel v1

Frozen: 2026-09-21
Status: **FROZEN BEFORE OUTCOME EXPOSURE**

## Primary test
On each quarterly options/futures expiration session, classify the sign of SPY's 3:30 PM ET → RTH-close move and compare it with the sign of SPY expiration close → next RTH open gap.

## Frozen event universe
- Instrument: SPY
- Coverage target: 2007-03 through 2026-09
- Calendar rule: quarterly March/June/September/December standard third-Friday expiration, adjusted only when the exchange holiday shifts the expiration session.
- Known holiday adjustments frozen here: 2008-03-21 Good Friday → 2008-03-20; 2026-06-19 Juneteenth → 2026-06-18.
- If intraday data are unavailable for a frozen event, report it as missing. Do not replace or omit it after seeing outcomes.
- Primary start time is 3:30 PM ET. 3:00 and 3:45 are robustness checks only.
- Primary outcome is expiration close → next RTH open sign. Next-session open→close and close→next-close are secondary diagnostics only.

## Frozen dates
1. 2007-03-16
2. 2007-06-15
3. 2007-09-21
4. 2007-12-21
5. 2008-03-20
6. 2008-06-20
7. 2008-09-19
8. 2008-12-19
9. 2009-03-20
10. 2009-06-19
11. 2009-09-18
12. 2009-12-18
13. 2010-03-19
14. 2010-06-18
15. 2010-09-17
16. 2010-12-17
17. 2011-03-18
18. 2011-06-17
19. 2011-09-16
20. 2011-12-16
21. 2012-03-16
22. 2012-06-15
23. 2012-09-21
24. 2012-12-21
25. 2013-03-15
26. 2013-06-21
27. 2013-09-20
28. 2013-12-20
29. 2014-03-21
30. 2014-06-20
31. 2014-09-19
32. 2014-12-19
33. 2015-03-20
34. 2015-06-19
35. 2015-09-18
36. 2015-12-18
37. 2016-03-18
38. 2016-06-17
39. 2016-09-16
40. 2016-12-16
41. 2017-03-17
42. 2017-06-16
43. 2017-09-15
44. 2017-12-15
45. 2018-03-16
46. 2018-06-15
47. 2018-09-21
48. 2018-12-21
49. 2019-03-15
50. 2019-06-21
51. 2019-09-20
52. 2019-12-20
53. 2020-03-20
54. 2020-06-19
55. 2020-09-18
56. 2020-12-18
57. 2021-03-19
58. 2021-06-18
59. 2021-09-17
60. 2021-12-17
61. 2022-03-18
62. 2022-06-17
63. 2022-09-16
64. 2022-12-16
65. 2023-03-17
66. 2023-06-16
67. 2023-09-15
68. 2023-12-15
69. 2024-03-15
70. 2024-06-21
71. 2024-09-20
72. 2024-12-20
73. 2025-03-21
74. 2025-06-20
75. 2025-09-19
76. 2025-12-19
77. 2026-03-20
78. 2026-06-18
79. 2026-09-18
