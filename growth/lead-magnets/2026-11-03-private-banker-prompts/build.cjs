const fs = require("fs");
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, WidthType, ShadingType,
  BorderStyle, AlignmentType, HeadingLevel, LevelFormat, PageBreak, ExternalHyperlink, ImageRun,
} = require("docx");

const INDIGO = "004EBA", LIME = "7ED116", LINEN = "F6F3E8", CORAL = "EC464D", EARTH = "844947", INK = "1D1B16", MUTED = "6B665A";
const W = 9360; // content width (Letter, 1" margins)

const t = (text, o = {}) => new TextRun({ text, ...o });
const p = (runs, o = {}) => new Paragraph({ children: Array.isArray(runs) ? runs : [t(runs)], spacing: { after: 140, line: 300 }, ...o });
const link = (text, url) => new ExternalHyperlink({ link: url, children: [t(text, { color: INDIGO, underline: {} })] });
const bullet = (runs) => new Paragraph({ children: Array.isArray(runs) ? runs : [t(runs)], numbering: { reference: "bul", level: 0 }, spacing: { after: 80, line: 290 } });
const kicker = (text, color = INDIGO) => p([t(text.toUpperCase(), { bold: true, color, size: 18, characterSpacing: 40 })], { spacing: { after: 60 } });
const none = { style: BorderStyle.NONE, size: 0, color: "FFFFFF" };

function box(children, { fill = LINEN, edge = INDIGO, dashed = false } = {}) {
  const side = dashed ? { style: BorderStyle.DASHED, size: 8, color: edge } : none;
  return new Table({
    width: { size: W, type: WidthType.DXA }, columnWidths: [W],
    rows: [new TableRow({ cantSplit: true, children: [new TableCell({
      width: { size: W, type: WidthType.DXA },
      shading: { fill, type: ShadingType.CLEAR, color: "auto" },
      margins: { top: 200, bottom: 120, left: 260, right: 260 },
      borders: { top: side, bottom: side, right: side, left: { style: dashed ? BorderStyle.DASHED : BorderStyle.SINGLE, size: dashed ? 8 : 36, color: edge } },
      children,
    })] })],
  });
}
const gap = () => new Paragraph({ children: [], spacing: { after: 160 } });

function prompt(n, title, why, lines, tip) {
  return [
    new Paragraph({ heading: HeadingLevel.HEADING_2, children: [t(`Prompt ${n}  `, { color: INDIGO }), t(title)] }),
    p([t(why, { italics: true, color: MUTED })], { keepNext: true }),
    box([
      p([t("COPY AND PASTE", { bold: true, size: 16, color: INDIGO, characterSpacing: 40 })], { spacing: { after: 80 } }),
      ...lines.map((l) => p([t(l, { size: 21 })], { spacing: { after: 100, line: 290 } })),
    ]),
    tip ? p([t("Tip: ", { bold: true, color: EARTH }), t(tip, { color: MUTED })], { spacing: { before: 100, after: 240 } }) : gap(),
  ];
}

const logo = fs.readFileSync("/home/user/Blok-Content/brand/assets/logo-wordmark.png");

const children = [
  new Paragraph({ children: [new ImageRun({ type: "png", data: logo, transformation: { width: 160, height: 31 } })], spacing: { after: 360 } }),
  kicker("Free guide · 20 minutes · ChatGPT, Claude or Gemini"),
  new Paragraph({ heading: HeadingLevel.TITLE, children: [t("The Private Banker Prompts")] }),
  p([t("The first meeting the top private banks give their richest clients, as 7 copy-paste prompts.", { size: 30, color: INDIGO })], { spacing: { after: 280 } }),

  box([
    p([t("Why this exists", { bold: true, size: 24 })]),
    p("The top private banks often want around $10 million in investable assets before they take you on as a client. Many others start at $1 million. Some private banks still in business today were founded in the 1600s, and for most of those 350 years, a sit-down with one was for the wealthy only."),
    p("The first meetings follow a script that hasn't changed much: get to know you, stress-test your nerves, X-ray what you own, map your cash, set the rules, and write them down in a one-page document called an Investment Policy Statement."),
    p([t("These 7 prompts walk you through the same script with an AI. You finish with your own Investment Policy Statement, the rulebook for your money. ", {}), t("For free.", { bold: true })], { spacing: { after: 60 } }),
  ], { fill: "EAF2FD", edge: INDIGO }),
  gap(),

  new Paragraph({ heading: HeadingLevel.HEADING_1, children: [t("How to use it")] }),
  bullet([t("Open a ", {}), t("new chat", { bold: true }), t(" in ChatGPT, Claude or Gemini. The free versions work.")]),
  bullet("Paste the prompts in order, in the same chat, so the AI remembers your answers."),
  bullet("Fill in anything in [square brackets] with your own details."),
  bullet([t("Use rough amounts. ", { bold: true }), t("Never paste account numbers, passwords or ID numbers.")]),
  bullet("The AI can be wrong, especially about what's inside a fund. Check anything important against the fund's latest factsheet."),
  new Paragraph({ children: [new PageBreak()] }),

  new Paragraph({ heading: HeadingLevel.HEADING_1, children: [t("The meeting, in 7 prompts")] }),

  ...prompt(1, "The first meeting", "A private banker's first job is to listen. This prompt makes the AI interview you properly, one question at a time.", [
    "Act as a private wealth adviser holding a first meeting with a new client. Interview me one question at a time, and wait for my answer before you ask the next one.",
    "Cover: what I'm investing for and when I'll need the money, how steady my income is, whether I have an emergency fund and how many months it covers, any debts and their interest rates, what I already invest in, and how I'd honestly feel if my investments fell 30% in a year.",
    "Keep it friendly and in plain English, no jargon. After 8 to 10 questions, give me a one-page summary: my goals, my time horizon, my comfort with risk, and the 3 biggest gaps a professional would point out. Don't recommend specific products.",
  ], "Answer honestly, not how you think a good investor should answer. The rest of the meeting is built on this."),

  ...prompt(2, "The stress test", "Everyone is brave in a rising market. Bankers check how you'll behave in a falling one, in dollars, not percentages.", [
    "Using what you know about me from this chat, run a stress test in plain dollars. Show roughly what my investments of $[amount] could look like in three cases: a very bad year like 2008, a flat decade for big US companies like 2000 to 2010, and a normal year.",
    "Use rough historical ranges and say clearly that these are illustrations, not predictions. Then ask me: in the bad case, would I sell, hold or add more? Explain what my answer says about the kind of mix I'd be comfortable living with.",
  ], "If the bad-case number makes your stomach drop, that's useful. It's the whole point of the exercise."),

  ...prompt(3, "The fund X-ray", "Owning five funds can still mean owning the same 10 companies five times. Analysts at private banks look inside.", [
    "Here are the funds and ETFs I own, with roughly how much is in each: [fund name or ticker: $amount, one per line].",
    "Acting as a private bank's portfolio analyst, X-ray them for me: 1) what I actually own when you look inside, roughly split by country, by sector and by type (stocks, bonds, cash); 2) where my funds overlap and hold the same companies; 3) the 10 companies I'm most exposed to across everything; 4) anything that looks concentrated or accidental.",
    "Tell me where your information might be out of date, and what I should check on each fund's latest factsheet.",
  ], "Fund holdings change. Treat this as a first look, then confirm on the factsheets."),

  ...prompt(4, "The money map", "Before any investing advice, a banker finds out how much you can really put away without stress.", [
    "Help me find my real investable amount. Ask me, one at a time, for my monthly take-home pay, my fixed costs, my flexible spending and my savings goals.",
    "Then show me a simple table: what's left each month, how big my emergency fund should be (3 to 6 months of costs), and a realistic monthly amount I could invest without stress.",
    "If the number is small, tell me honestly whether starting small is still worth it, and why.",
  ], "Spoiler: starting small is how almost everyone starts."),

  ...prompt(5, "The rebalancing rule", "Professionals don't decide when to rebalance in the moment. They set the rule in advance, while they're calm.", [
    "Help me set my rebalancing rule. Ask me for my target mix (for example 60% stocks, 30% bonds, 10% cash).",
    "Then explain in plain English the difference between rebalancing on a calendar (for example once a year) and rebalancing when a slice drifts past a band (for example 5 percentage points). Show a worked example with $1,000 where one slice grows and the mix drifts.",
    "Finish by writing my rule in one sentence I could stick on the fridge.",
  ]),

  ...prompt(6, "Write my Investment Policy Statement", "This is the document wealthy families keep: the written rules for their money. Now you get one.", [
    "Using everything from this chat, write my Investment Policy Statement. One page, plain English, first person, so it sounds like me. Use these sections:",
    "My goals and timeline · How much risk I'll take (in dollars, not just words) · My target mix and my rebalancing rule · What I will do when markets fall · How much I add, and when · What I will never do · When I'll review this document.",
    "End with 3 questions I should ask a licensed financial adviser before I act on it.",
  ], "Save it, print it, or pin it in your notes app. Read it the next time markets have a scary week."),

  ...prompt(7, "The hard questions", "The best bankers argue with you before the market does.", [
    "Now switch roles. You are a sceptical senior private banker reviewing my plan. Find the 5 weakest points in my Investment Policy Statement, ask me the hardest question about each one, and tell me what would have to be true for my plan to fail. Be direct but kind.",
  ]),

  p([t("Example (made up): ", { bold: true, color: EARTH }), t("what one section of an Investment Policy Statement can look like", { color: MUTED })], { spacing: { before: 120, after: 80 } }),
  box([
    p([t("What I will do when markets fall", { bold: true })], { spacing: { after: 60 } }),
    p([t("If my investments drop 20% or more, I will not sell. I'll reread this page, keep my $150 monthly top-up going, and only rebalance if a slice has drifted more than 5 points from my target. I'm investing for 2045, not for next month.", { italics: true })], { spacing: { after: 40 } }),
  ], { fill: "FFFFFF", edge: EARTH, dashed: true }),
  new Paragraph({ children: [new PageBreak()] }),

  kicker("Bonus 1", "4E8A0A"),
  new Paragraph({ heading: HeadingLevel.HEADING_1, children: [t("Keep a private banker in your pocket")] }),
  p("Turn the AI into a coach that remembers your rules. In Claude, create a Project and paste this into the project instructions. In ChatGPT, paste it into a custom GPT or into Settings, Personalization, Custom instructions. Then paste your Investment Policy Statement at the end."),
  box([
    p([t("COPY AND PASTE", { bold: true, size: 16, color: INDIGO, characterSpacing: 40 })], { spacing: { after: 80 } }),
    p([t("You are my personal investing coach, in the style of a private wealth adviser. My Investment Policy Statement is pasted below. Whenever I ask about a money decision, first check it against my rules and tell me whether it fits them.", { size: 21 })]),
    p([t("Speak plain English, give examples in US dollars, and always mention the risk. You are not a licensed adviser: never tell me to buy or sell a specific investment. Help me think it through, and list the questions I should ask a professional.", { size: 21 })]),
    p([t("When I type QUARTERLY REVIEW, walk me through: what changed in my life, whether my mix has drifted past my rebalancing band, and whether my rules still fit me.", { size: 21 })]),
    p([t("My Investment Policy Statement: [paste it here]", { size: 21, bold: true })]),
  ]),
  gap(),

  kicker("Bonus 2", "4E8A0A"),
  new Paragraph({ heading: HeadingLevel.HEADING_1, children: [t("From a rulebook to a fund of your own")] }),
  p("Your Investment Policy Statement is the rulebook. The next step is a fund that follows it. For centuries, running your own fund took a fortune, lawyers and a bank introduction. On-chain, a small fund can sit in an account only you control, with every holding visible any time, starting from $10."),
  p([t("If you're curious, join the BLOK waitlist at ", {}), link("blokc.app", "https://blokc.app"), t(". Sign in with Google, no forms. Start with an amount you'd be fine losing, and learn first.")]),
  gap(),

  box([
    p([t("The honest small print", { bold: true, color: EARTH })], { spacing: { after: 60 } }),
    p([t("This guide is educational only and is not financial or investment advice. An AI is not a licensed adviser and can make mistakes. Investing involves risk, including losing money. On-chain assets can be especially volatile. Private bank minimums vary by bank and country; the figures above are typical examples.", { size: 19, color: MUTED })], { spacing: { after: 40 } }),
  ], { fill: "FFFFFF", edge: EARTH, dashed: true }),
  gap(),
  p([t("Know someone who'd want their own private banker meeting? Send them this doc.", { bold: true })], { alignment: AlignmentType.CENTER }),
  p([t("Made by ", { color: MUTED }), link("@blok.capital", "https://www.instagram.com/blok.capital/"), t(" · one forgotten money story a day", { color: MUTED })], { alignment: AlignmentType.CENTER }),
];

const doc = new Document({
  creator: "BLOK Capital",
  title: "The Private Banker Prompts",
  styles: {
    default: { document: { run: { font: "Arial", size: 22, color: INK } } },
    paragraphStyles: [
      { id: "Title", name: "Title", basedOn: "Normal", next: "Normal", run: { font: "Georgia", size: 64, color: INK }, paragraph: { spacing: { before: 0, after: 120 }, keepNext: true } },
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true, run: { font: "Georgia", size: 40, color: INK }, paragraph: { spacing: { before: 240, after: 140 }, keepNext: true, outlineLevel: 0 } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true, run: { font: "Georgia", size: 30, color: INK }, paragraph: { spacing: { before: 280, after: 80 }, keepNext: true, outlineLevel: 1 } },
    ],
  },
  numbering: { config: [{ reference: "bul", levels: [{ level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 540, hanging: 300 } } } }] }] },
  sections: [{ properties: { page: { size: { width: 12240, height: 15840 }, margin: { top: 1296, bottom: 1296, left: 1440, right: 1440 } } }, children }],
});

Packer.toBuffer(doc).then((b) => { fs.writeFileSync(process.argv[2], b); console.log("ok"); });
