# Narration script

Spoken over the slides in `slides/memory_for_llm_agents.pdf`. The same text is in each slide's speaker notes.
Estimated length at 152 words per minute: 2371 words, about 15.6 minutes.

## Slide 1: Memory for
LLM Agents  `~00:00`

Hi, I'm Pratham Gala, and this is my CMPE 297 short story on memory for LLM agents. Over the next fifteen minutes or so, I'll walk through five survey papers from 2026 and two new benchmark papers. I'll explain the main taxonomy, look at the techniques that top the leaderboards, and finish with my own opinions on where this field is heading.

## Slide 2: A bigger context window is a desk, not a memory  `~00:25`

Let me start with why this matters. Agents forget what you told them last week. Or worse, they remember it and ignore it. The tempting fix is a bigger context window, but a long window is a desk, not a memory. The LongMemEval benchmark showed that GPT-4o lost thirty percent of its accuracy when it got a user's full chat history instead of only the relevant sessions, even though the answers were right there in the prompt. Meanwhile, one survey coded 435 papers and found that sixty-two percent work on retrieval, but only six percent on rollback. The field is very good at remembering and much weaker at governing and undoing memory. That imbalance runs through this whole talk.

## Slide 3: The reading list: seven papers, April to November 2026  `~01:13`

Here is my reading list. The main paper is Memory-Centric Continual Learning for AI Agents, posted in October by a 28-author team from Harbin Institute of Technology Shenzhen, Tsinghua, Huawei and China Telecom. Around it are four more surveys. Always-On Agents, from June, focuses on governance. Memory for Large Language Models, from Tsinghua, NUS and Bosch, looks inside the model. From Storage to Experience is an ACL 2026 Findings paper. And a security survey from MemTensor is an EMNLP 2026 paper that was revised through November. For the leaderboard I added two independent evaluation papers, Harness the Memory and MERIT, shown in orange.

## Slide 4: Three layers of memory, and one question across them  `~01:55`

These papers don't compete. They describe different layers of one stack. At the bottom is the model layer: how the network itself carries state, through KV caches, recurrent states, or weights updated at test time. In the middle is the agent layer: what is worth writing down, how it's organized, and when it comes back. On top is the governance layer: who may write, read, share or delete a memory, and whether a bad one can be rolled back. Evaluation cuts across all three. Does memory change what the agent does, and what does it cost?

## Slide 5: Main paper: judge memory by what it changes  `~02:33`

The main paper makes one provocative claim. Memory should be judged by whether it improves future actions, not by what it can retrieve. By that standard, most current systems are passive caches that happen to be good at quiz questions. The paper makes three contributions. First, a three-axis taxonomy with a lifecycle model. Second, an evaluation protocol for retention, adaptation and transfer, run against matched baselines, so that memory helped can't secretly mean we gave the model more tokens. Third, a scaling framework for how performance grows with experience, storage and compute.

## Slide 6: Taxonomy: WHERE it lives, WHAT it holds, HOW it is run  `~03:10`

Here is the taxonomy. WHERE is the substrate. Contextual memory is tokens in the live prompt: instant, but gone when the session ends. Activation memory is KV caches and recurrent states. External memory is logs, vector stores and graphs, like MemGPT, Mem0 or A-MEM. You can edit and delete it, but items can quietly stop being retrieved, which the authors call functional forgetting. Parametric memory is weights and adapters: cheap to read, expensive and risky to write. WHAT is the asset: episodic memories of what happened, semantic facts, and procedural know-how like workflows and skills. HOW is the policy: fixed rules like top-k, deliberative policies where the LLM decides, or controllers learned from outcomes. The axes are independent. Mem0 is external, semantic and deliberative. Memory-R1 swaps in a learned policy.

## Slide 7: Memory is two coupled loops, not a pipeline  `~04:02`

The paper also argues that memory isn't a pipeline but two coupled loops. The inner loop is the memory state. First, writing. The authors call admission the plasticity boundary, because whatever passes it can change future behavior. Second, consolidation, where episodes become rules. The danger here is context collapse: compression strips out when, who and under what conditions, and leaves a confident but wrong rule. Third, retrieval and use. Fourth, revision and forgetting, where marking a fact as outdated is different from deleting things to save space. The outer loop is policy evolution: task feedback updates the rules of the inner loop. Almost no deployed system runs that outer loop online today.

## Slide 8: Storage → Reflection → Experience  `~04:47`

A second survey, From Storage to Experience, tells the same story as a progression. Storage keeps raw trajectories, in windows, vector stores, or tables and graphs. Reflection refines a single trajectory, the way Reflexion critiques itself or Mem0 maintains its facts. Experience abstracts across many trajectories into rules and skills that transfer to new tasks. The stages stack rather than replace each other. The authors admit they can't rank the stages with numbers, because each one optimizes a different goal. That's an early hint of the evaluation problem we'll see later.

## Slide 9: Inside the model: implicit state vs. addressable memory  `~05:24`

The Tsinghua, NUS and Bosch survey goes inside the model. Implicit memory, in blue, is a by-product of computation: the KV cache, and state-space models like Mamba-3, RWKV-7 and Gated DeltaNet. Explicit memory, in orange, has its own addressable component: kNN-LM's datastore, mixture-of-experts layers, and test-time learners like Titans, which update a memory module during inference based on how surprising the input is. One fun detail: the offline, short-term corner is empty. Their conclusion is that hybrid designs will become the norm, which is exactly what the agent-level surveys conclude too.

## Slide 10: Three architectures behind most leaderboard rows  `~06:01`

Here are the three architectures behind most leaderboard rows. MemGPT, now Letta, treats the context window like RAM, and pages data to a recall store and an archival vector store with function calls. Mem0 extracts facts from each exchange, compares each one with the most similar stored memories, and picks add, update, delete, or do nothing. That reconcile step targets the most common real problem: facts that change. Zep is a temporal knowledge graph. It keeps raw episodes, an entity graph where facts are edges, and community summaries. Every fact carries two clocks: when it was true, and when the system learned it.

## Slide 11: Experience memory: storing lessons instead of facts  `~06:42`

The other family in every survey is experience memory, where the agent stores lessons instead of facts. Reflexion writes a verbal post-mortem after a failed attempt. ExpeL compares successes and failures to extract general insights. Agent Workflow Memory induces reusable workflows, with reported gains of about twenty-five percent on Mind2Web and fifty-one percent on WebArena. ReasoningBank distills strategies from both successes and failures. Voyager stores executable code skills. And learned controllers like Memory-R1 use reinforcement learning to decide what to store, instead of prompting the model to guess.

## Slide 12: LoCoMo: full context wins accuracy, memory wins latency  `~07:18`

Now the leaderboard. LoCoMo is the benchmark everyone reports: long conversations of about 26 thousand tokens, followed by questions. This chart plots the Mem0 paper's results: a judge score against p95 latency on a log scale. The headline is that Mem0 matches or beats the other memory systems while answering in about one and a half seconds, versus seventeen for full context, with ninety-three percent fewer tokens. But look at the top right. Full context still scores highest, 72.9 against 66.9. A 26 thousand token conversation fits in any modern window, so on LoCoMo memory is a cost optimization, not an accuracy win. Also, these baselines were run by Mem0's own authors.

## Slide 13: LongMemEval: a temporal graph beats a 115k-token prompt  `~08:03`

LongMemEval is harder: 500 questions over histories of about 115 thousand tokens, testing extraction, multi-session reasoning, temporal reasoning, knowledge updates, and knowing when not to answer. Here the picture flips. With GPT-4o, Zep's temporal graph scored 71.2 percent against 60.2 for the full history in the prompt. It cut latency by about ninety percent and read about 1,600 tokens instead of 115 thousand. The LongMemEval authors also ran useful ablations. Indexing each memory under extra fact-based keys raised recall by about nine percent, and adding time ranges to time-sensitive queries improved temporal recall by seven to eleven percent.

## Slide 14: Independent test: no memory substrate wins every column  `~08:42`

Vendor tables compare whole products, so I wanted an independent view. Harness the Memory holds everything fixed except the memory substrate: same model, same prompts, same harness. It tests eleven designs. No substrate wins every column. A LightRAG-style graph wins LoCoMo and LongMemEval. A gist index wins long-range and test-time learning. Conflict resolution is bad for everyone, with a best score of 0.32. Full context collapses on LongMemEval because the history no longer fits. Memory stored in LoRA weights is the weakest almost everywhere. And the winning graph is about thirty-six times slower per query than a plain vector index.

## Slide 15: For agents that act, more memory is not automatically better  `~09:23`

The most interesting part is what happens when the agent has to act. On ALFWorld, an embodied task suite, distilled strategies in the style of ReasoningBank gave the biggest boost, almost ten points. On coding, almost everything hurt except simple lexical retrieval. They also varied how many memories get retrieved. On LoCoMo, retrieving more always helped. On ALFWorld it hurt, and plain vector and BM25 indexes eventually fell below the no-memory baseline. An attention probe suggests why: retrieved text pulls attention away from the current observation and the list of valid actions.

## Slide 16: When facts change, update-on-write beats similarity search  `~09:60`

MERIT asks the question I care about most as a builder. When a fact changes halfway through a series of tool-using tasks, does the agent use the new value? With no memory it never succeeds. Full replay of past transcripts works, but it's expensive. Embedding retrieval is the weak spot. It returns the stale and the fresh value side by side, with no sense of recency, and success drops as low as 0.35. Fact stores that update on write, and LLM summaries, stay between 0.7 and 1.0. Two more findings stuck with me. Agents ignored the correct retrieved value 45 percent of the time. And swapping the fact extractor moved one domain by up to 60 points.

## Slide 17: Ablation: memory that helps early can hurt later  `~10:47`

The main paper ran two small but important ablations with Mem0. First, how the agent reads memory matters. Searching and summarizing saves tokens but costs accuracy, and raising the read budget from 512 to 2,048 tokens moved LongMemEval accuracy from 35 to 44 percent. Second, and this is the plot I most want people to see, they compared an agent that keeps its memory with the same agent reset to empty. After 64 dialogues, memory helped by seven points. After 128 it hurt by about ten, and after 256 by about fourteen. Consolidation shrank the store but didn't fix it. Leaderboards measure one moment. Deployment is a trajectory.

## Slide 18: Why recall scores mislead: memory must pass four gates  `~11:30`

So how should we measure memory? The main paper proposes a four-gate cascade, and I've attached evidence from the other papers to each gate. Preservation: was it stored correctly? That's MERIT's extractor result. Access: can it be found at the right moment? That's LongMemEval's key expansion. Utilization: does the agent actually use it? That's the 45 percent ignore rate. Effect: does behavior beat no memory, now and later? That's the stateful-minus-reset curve. The overall benefit is capped by the leakiest gate, and recall benchmarks mostly test the first two.

## Slide 19: The field is great at remembering, poor at un-remembering  `~12:06`

Now the governance layer. Always-On Agents treats a long-running agent as a persistent-state system, whose state includes permissions, commitments and audit logs, not just memories. The authors coded 435 papers by lifecycle stage. Accumulating and using memory is well covered: retrieval alone shows up in 62 percent of works. Governing and recovering is thin: forgetting is fifteen percent, rollback six. None of the coded works reports how well recovery actually works. The authors say each memory record should carry six properties: authority, scope, mutability, provenance, recoverability and actionability.

## Slide 20: A governance scorecard, not an accuracy leaderboard  `~12:42`

They then built a small evaluation contract called AOEP. It scores obligations, not answer quality: restarts, revoked permissions, deletion requests and poisoned tool output. A governed reference design met all fifteen obligations. Raw storage met seven. The fact-extracting systems met only three or four, and in two episodes they leaked a deleted billing address and an attacker-planted address. The authors say clearly this is a small pilot, not a product verdict. My favorite detail is the no-memory row. It passes every must-not check by storing nothing, and fails every obligation. Safety and usefulness have to be measured together.

## Slide 21: Memory turns one injection into a lasting compromise  `~13:21`

The security survey explains why this matters. Memory turns a one-shot prompt injection into a persistent compromise. It maps attacks onto six lifecycle phases. At write time, MINJA plants poison through ordinary queries, and AgentPoison reported over eighty percent attack success with under a tenth of a percent of memory poisoned. Consolidation can launder poison into a trusted-looking lesson. At retrieval, a salient memory can override what the user asked. At execution, memory steers tool calls. Sharing spreads infection, and deletion misses copies in summaries. Their answer is five testable governance properties: write authorization, provenance, user-scoped retrieval, rollback, and verified forgetting.

## Slide 22: My two cents  `~14:02`

Here are my own takeaways. One: memory is three problems sharing one word: storage engineering, learning, and governance. Most products solve the first, and almost nobody measures the third. Two: LoCoMo-style leaderboards are close to saturated. When full context still wins, the leaderboard is ranking compression. I'd trust controlled comparisons like Harness and MERIT more. Three: the write path is underrated. Extraction errors, context collapse and poisoning all happen at write time. Four: forgetting is a feature. Memory needs what databases have: schemas, tombstones, backups and garbage collection. Five: match the substrate to the job, and expect portfolios. Learning to route between memories is the next big open problem. My prediction: within a year, provenance, versioning and per-user scoping will ship by default in memory APIs.

## Slide 23: A builder's checklist  `~14:52`

If you're building an agent, here's the checklist I'd use. Run no-memory and full-context baselines, and report stateful minus reset over time. Tag every write with its source, time, validity window, scope and confidence. Use update-on-write stores or two-clock graph edges for facts that change. Show the model recency and provenance next to each memory. Cap and consolidate, but keep raw episodes so you can audit and roll back. Scope retrieval by user, and test deletion by probing summaries and indexes. Track tokens, latency and dollars per successful task. And keep retrieval shallow for agents that act.

## Slide 24: Thank you  `~15:31`

That's my short story. All of these papers are linked in my GitHub repository, together with the article, the slides, and the data behind every chart, so you can check the numbers yourself. The short version: agents don't need to remember more. They need to remember better, and to be able to forget on purpose. Thanks for watching.

