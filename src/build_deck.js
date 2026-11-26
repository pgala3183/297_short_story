// Builds slides/memory_for_llm_agents.pptx and video/narration_script.md.
// Run from the repo root:
//   NODE_PATH=src/node_modules node src/build_deck.js
// Speaker notes hold the narration; the video build reads them back from the .pptx.
const fs = require("fs");
const path = require("path");
const pptxgen = require("pptxgenjs");

const ROOT = path.resolve(__dirname, "..");
const FIG = (f) => path.join(ROOT, "figures", "slides", f);
const OUT_PPTX = path.join(ROOT, "slides", "memory_for_llm_agents.pptx");

const THEME = {
  name: "Agent Memory",
  headFontFace: "Segoe UI Semibold",
  bodyFontFace: "Segoe UI",
  colors: {
    dk1: "1D1A26", lt1: "FFFFFF", dk2: "2B1E3F", lt2: "F3F2EF",
    accent1: "2A78D6", accent2: "EB6834", accent3: "1BAF7A", accent4: "E8A33D",
    accent5: "6250D6", accent6: "E34948", hlink: "2A78D6", folHlink: "6250D6",
  },
};
const HEX = { ink: "1D1A26", ink2: "52514E", muted: "8A8985", grid: "E6E5E1", card: "F3F2EF", lav: "D9D2E6" };

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in
pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
pres.title = "Memory for LLM Agents";
pres.author = "Pratham Gala";
pres.subject = "CMPE 297 short story: survey of memory for LLM agents (2026)";
const C = pres.SchemeColor;

// ------------------------------------------------------------------ layouts
pres.defineSlideMaster({
  title: "TITLE_DARK",
  background: { color: THEME.colors.dk2 },
  objects: [
    { placeholder: { options: { name: "title", type: "title", x: 0.8, y: 1.6, w: 6.5, h: 2.3, fontSize: 48, bold: true, color: C.background1, fontFace: THEME.headFontFace, align: "left", valign: "bottom", margin: 0 }, text: "" } },
    { placeholder: { options: { name: "body", type: "body", x: 0.8, y: 4.1, w: 6.5, h: 1.4, fontSize: 20, color: C.background2, valign: "top", margin: 0 }, text: "" } },
    { text: { text: "CMPE 297 short story  ·  Pratham Gala  ·  November 2026", options: { x: 0.8, y: 6.5, w: 6.5, h: 0.4, fontSize: 13, color: C.accent4, margin: 0 } } },
  ],
});
pres.defineSlideMaster({
  title: "CONTENT",
  background: { color: THEME.colors.lt1 },
  margin: [0.4, 0.6, 0.6, 0.6],
  objects: [
    { placeholder: { options: { name: "title", type: "title", x: 0.6, y: 0.35, w: 12.13, h: 0.8, fontSize: 30, bold: true, color: C.text1, fontFace: THEME.headFontFace, align: "left", valign: "middle", margin: 0 }, text: "" } },
    { text: { text: "Memory for LLM Agents  ·  Pratham Gala", options: { x: 0.6, y: 7.0, w: 8, h: 0.3, fontSize: 10, color: C.text2, margin: 0 } } },
  ],
  slideNumber: { x: 12.23, y: 7.0, w: 0.5, h: 0.3, fontSize: 10, color: C.text2, align: "right" },
});

// ------------------------------------------------------------------ helpers
function pngSize(file) {
  const b = fs.readFileSync(file);
  return { w: b.readUInt32BE(16), h: b.readUInt32BE(20) };
}
function addFigure(slide, file, box = { x: 0.6, y: 1.25, w: 12.13, h: 5.3 }, alt = "") {
  const { w, h } = pngSize(file);
  const scale = Math.min(box.w / w, box.h / h);
  const iw = w * scale, ih = h * scale;
  slide.addImage({ path: file, x: box.x + (box.w - iw) / 2, y: box.y + (box.h - ih) / 2, w: iw, h: ih, altText: alt, objectName: "figure" });
}
function caption(slide, text, y = 6.6) {
  slide.addText(text, { x: 0.6, y, w: 12.13, h: 0.32, fontSize: 11, color: C.text2, italic: true, margin: 0, isTextBox: true, objectName: "source caption" });
}
function card(slide, x, y, w, h, fill = HEX.card) {
  slide.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, fill: { color: fill }, line: { color: fill, width: 0 }, rectRadius: 0.08, objectName: "card" });
}
function badge(slide, x, y, label, color, d = 0.46) {
  slide.addShape(pres.shapes.OVAL, { x, y, w: d, h: d, fill: { color }, line: { color, width: 0 }, objectName: "badge" });
  slide.addText(label, { x, y, w: d, h: d, fontSize: 14, bold: true, color: C.background1, align: "center", valign: "middle", margin: 0, isTextBox: true });
}
const chartText = {
  catAxisLabelColor: HEX.ink2, valAxisLabelColor: HEX.ink2,
  catAxisLabelFontFace: "+mn-lt", valAxisLabelFontFace: "+mn-lt",
  catAxisLabelFontSize: 12, valAxisLabelFontSize: 11,
  valGridLine: { color: HEX.grid, size: 0.75 }, catGridLine: { style: "none" },
  catAxisLineShow: false, valAxisLineShow: false,
  dataLabelFontFace: "+mn-lt", dataLabelFontSize: 12, dataLabelColor: HEX.ink,
  legendFontFace: "+mn-lt", legendFontSize: 12, legendColor: HEX.ink2,
  titleFontFace: "+mn-lt", titleFontSize: 14, titleColor: HEX.ink,
};
const chartOpts = (extra) => Object.assign({}, chartText, { valGridLine: { color: HEX.grid, size: 0.75 }, catGridLine: { style: "none" } }, extra);
function bullets(slide, items, box, fontSize = 16) {
  slide.addText(items.map((t, i) => ({ text: t, options: { bullet: true, breakLine: i < items.length - 1, paraSpaceAfter: 8 } })),
    Object.assign({ fontSize, color: C.text1, valign: "top", margin: 0, isTextBox: true, objectName: "commentary" }, box));
}

const narration = [];
let section = "";
function newSlide(master, title, notes, sectionTitle) {
  if (sectionTitle && sectionTitle !== section) { pres.addSection({ title: sectionTitle }); section = sectionTitle; }
  const s = pres.addSlide({ masterName: master, sectionTitle: section });
  if (title) s.addText(title, { placeholder: "title" });
  s.addNotes(notes);
  narration.push({ title: title || "", notes });
  return s;
}

// ------------------------------------------------------------------ 1 title
{
  const s = newSlide("TITLE_DARK", "Memory for\nLLM Agents",
    "Hi, I'm Pratham Gala, and this is my CMPE 297 short story on memory for LLM agents. Over the next fifteen minutes or so, I'll walk through five survey papers from 2026 and two new benchmark papers. I'll explain the main taxonomy, look at the techniques that top the leaderboards, and finish with my own opinions on where this field is heading.",
    "Introduction");
  s.addText("What five 2026 surveys say about how agents remember, and where the benchmarks disagree", { placeholder: "body" });
  s.addImage({ path: FIG("title_art.png"), x: 7.6, y: 0, w: 5.733, h: 7.5, altText: "constellation of memory nodes", objectName: "cover art" });
}

// ------------------------------------------------------------------ 2 why now
{
  const s = newSlide("CONTENT", "A bigger context window is a desk, not a memory",
    "Let me start with why this matters. Agents forget what you told them last week. Or worse, they remember it and ignore it. The tempting fix is a bigger context window, but a long window is a desk, not a memory. The LongMemEval benchmark showed that GPT-4o lost thirty percent of its accuracy when it got a user's full chat history instead of only the relevant sessions, even though the answers were right there in the prompt. Meanwhile, one survey coded 435 papers and found that sixty-two percent work on retrieval, but only six percent on rollback. The field is very good at remembering and much weaker at governing and undoing memory. That imbalance runs through this whole talk.");
  const stats = [
    ["30%", "relative accuracy drop for GPT-4o when it reads a full 115k-token history instead of only the relevant sessions", "LongMemEval"],
    ["62% vs 6%", "of 435 memory papers address retrieval vs. rollback", "Always-On Agents survey"],
    ["0.93 vs 0.65", "LoCoMo score of a per-question oracle choosing the memory design vs. the best single design", "Harness the Memory"],
  ];
  stats.forEach(([big, label, src], i) => {
    const x = 0.6 + i * 4.11;
    card(s, x, 1.65, 3.85, 4.4);
    s.addText(big, { x: x + 0.3, y: 1.95, w: 3.3, h: 1.3, fontSize: 48, bold: true, color: [C.accent1, C.accent2, C.accent5][i], fontFace: THEME.headFontFace, margin: 0, isTextBox: true });
    s.addText(label, { x: x + 0.3, y: 3.35, w: 3.3, h: 1.9, fontSize: 16, color: C.text1, valign: "top", margin: 0, isTextBox: true });
    s.addText(src, { x: x + 0.3, y: 5.45, w: 3.3, h: 0.4, fontSize: 12, color: C.text2, italic: true, margin: 0, isTextBox: true });
  });
}

// ------------------------------------------------------------------ 3 reading list
{
  const s = newSlide("CONTENT", "The reading list: seven papers, April to November 2026",
    "Here is my reading list. The main paper is Memory-Centric Continual Learning for AI Agents, posted in October by a 28-author team from Harbin Institute of Technology Shenzhen, Tsinghua, Huawei and China Telecom. Around it are four more surveys. Always-On Agents, from June, focuses on governance. Memory for Large Language Models, from Tsinghua, NUS and Bosch, looks inside the model. From Storage to Experience is an ACL 2026 Findings paper. And a security survey from MemTensor is an EMNLP 2026 paper that was revised through November. For the leaderboard I added two independent evaluation papers, Harness the Memory and MERIT, shown in orange.");
  addFigure(s, FIG("fig01_reading_list_timeline.png"), { x: 0.6, y: 1.4, w: 12.13, h: 5.0 }, "timeline of the seven papers");
  caption(s, "Dates are first arXiv submission. Blue = survey, orange = evaluation paper used for the leaderboard.");
}

// ------------------------------------------------------------------ 4 three layers
{
  const s = newSlide("CONTENT", "Three layers of memory, and one question across them",
    "These papers don't compete. They describe different layers of one stack. At the bottom is the model layer: how the network itself carries state, through KV caches, recurrent states, or weights updated at test time. In the middle is the agent layer: what is worth writing down, how it's organized, and when it comes back. On top is the governance layer: who may write, read, share or delete a memory, and whether a bad one can be rolled back. Evaluation cuts across all three. Does memory change what the agent does, and what does it cost?");
  addFigure(s, FIG("fig02_three_layers.png"), undefined, "three layers diagram");
}

// ------------------------------------------------------------------ 5 main paper thesis
{
  const s = newSlide("CONTENT", "Main paper: judge memory by what it changes",
    "The main paper makes one provocative claim. Memory should be judged by whether it improves future actions, not by what it can retrieve. By that standard, most current systems are passive caches that happen to be good at quiz questions. The paper makes three contributions. First, a three-axis taxonomy with a lifecycle model. Second, an evaluation protocol for retention, adaptation and transfer, run against matched baselines, so that memory helped can't secretly mean we gave the model more tokens. Third, a scaling framework for how performance grows with experience, storage and compute.",
    "Taxonomy");
  card(s, 0.6, 1.4, 12.13, 1.35, "EFE9F7");
  s.addText([
    { text: "“A memory write counts as learning only if it is read later and changes behavior.”", options: { fontSize: 22, color: C.text1, italic: true, breakLine: true } },
    { text: "Memory-Centric Continual Learning for AI Agents · Li et al. · arXiv 2610.29357 · Oct 2026 (my paraphrase)", options: { fontSize: 12, color: C.text2 } },
  ], { x: 0.9, y: 1.5, w: 11.6, h: 1.15, valign: "middle", margin: 0, isTextBox: true, objectName: "thesis" });
  const items = [
    ["1", "Taxonomy + lifecycle", "WHERE memory lives, WHAT it holds, HOW it is managed; two coupled loops of memory state and policy", C.accent1],
    ["2", "Evaluation protocol", "Retention under interference, adaptation to change, transfer; always against no-memory, full-history, RAG and equal-compute baselines", C.accent3],
    ["3", "Memory scaling", "How performance grows with experience, storage and compute, for both external and parametric memory", C.accent2],
  ];
  items.forEach(([n, head, body, color], i) => {
    const x = 0.6 + i * 4.11;
    card(s, x, 3.05, 3.85, 3.3);
    badge(s, x + 0.3, 3.35, n, color);
    s.addText(head, { x: x + 0.95, y: 3.33, w: 2.75, h: 0.5, fontSize: 19, bold: true, color: C.text1, valign: "middle", margin: 0, isTextBox: true });
    s.addText(body, { x: x + 0.3, y: 4.05, w: 3.3, h: 2.1, fontSize: 15, color: C.text1, valign: "top", margin: 0, isTextBox: true });
  });
}

// ------------------------------------------------------------------ 6 WHERE WHAT HOW
{
  const s = newSlide("CONTENT", "Taxonomy: WHERE it lives, WHAT it holds, HOW it is run",
    "Here is the taxonomy. WHERE is the substrate. Contextual memory is tokens in the live prompt: instant, but gone when the session ends. Activation memory is KV caches and recurrent states. External memory is logs, vector stores and graphs, like MemGPT, Mem0 or A-MEM. You can edit and delete it, but items can quietly stop being retrieved, which the authors call functional forgetting. Parametric memory is weights and adapters: cheap to read, expensive and risky to write. WHAT is the asset: episodic memories of what happened, semantic facts, and procedural know-how like workflows and skills. HOW is the policy: fixed rules like top-k, deliberative policies where the LLM decides, or controllers learned from outcomes. The axes are independent. Mem0 is external, semantic and deliberative. Memory-R1 swaps in a learned policy.");
  addFigure(s, FIG("fig03_where_what_how.png"), { x: 0.6, y: 1.3, w: 12.13, h: 5.3 }, "WHERE WHAT HOW taxonomy");
  caption(s, "Redrawn from Memory-Centric Continual Learning (arXiv 2610.29357) with example systems.", 6.65);
}

// ------------------------------------------------------------------ 7 two loops
{
  const s = newSlide("CONTENT", "Memory is two coupled loops, not a pipeline",
    "The paper also argues that memory isn't a pipeline but two coupled loops. The inner loop is the memory state. First, writing. The authors call admission the plasticity boundary, because whatever passes it can change future behavior. Second, consolidation, where episodes become rules. The danger here is context collapse: compression strips out when, who and under what conditions, and leaves a confident but wrong rule. Third, retrieval and use. Fourth, revision and forgetting, where marking a fact as outdated is different from deleting things to save space. The outer loop is policy evolution: task feedback updates the rules of the inner loop. Almost no deployed system runs that outer loop online today.");
  addFigure(s, FIG("fig04_two_loops.png"), undefined, "two coupled loops");
  caption(s, "Five lifecycle stages from Memory-Centric Continual Learning (arXiv 2610.29357); layout is mine.");
}

// ------------------------------------------------------------------ 8 storage reflection experience
{
  const s = newSlide("CONTENT", "Storage → Reflection → Experience",
    "A second survey, From Storage to Experience, tells the same story as a progression. Storage keeps raw trajectories, in windows, vector stores, or tables and graphs. Reflection refines a single trajectory, the way Reflexion critiques itself or Mem0 maintains its facts. Experience abstracts across many trajectories into rules and skills that transfer to new tasks. The stages stack rather than replace each other. The authors admit they can't rank the stages with numbers, because each one optimizes a different goal. That's an early hint of the evaluation problem we'll see later.");
  addFigure(s, FIG("fig05_storage_reflection_experience.png"), undefined, "three stage evolution");
  caption(s, "Redrawn from From Storage to Experience (arXiv 2605.06716, ACL 2026 Findings).");
}

// ------------------------------------------------------------------ 9 model level
{
  const s = newSlide("CONTENT", "Inside the model: implicit state vs. addressable memory",
    "The Tsinghua, NUS and Bosch survey goes inside the model. Implicit memory, in blue, is a by-product of computation: the KV cache, and state-space models like Mamba-3, RWKV-7 and Gated DeltaNet. Explicit memory, in orange, has its own addressable component: kNN-LM's datastore, mixture-of-experts layers, and test-time learners like Titans, which update a memory module during inference based on how surprising the input is. One fun detail: the offline, short-term corner is empty. Their conclusion is that hybrid designs will become the norm, which is exactly what the agent-level surveys conclude too.");
  addFigure(s, FIG("fig06_model_level_memory.png"), undefined, "model level memory map");
  caption(s, "Representation × update dynamics × persistence. Memory for Large Language Models (arXiv 2607.25380), Table I.");
}

// ------------------------------------------------------------------ 10 architectures
{
  const s = newSlide("CONTENT", "Three architectures behind most leaderboard rows",
    "Here are the three architectures behind most leaderboard rows. MemGPT, now Letta, treats the context window like RAM, and pages data to a recall store and an archival vector store with function calls. Mem0 extracts facts from each exchange, compares each one with the most similar stored memories, and picks add, update, delete, or do nothing. That reconcile step targets the most common real problem: facts that change. Zep is a temporal knowledge graph. It keeps raw episodes, an entity graph where facts are edges, and community summaries. Every fact carries two clocks: when it was true, and when the system learned it.",
    "Techniques");
  addFigure(s, FIG("fig19_three_architectures.png"), undefined, "MemGPT Mem0 Zep architectures");
  caption(s, "Simplified from the MemGPT (2023), Mem0 (2025) and Zep (2025) papers.");
}

// ------------------------------------------------------------------ 11 experience techniques
{
  const s = newSlide("CONTENT", "Experience memory: storing lessons instead of facts",
    "The other family in every survey is experience memory, where the agent stores lessons instead of facts. Reflexion writes a verbal post-mortem after a failed attempt. ExpeL compares successes and failures to extract general insights. Agent Workflow Memory induces reusable workflows, with reported gains of about twenty-five percent on Mind2Web and fifty-one percent on WebArena. ReasoningBank distills strategies from both successes and failures. Voyager stores executable code skills. And learned controllers like Memory-R1 use reinforcement learning to decide what to store, instead of prompting the model to guess.");
  const t = [
    ["Reflexion", "verbal post-mortem after each failed attempt, reread on the next try", "episodic · deliberative", C.accent1],
    ["ExpeL", "compares successes with failures to extract general insights", "episodic → semantic", C.accent1],
    ["Agent Workflow Memory", "induces reusable workflows; +24.6% Mind2Web, +51.1% WebArena (reported)", "procedural", C.accent3],
    ["ReasoningBank", "distills reasoning strategies from successes and failures; best ALFWorld gain in Harness", "procedural", C.accent3],
    ["Voyager", "library of executable code skills; 3.3× more items, milestones up to 15.3× faster", "procedural · external", C.accent2],
    ["Memory-R1 · MEM1", "reinforcement learning decides what to store or how to compress state", "learned policy", C.accent5],
  ];
  t.forEach(([name, body, tag, color], i) => {
    const col = i % 3, row = Math.floor(i / 3);
    const x = 0.6 + col * 4.11, y = 1.45 + row * 2.6;
    card(s, x, y, 3.85, 2.35);
    s.addShape(pres.shapes.OVAL, { x: x + 0.3, y: y + 0.33, w: 0.22, h: 0.22, fill: { color }, line: { color, width: 0 } });
    s.addText(name, { x: x + 0.65, y: y + 0.2, w: 3.0, h: 0.48, fontSize: 18, bold: true, color: C.text1, valign: "middle", margin: 0, isTextBox: true });
    s.addText(body, { x: x + 0.3, y: y + 0.78, w: 3.3, h: 1.05, fontSize: 14, color: C.text1, valign: "top", margin: 0, isTextBox: true });
    s.addText(tag, { x: x + 0.3, y: y + 1.85, w: 3.3, h: 0.32, fontSize: 12, color: C.text2, italic: true, margin: 0, isTextBox: true });
  });
}

// ------------------------------------------------------------------ 12 LoCoMo
{
  const s = newSlide("CONTENT", "LoCoMo: full context wins accuracy, memory wins latency",
    "Now the leaderboard. LoCoMo is the benchmark everyone reports: long conversations of about 26 thousand tokens, followed by questions. This chart plots the Mem0 paper's results: a judge score against p95 latency on a log scale. The headline is that Mem0 matches or beats the other memory systems while answering in about one and a half seconds, versus seventeen for full context, with ninety-three percent fewer tokens. But look at the top right. Full context still scores highest, 72.9 against 66.9. A 26 thousand token conversation fits in any modern window, so on LoCoMo memory is a cost optimization, not an accuracy win. Also, these baselines were run by Mem0's own authors.",
    "Leaderboard");
  addFigure(s, FIG("fig07_locomo_accuracy_vs_latency.png"), undefined, "LoCoMo scatter");
  caption(s, "Mem0 paper, Table 2 (arXiv 2504.19413). 10 conversations, GPT-4o-mini, mean of 10 runs. Baselines run by the Mem0 authors.");
}

// ------------------------------------------------------------------ 13 LongMemEval (native chart)
{
  const s = newSlide("CONTENT", "LongMemEval: a temporal graph beats a 115k-token prompt",
    "LongMemEval is harder: 500 questions over histories of about 115 thousand tokens, testing extraction, multi-session reasoning, temporal reasoning, knowledge updates, and knowing when not to answer. Here the picture flips. With GPT-4o, Zep's temporal graph scored 71.2 percent against 60.2 for the full history in the prompt. It cut latency by about ninety percent and read about 1,600 tokens instead of 115 thousand. The LongMemEval authors also ran useful ablations. Indexing each memory under extra fact-based keys raised recall by about nine percent, and adding time ranges to time-sensitive queries improved temporal recall by seven to eleven percent.");
  s.addChart(pres.charts.BAR, [
    { name: "Full context (115k tokens)", labels: ["gpt-4o-mini", "gpt-4o"], values: [55.4, 60.2] },
    { name: "Zep (~1.6k tokens)", labels: ["gpt-4o-mini", "gpt-4o"], values: [63.8, 71.2] },
  ], chartOpts({
    x: 0.6, y: 1.35, w: 7.0, h: 5.15, barDir: "col", barGrouping: "clustered", barGapWidthPct: 60,
    chartColors: [THEME.colors.accent2, THEME.colors.accent1],
    showValue: true, dataLabelPosition: "outEnd", dataLabelFormatCode: "0.0",
    valAxisMinVal: 0, valAxisMaxVal: 80, valAxisMajorUnit: 20,
    showLegend: true, legendPos: "t",
    showTitle: true, title: "Accuracy on LongMemEval_S (%)", objectName: "LongMemEval accuracy chart",
  }));
  bullets(s, [
    "Latency: 28.9 s → 2.6 s with GPT-4o (about 90% lower)",
    "Biggest gains: temporal reasoning and user preferences",
    "Worse on recalling what the assistant itself said (94.6 → 80.4)",
    "LongMemEval ablation: fact-augmented keys gave +9.4% recall@k",
    "Time-aware query expansion: +7–11% temporal recall",
  ], { x: 8.0, y: 1.6, w: 4.73, h: 4.6 }, 16);
  caption(s, "Zep paper, Table 2 (arXiv 2501.13956); LongMemEval (arXiv 2410.10813, ICLR 2025).");
}

// ------------------------------------------------------------------ 14 Harness heatmap
{
  const s = newSlide("CONTENT", "Independent test: no memory substrate wins every column",
    "Vendor tables compare whole products, so I wanted an independent view. Harness the Memory holds everything fixed except the memory substrate: same model, same prompts, same harness. It tests eleven designs. No substrate wins every column. A LightRAG-style graph wins LoCoMo and LongMemEval. A gist index wins long-range and test-time learning. Conflict resolution is bad for everyone, with a best score of 0.32. Full context collapses on LongMemEval because the history no longer fits. Memory stored in LoRA weights is the weakest almost everywhere. And the winning graph is about thirty-six times slower per query than a plain vector index.");
  addFigure(s, FIG("fig09_harness_substrate_heatmap.png"), undefined, "substrate heatmap");
  caption(s, "LLM-judge score, Qwen3-32B backbone, boxed = best in column. Harness the Memory, Table 1 (arXiv 2608.15008v2).");
}

// ------------------------------------------------------------------ 15 Harness agents
{
  const s = newSlide("CONTENT", "For agents that act, more memory is not automatically better",
    "The most interesting part is what happens when the agent has to act. On ALFWorld, an embodied task suite, distilled strategies in the style of ReasoningBank gave the biggest boost, almost ten points. On coding, almost everything hurt except simple lexical retrieval. They also varied how many memories get retrieved. On LoCoMo, retrieving more always helped. On ALFWorld it hurt, and plain vector and BM25 indexes eventually fell below the no-memory baseline. An attention probe suggests why: retrieved text pulls attention away from the current observation and the list of valid actions.");
  addFigure(s, FIG("fig10_harness_agent_tasks.png"), undefined, "agent task gains");
  caption(s, "Gain over a no-memory agent, Qwen3-32B. Harness the Memory, Table 2 (arXiv 2608.15008v2).");
}

// ------------------------------------------------------------------ 16 MERIT (native)
{
  const s = newSlide("CONTENT", "When facts change, update-on-write beats similarity search",
    "MERIT asks the question I care about most as a builder. When a fact changes halfway through a series of tool-using tasks, does the agent use the new value? With no memory it never succeeds. Full replay of past transcripts works, but it's expensive. Embedding retrieval is the weak spot. It returns the stale and the fresh value side by side, with no sense of recency, and success drops as low as 0.35. Fact stores that update on write, and LLM summaries, stay between 0.7 and 1.0. Two more findings stuck with me. Agents ignored the correct retrieved value 45 percent of the time. And swapping the fact extractor moved one domain by up to 60 points.");
  const cats = ["Full replay", "Embedding retrieval", "LLM summary", "Fact store", "Hybrid"];
  s.addChart(pres.charts.BAR, [
    { name: "Customer support", labels: cats, values: [1.0, 0.7, 1.0, 0.95, 0.8] },
    { name: "IT operations", labels: cats, values: [0.95, 0.35, 0.7, 0.75, 0.6] },
    { name: "Personal assistant", labels: cats, values: [1.0, 0.45, 1.0, 1.0, 0.5] },
  ], chartOpts({
    x: 0.6, y: 1.35, w: 8.2, h: 5.15, barDir: "col", barGrouping: "clustered", barGapWidthPct: 70,
    chartColors: [THEME.colors.accent1, THEME.colors.accent2, THEME.colors.accent3],
    valAxisMinVal: 0, valAxisMaxVal: 1, valAxisMajorUnit: 0.2, valAxisLabelFormatCode: "0.0",
    showLegend: true, legendPos: "t",
    showTitle: true, title: "Task success when a fact changed mid-arc (no memory = 0.00)", objectName: "MERIT chart",
  }));
  bullets(s, [
    "Retrieval shows stale and fresh values side by side",
    "Agent ignored the fresh value in 25 of 55 probes (45%)",
    "Changing the extractor moved one domain by up to 60 points",
    "Full replay works but is never the cheapest per success",
  ], { x: 9.15, y: 1.7, w: 3.58, h: 4.6 }, 16);
  caption(s, "MERIT hard tier, gpt-4.1-mini agent (arXiv 2609.05441).");
}

// ------------------------------------------------------------------ 17 ablations (native line)
{
  const s = newSlide("CONTENT", "Ablation: memory that helps early can hurt later",
    "The main paper ran two small but important ablations with Mem0. First, how the agent reads memory matters. Searching and summarizing saves tokens but costs accuracy, and raising the read budget from 512 to 2,048 tokens moved LongMemEval accuracy from 35 to 44 percent. Second, and this is the plot I most want people to see, they compared an agent that keeps its memory with the same agent reset to empty. After 64 dialogues, memory helped by seven points. After 128 it hurt by about ten, and after 256 by about fourteen. Consolidation shrank the store but didn't fix it. Leaderboards measure one moment. Deployment is a trajectory.",
    "Evaluation");
  s.addChart(pres.charts.LINE, [
    { name: "One task ordering", labels: ["64 dialogues", "128", "256"], values: [7.1, -10.43, -13.93] },
    { name: "Pooled over 3 orderings", labels: ["64 dialogues", "128", "256"], values: [3.18, -10.38, -11.6] },
  ], chartOpts({
    x: 0.6, y: 1.35, w: 7.4, h: 5.15,
    chartColors: [THEME.colors.accent1, THEME.colors.accent5], lineSize: 2, lineDataSymbol: "circle", lineDataSymbolSize: 9,
    valAxisMinVal: -16, valAxisMaxVal: 10, valAxisMajorUnit: 4,
    showLegend: true, legendPos: "t",
    showTitle: true, title: "Stateful minus reset score (points)", objectName: "stateful minus reset chart",
  }));
  card(s, 8.35, 1.45, 4.38, 2.35);
  s.addText([
    { text: "Reader policy over the same Mem0 bank", options: { bold: true, breakLine: true } },
    { text: "Read all: F1 4.63 · 730 tokens", options: { breakLine: true } },
    { text: "Search: F1 4.29 · 226 tokens", options: { breakLine: true } },
    { text: "Search + summarize: F1 3.91 · 44 tokens", options: {} },
  ], { x: 8.6, y: 1.6, w: 3.95, h: 2.05, fontSize: 15, color: C.text1, valign: "top", margin: 0, paraSpaceAfter: 6, isTextBox: true });
  card(s, 8.35, 4.05, 4.38, 2.35);
  s.addText([
    { text: "Read budget 512 → 2,048 tokens", options: { bold: true, breakLine: true } },
    { text: "LongMemEval accuracy 35% → 44%", options: { breakLine: true } },
    { text: "Consolidation cut the store from ~3,900 to ~1,800 tokens; the gain stayed negative", options: {} },
  ], { x: 8.6, y: 4.2, w: 3.95, h: 2.05, fontSize: 15, color: C.text1, valign: "top", margin: 0, paraSpaceAfter: 6, isTextBox: true });
  caption(s, "Memory-Centric Continual Learning, Sec. 4.3 and Table 4 (arXiv 2610.29357). Mem0 at an 8,192-token cap, Qwen3-30B.");
}

// ------------------------------------------------------------------ 18 four gates
{
  const s = newSlide("CONTENT", "Why recall scores mislead: memory must pass four gates",
    "So how should we measure memory? The main paper proposes a four-gate cascade, and I've attached evidence from the other papers to each gate. Preservation: was it stored correctly? That's MERIT's extractor result. Access: can it be found at the right moment? That's LongMemEval's key expansion. Utilization: does the agent actually use it? That's the 45 percent ignore rate. Effect: does behavior beat no memory, now and later? That's the stateful-minus-reset curve. The overall benefit is capped by the leakiest gate, and recall benchmarks mostly test the first two.");
  addFigure(s, FIG("fig18_four_gate_cascade.png"), undefined, "four gate cascade");
  caption(s, "Cascade from Memory-Centric Continual Learning (arXiv 2610.29357); evidence from MERIT, LongMemEval and the MCCL experiments.");
}

// ------------------------------------------------------------------ 19 Always-On corpus (native)
{
  const s = newSlide("CONTENT", "The field is great at remembering, poor at un-remembering",
    "Now the governance layer. Always-On Agents treats a long-running agent as a persistent-state system, whose state includes permissions, commitments and audit logs, not just memories. The authors coded 435 papers by lifecycle stage. Accumulating and using memory is well covered: retrieval alone shows up in 62 percent of works. Governing and recovering is thin: forgetting is fifteen percent, rollback six. None of the coded works reports how well recovery actually works. The authors say each memory record should carry six properties: authority, scope, mutability, provenance, recoverability and actionability.",
    "Governance");
  const stages = ["Observe", "Write", "Validate", "Organize", "Retrieve", "Act", "Update", "Forget", "Audit", "Rollback"];
  const counts = [68, 200, 87, 128, 269, 141, 127, 66, 88, 27];
  const labels = stages.map((st, i) => `${st} (${counts[i]})`);
  s.addChart(pres.charts.BAR, [
    { name: "Forward arc: accumulate and use", labels, values: counts.map((v, i) => (i < 6 ? v : 0)) },
    { name: "Return arc: govern and recover", labels, values: counts.map((v, i) => (i >= 6 ? v : 0)) },
  ], chartOpts({
    x: 0.6, y: 1.35, w: 8.0, h: 5.15, barDir: "bar", barGrouping: "stacked", barGapWidthPct: 45,
    chartColors: [THEME.colors.accent1, THEME.colors.accent2], catAxisOrientation: "maxMin",
    valAxisMinVal: 0, valAxisMaxVal: 300, valAxisMajorUnit: 50,
    showLegend: true, legendPos: "t",
    showTitle: true, title: "Works addressing each lifecycle stage (of 435)", objectName: "corpus lifecycle chart",
  }));
  bullets(s, [
    "Retrieve: 62% of works",
    "Forget: 15% · Rollback: 6%",
    "Rollback was 0% before 2025",
    "No coded work measures recovery success or cost",
    "Six axes per memory record: authority, scope, mutability, provenance, recoverability, actionability",
  ], { x: 9.0, y: 1.7, w: 3.73, h: 4.7 }, 16);
  caption(s, "Always-On Agents survey (arXiv 2606.30306). Multi-label coding of a 435-work corpus.");
}

// ------------------------------------------------------------------ 20 AOEP (native)
{
  const s = newSlide("CONTENT", "A governance scorecard, not an accuracy leaderboard",
    "They then built a small evaluation contract called AOEP. It scores obligations, not answer quality: restarts, revoked permissions, deletion requests and poisoned tool output. A governed reference design met all fifteen obligations. Raw storage met seven. The fact-extracting systems met only three or four, and in two episodes they leaked a deleted billing address and an attacker-planted address. The authors say clearly this is a small pilot, not a product verdict. My favorite detail is the no-memory row. It passes every must-not check by storing nothing, and fails every obligation. Safety and usefulness have to be measured together.");
  const sys = ["Governed reducer (reference)", "Naive append", "Full context", "Vector RAG", "Mem0-style reimplementation", "Mem0 package (local)", "No memory"];
  s.addChart(pres.charts.BAR, [{ name: "Obligations met (of 15)", labels: sys, values: [15, 7, 7, 7, 4, 3, 0] }], chartOpts({
    x: 0.6, y: 1.35, w: 8.0, h: 5.15, barDir: "bar", barGapWidthPct: 55,
    chartColors: [THEME.colors.accent1], catAxisOrientation: "maxMin",
    valAxisMinVal: 0, valAxisMaxVal: 15, valAxisMajorUnit: 5,
    showValue: true, dataLabelPosition: "outEnd", showLegend: false,
    showTitle: true, title: "AOEP-v0 obligations met (of 15)", objectName: "AOEP chart",
  }));
  bullets(s, [
    "Fault patterns: restart, permission drift, deletion, cross-user scope, poisoned tool output",
    "Fact-extracting stores leaked a deleted address and an attacker's address",
    "No memory: 41 of 41 'must not' checks passed, 0 of 15 obligations met",
    "Pilot, not a product verdict",
  ], { x: 9.0, y: 1.7, w: 3.73, h: 4.7 }, 16);
  caption(s, "Always-On Agents, Table 18 (arXiv 2606.30306). Qwen2.5-7B reader, nine fault patterns.");
}

// ------------------------------------------------------------------ 21 security
{
  const s = newSlide("CONTENT", "Memory turns one injection into a lasting compromise",
    "The security survey explains why this matters. Memory turns a one-shot prompt injection into a persistent compromise. It maps attacks onto six lifecycle phases. At write time, MINJA plants poison through ordinary queries, and AgentPoison reported over eighty percent attack success with under a tenth of a percent of memory poisoned. Consolidation can launder poison into a trusted-looking lesson. At retrieval, a salient memory can override what the user asked. At execution, memory steers tool calls. Sharing spreads infection, and deletion misses copies in summaries. Their answer is five testable governance properties: write authorization, provenance, user-scoped retrieval, rollback, and verified forgetting.");
  addFigure(s, FIG("fig17_memory_security_lifecycle.png"), undefined, "memory security lifecycle");
  caption(s, "Long-Term Memory Security survey (arXiv 2604.16548 v6, expanded EMNLP 2026 paper).");
}

// ------------------------------------------------------------------ 22 two cents
{
  const s = newSlide("CONTENT", "My two cents",
    "Here are my own takeaways. One: memory is three problems sharing one word: storage engineering, learning, and governance. Most products solve the first, and almost nobody measures the third. Two: LoCoMo-style leaderboards are close to saturated. When full context still wins, the leaderboard is ranking compression. I'd trust controlled comparisons like Harness and MERIT more. Three: the write path is underrated. Extraction errors, context collapse and poisoning all happen at write time. Four: forgetting is a feature. Memory needs what databases have: schemas, tombstones, backups and garbage collection. Five: match the substrate to the job, and expect portfolios. Learning to route between memories is the next big open problem. My prediction: within a year, provenance, versioning and per-user scoping will ship by default in memory APIs.",
    "Takeaways");
  const ops = [
    ["Memory is three problems", "storage engineering, learning, governance; most products solve only the first"],
    ["Recall leaderboards are saturating", "when full context wins, the board ranks compression; trust controlled studies"],
    ["The write path is underrated", "extraction errors, context collapse and poisoning all start at write time"],
    ["Forgetting is a feature", "schemas, tombstones, backups, garbage collection, like a database"],
    ["Match substrate to job", "oracle routing 0.93 vs best single 0.65; learning to route is the open problem"],
  ];
  ops.forEach(([head, body], i) => {
    const col = i < 3 ? 0 : 1, row = i < 3 ? i : i - 3;
    const x = 0.6 + col * 6.17, y = 1.4 + row * 1.62;
    card(s, x, y, 5.96, 1.42);
    badge(s, x + 0.25, y + 0.25, String(i + 1), [C.accent1, C.accent2, C.accent3, C.accent5, C.accent4][i]);
    s.addText(head, { x: x + 0.9, y: y + 0.18, w: 4.9, h: 0.5, fontSize: 18, bold: true, color: C.text1, valign: "middle", margin: 0, isTextBox: true });
    s.addText(body, { x: x + 0.9, y: y + 0.7, w: 4.9, h: 0.62, fontSize: 14, color: C.text1, valign: "top", margin: 0, isTextBox: true });
  });
  card(s, 6.77, 4.64, 5.96, 1.42, THEME.colors.dk2);
  s.addText([
    { text: "Prediction", options: { bold: true, color: C.accent4, breakLine: true } },
    { text: "Within a year, memory APIs ship provenance, versioning and per-user scoping by default, like databases ship transactions.", options: { color: C.background1 } },
  ], { x: 7.05, y: 4.74, w: 5.45, h: 1.22, fontSize: 15, valign: "middle", margin: 0, isTextBox: true, objectName: "prediction" });
}

// ------------------------------------------------------------------ 23 checklist
{
  const s = newSlide("CONTENT", "A builder's checklist",
    "If you're building an agent, here's the checklist I'd use. Run no-memory and full-context baselines, and report stateful minus reset over time. Tag every write with its source, time, validity window, scope and confidence. Use update-on-write stores or two-clock graph edges for facts that change. Show the model recency and provenance next to each memory. Cap and consolidate, but keep raw episodes so you can audit and roll back. Scope retrieval by user, and test deletion by probing summaries and indexes. Track tokens, latency and dollars per successful task. And keep retrieval shallow for agents that act.");
  const items = [
    "Run no-memory and full-context baselines; report stateful − reset over time",
    "Tag every write: source, timestamp, validity window, scope, confidence",
    "Use update-on-write or bi-temporal edges for facts that change",
    "Show recency and provenance next to each memory in the prompt",
    "Cap and consolidate, but keep raw episodes for audit and rollback",
    "Scope retrieval per user; probe summaries and indexes after deletion",
    "Track tokens, latency and dollars per successful task",
    "Keep retrieval shallow for agents that act",
  ];
  items.forEach((t, i) => {
    const col = i % 2, row = Math.floor(i / 2);
    const x = 0.6 + col * 6.17, y = 1.45 + row * 1.3;
    card(s, x, y, 5.96, 1.1);
    s.addShape(pres.shapes.OVAL, { x: x + 0.25, y: y + 0.3, w: 0.5, h: 0.5, fill: { color: THEME.colors.accent3 }, line: { color: THEME.colors.accent3, width: 0 } });
    s.addText("✓", { x: x + 0.25, y: y + 0.3, w: 0.5, h: 0.5, fontSize: 16, bold: true, color: C.background1, align: "center", valign: "middle", margin: 0, isTextBox: true });
    s.addText(t, { x: x + 0.95, y: y + 0.1, w: 4.85, h: 0.9, fontSize: 15, color: C.text1, valign: "middle", margin: 0, isTextBox: true });
  });
}

// ------------------------------------------------------------------ 24 references
{
  const s = newSlide("TITLE_DARK", "Thank you",
    "That's my short story. All of these papers are linked in my GitHub repository, together with the article, the slides, and the data behind every chart, so you can check the numbers yourself. The short version: agents don't need to remember more. They need to remember better, and to be able to forget on purpose. Thanks for watching.");
  s.addText("Agents don't need to remember more. They need to remember better, and forget on purpose.", { placeholder: "body" });
  const refs = [
    "Li et al. Memory-Centric Continual Learning for AI Agents. arXiv 2610.29357",
    "Ding et al. Always-On Agents. arXiv 2606.30306",
    "Zhoubian et al. Memory for Large Language Models. arXiv 2607.25380",
    "Luo et al. From Storage to Experience. arXiv 2605.06716",
    "Lin et al. Long-Term Memory Security in LLM Agents. arXiv 2604.16548",
    "Huang et al. Harness the Memory. arXiv 2608.15008",
    "Mishra & Mishra. When Does Memory Help? (MERIT). arXiv 2609.05441",
    "Chhikara et al. Mem0. arXiv 2504.19413 · Rasmussen et al. Zep. arXiv 2501.13956",
    "Wu et al. LongMemEval. arXiv 2410.10813 · Packer et al. MemGPT. arXiv 2310.08560",
  ];
  s.addText(refs.map((r, i) => ({ text: r, options: { breakLine: i < refs.length - 1 } })),
    { x: 9.0, y: 1.4, w: 3.9, h: 4.9, fontSize: 11, color: C.background2, valign: "top", margin: 0, paraSpaceAfter: 6, isTextBox: true, objectName: "references" });
  s.addText("github.com/pgala3183/297_short_story", { x: 9.0, y: 6.5, w: 3.9, h: 0.4, fontSize: 12, color: C.accent4, margin: 0, isTextBox: true });
}

// ------------------------------------------------------------------ write
(async () => {
  fs.mkdirSync(path.dirname(OUT_PPTX), { recursive: true });
  await pres.writeFile({ fileName: OUT_PPTX });
  const skillTheme = process.env.PPTX_APPLY_THEME;
  if (skillTheme) {
    const { applyTheme } = require(skillTheme);
    await applyTheme(OUT_PPTX, THEME);
  }
  // narration script
  const wpm = 152;
  let md = "# Narration script\n\nSpoken over the slides in `slides/memory_for_llm_agents.pdf`. The same text is in each slide's speaker notes.\n";
  md += `Estimated length at ${wpm} words per minute: `;
  const total = narration.reduce((a, n) => a + n.notes.split(/\s+/).length, 0);
  md += `${total} words, about ${(total / wpm).toFixed(1)} minutes.\n\n`;
  let t = 0;
  narration.forEach((n, i) => {
    const words = n.notes.split(/\s+/).length;
    const mm = String(Math.floor(t / 60)).padStart(2, "0"), ss = String(Math.round(t % 60)).padStart(2, "0");
    md += `## Slide ${i + 1}: ${n.title}  \`~${mm}:${ss}\`\n\n${n.notes}\n\n`;
    t += (words / wpm) * 60 + 0.8;
  });
  fs.mkdirSync(path.join(ROOT, "video"), { recursive: true });
  fs.writeFileSync(path.join(ROOT, "video", "narration_script.md"), md, "utf8");
  console.log(`wrote ${OUT_PPTX} (${narration.length} slides, ${total} narration words, ~${(total / wpm).toFixed(1)} min)`);
})();
