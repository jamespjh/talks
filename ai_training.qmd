# Some thoughts on training in AI for digital researchers

* Prof James Hetherington
* 2025 09 11

## Preamble

### Why am I doing this?

* Digital transformation, singularity yada yada...
* The quality of our AI discourse is very poor
    * This is a POLITICAL space
    * This is a MARKETING HYPE space
* This is a SOCIO-TECHNICAL space
    * We (carpentries and related communities) are actually quite good at these!
    * Carpentries instructor training is PRECISELY the kind of training that works here
    * As scientists, our response to this should be knowledge-based

### What is this talk?

* It's a sketch of some topics I think we should be thinking about
* It's a sketch of some topics I think we should be thinking about teaching

### Who is it for?

* I'm not yet sure which of these things 
    * we should be teaching to postdocs and PhD students, 
    * which we should be including in instructor training for trainers, 
    * which we should be teaching to RSEs and other RTPs

### Scope

* I'm talking about LLMs, and systems built on top of them:
    * Agentic agents
    * Stateful agents
    * Reasoning models
* I'm talking about AI-assisted software engineering in particular
    * Code completion
    * Pull request generators
    * Agentic editors and IDEs
    * Vibe-coding??
* I hate using "AI" as a proxy for this. See more later
* I'm not talking about other ML things
    * Generative image and video models
    * Classical ML - classifiers etc
    * Proxy models of simulations

### What's our objective?

* I think the RTP identity will need to change to accommodate new professions
* I think we all have a lot of thinking and learning to do before we understand what's going enough to define best practice
* If we can't define a consensus best practice we can't teach
* I don't think our consensus will be universal - there will be dissenters
    * I think that's OK?

### Disclaimer

* No one is an expert
* Some are more knowledgeable than others
* My knowledge is patchy
* There is no shame in ignorance
    * Only in persistent ignorance
* I will change my mind on some things in our dialogue today
    * I will be less wrong after
    * I hope you will be too

### Broad topic areas

* How LLMs work
* How to use AIs
* How to Build with AIs
* The Politics, Philosophy and Economics of AI

## How LLMs work
    
* Hypothesis: philosophically, we should understand how tools work before using them. 
    * Is this defensible?
* Hypothesis: practically, we use tools more effectively and safely if
we understand how they work. 
    * Is this definsible?
* Assertion: there's a LOT more to how the big models work than just Transformers.
* Hypothesis: Understanding beyond "machine learning magic" is essential and requires updating mathematical intuitions

### How to use AIs

* Hypothesis: skilled users use them more effectively 
    * Is this defensible? 
        * Unskilled use is a design objective.
        * Deskilled users may be a systems endpoint?
    * It may be divergent for different tools

### How to build with AIs

* Assertion: a lot of what we do as research engineers in the future will be composing, connecting and designing AIs
* Hypothesis: this will require a new RTP identity: "research agent engineers?"
    * I have no idea if this is right

### The politics, philosophy and economics of AI

* Assertions: the poor quality of the AI discourse comes from
    * low knowledge
    * anxiety
    * hype
    * source bias
* Assertion: we **research** technology professionals, have a professional duty to get this right
* Hypothesis: we have some attributes that mean we're in a good place to think about this well
    * Technical knowhow substrate
        * But it's patchy and degraded
    * Independence
        * But anxiety and social risk
    * Epistemological tradition
* Hypothesis: an interest in speculative fiction is an asset here

## How AIs work

* Question as to how far back we go
* Question as to how much mathematics to assume
    * Fork the syllabus?
    * Reference for those with the background?
* Work our way up the tower

### The technical substrate

* GPUs, parallel computing, warehouse-scale computers
  * This will be necessary when we get to the environmental science
* Linear algebra
* Optimisation (SGD, Adam etc)

* This all works nicely as hands-on technology demistifier classes
* Probably teach at the Cupy/Pytorch level 

### 

## Building with AIs

* Context engineering
* AI security, prompt injection
* RAG
* Tool integration - model context protocol
* Stateful agents - 


