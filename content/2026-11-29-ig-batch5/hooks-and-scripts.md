# Batch 5 · Nov 29 (Sat after Thanksgiving) · scripts for review

Slot A 8:30 AM ET: papercraft "Grandma's garden" (already reviewed, see ../papercraft/).
Data as of Nov 28 02:14 UTC (judged at 18-24 h): janitor (Ronald Read P3) 212 views, skip 35.4%, avg 11.4 s (best). Thanksgiving advice POV 172, 37.8%, 13.5 s.
Grandma one question 131, 33.9%, 13.6 s. Uncle 141, 50%. Jay 40 TVs 125, 48.2%, 6.7 s (stalled). BF camping 85, 55%. Read P2 43, 67%. Sylvia Bloom 147 at 7 h, 40.7%.
Zero saves on every reel; comments near zero. Followers flat at 440.
Changes: (1) skip the Jay slot for a day (Jay niece 401k posts Nov 28 as the last Jay test), (2) give one reel a saveable payoff (a 3-item checklist on screen + "save this"), (3) keep real-person story in the 2:30 PM slot.

## R13 · 2:30 PM ET · real person · "Anne Scheiber"
Sources: Wikipedia "Anne Scheiber"; Time, "Death and the Maven" (1995); J. Weekly, "$22 million gift to Yeshiva U" (Dec 8 1995); Yeshiva University archive.
Facts used: IRS auditor; career stalled (her own letter to YU's president); about $5,000 savings when she retired/started investing in her early 50s; invested in stocks she understood and held long term; died 1995 at 101; left ~$22M to Yeshiva University for scholarships/loans for women.
Avoided: exact retirement year (sources say 1943 or 1944), salary, claims about skill (executor said these were exaggerated).
Lines: see /home/user/rb/r13/build/lines.json (copied below).

## R14 · 7:30 PM ET · POV + saveable checklist · "First paycheck, three questions"
Educational, no facts beyond the $10 minimum.

### r13
0 She retired with $5,000. She left $22 million.
1 Anne Scheiber audited taxes for the government.
2 Her career stalled for years. Her pay barely moved.
3 So in her fifties, she put her savings into companies she understood.
4 Then she mostly left them alone. For about fifty years.
5 She died at 101 and left it all for scholarships for women.
6 One story, not a promise. Markets fall. But she started with what she had.
7 We're building BLOK so anyone can own a fund of their own, from $10.
8 Who taught you to save? Tell me below.
9 Comment FUND and I'll send you the 7 questions private banks ask on day one.
### r14
0 POV: your little sister just got her first paycheck.
1 She asks where to put some of it.
2 You don't give her a tip. You give her three questions.
3 One. What's actually inside it?
4 Two. Who decides when it changes?
5 Three. Can I check it any day I want?
6 Save this for your first fund.
7 We're building BLOK so anyone can own a fund of their own, from $10.
8 Which one would you ask first? One, two or three? Tell me below.
9 Comment FUND and I'll send you the 7 questions private banks ask on day one.

## Gate receipts (Nov 28 02:40 UTC)
- R13 grounding BOUNCE: the $5,000 start is disputed (Wikipedia shows dividends by 1936; executor math implies ~$21k), "fifty years" too short, "left it all" unsupported. Fixes: hook now uses the supported salary fact ("never earned more than $4,000 a year"), L3 "by her forties", L4 "for decades", L5 "left it to scholarships for women". Linters 0 flags.
- R13 voice BOUNCE: L1-L2 stacked declaratives; L2 now "And she got stuck there. Years of it, and the pay barely moved."
- R14 grounding PASS. Voice BOUNCE: ambiguous "it" in L3; now "What's actually inside the fund?"
- Both pass after fixes. Caption must carry the Instagram disclaimer.

## Final lines
### r13
0 She never earned more than $4,000 a year. She left $22 million.
1 Anne Scheiber audited taxes for the government.
2 And she got stuck there. Years of it, and the pay barely moved.
3 By her forties, she owned pieces of companies she understood.
4 Then she mostly left them alone. For decades.
5 She died at 101 and left it to scholarships for women.
6 One story, not a promise. Markets fall. But she started with what she had.
7 We're building BLOK so anyone can own a fund of their own, from $10.
8 Who taught you to save? Tell me below.
9 Comment FUND and I'll send you the 7 questions private banks ask on day one.
### r14
0 POV: your little sister just got her first paycheck.
1 She asks where to put some of it.
2 You don't give her a tip. You give her three questions.
3 One. What's actually inside the fund?
4 Two. Who decides when it changes?
5 Three. Can I check it any day I want?
6 Save this for your first fund.
7 We're building BLOK so anyone can own a fund of their own, from $10.
8 Which one would you ask first? One, two or three? Tell me below.
9 Comment FUND and I'll send you the 7 questions private banks ask on day one.
- QA (Nov 28 03:00 UTC): R13 L3 re-generated (both takes said "company"; line now "pieces of several companies"). Remaining flag: ASR spells the name "Ansheiba" (proper noun, sounds right). R14 flag: "POV" heard as "P.O.B." (letters spoken, same as earlier POV reels). LUFS -15.5 / -15.3. Durations 44.3 s / 37.6 s.
