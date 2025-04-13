# RAG_LLMs
A collective repository of our mini-project, with RAG based LLMs, under AI Club!

Hello world, so before jumping on to the stuff I would like to thank our mentors Anish & Nishitha for giving us all the support throughout this mini project and it was a great time learning under them and building such great 
apps almost within a month, and would thank Shailesh to arrange these mini projects!! lets start this awesome journey , please If you catch an error, consider it an Easter egg from the chaos gods. Just kidding… mostly.

## WEEK 1 

Before we could build anything smart, we had to teach our models **how to read** , not just casually scroll like they're on Instagram, but actually understand text.

So this week, we dove into some old-school NLP heroes that still hold their ground.
###  TF-IDF  
> *“I know the word is common... but is it really important?”*

TF-IDF taught us how to score words based on how often they appear , but also how rare they are across the whole dataset. So, “Rare” gets a boost, “the” gets booted.  
Simple, efficient, and still kinda magical.
###  BM25  
> *“Like TF-IDF, but caffeinated and tuned for ranking.”*

BM25 helped us go one step further , it not only weighted terms smartly, it also considered document length and relevance for **better search accuracy**. It was like learning how Google decides what you see.

###  GloVe Embeddings  
> *“Tell me who your neighbors are, and I’ll tell you who you are.”*

GloVe introduced us to word embeddings — where words became vectors in space. Words with similar meanings started clustering, analogies came to life, and math got... poetic.  
Basically, words finally left 1995 and entered neural space.

 You can find our notes, slides, and references in the Resources folder.

This week laid the foundation — so by the time we started RAG, our models weren’t just parroting words... they were starting to *understand them.*

##  WEEK 2: RAG-ing Into Action

So Week 2 was all about learning what **RAG** even means — and no, it’s not a cleaning cloth, though it does clean up your chatbot’s IQ quite a bit.

We didn’t just randomly throw embeddings and LLMs together — we studied. We watched. We read. We RAG’d. Hard.

###  we studied (because we’re nerds now):

We read some articles, watched some videos all of which link is there in the resources folder

- Optional Reading: [Original RAG Paper (Lewis et al., Facebook AI)](https://arxiv.org/abs/2005.11401)  
  → Only if you wanted to flex your neurons. Some of us cried. Some of us understood. Some... did both.
  
The goal this week was to understand what it really means to retrieve documents, ground the LLM in actual context, and generate answers without hallucination,
By the end of this week, we were ready to build our own RAG pipelines — from scratch. We knew which models to try, which vector stores to test, and that *maybe*... just maybe... ChatGPT wasn’t magic after all — it was RAG.

All article links and videos live in the Resources folder.

## WEEK 3–5

During weeks 3 to 5, we built our own RAG-based chatbot implementations using everything we had learned so far. Each of us explored different domains, retrievers, embedding models, and ideas. You can check out the respective implementations in their own branches in this repository.

## The Journey Ends (or maybe just begins...)
This mini project was more than just code, it was latenight cramming, wild prompting experiments, retriever wars, and a lot of "why is it not retrieving properly" moments. But through it all, we learned not just how to build a RAG pipeline, but how to think like builders — experiment, fail, fix, repeat, and ship.

We're proud of what we created in just a few weeks, a set of fully working, locally hosted, LLM-powered RAG bots that can reason over real data. And even prouder of how much we've learned from each other, from our mentors, and from good old trial and error.

Big shoutout again to everyone who made this project possible, and to anyone reading this: clone a branch, try a build, ask the bot something wild ,and if it breaks? Well, we warned you. Might just be another one of those Easter eggs from the chaos gods.

Credits->
This was...

RAG_LLMs  
A mini-project by Team SG5  
as part of AI Club led by Shailesh,  @ CFI, IIT Madras  

----------------------------

Created with  :
Ideas  
Code  
Confusion  
Debugging  
and a LOT of Google searches  

----------------------------

Mentored by : 
Anish  
Nishitha  

----------------------------

Built by:
Soham  
Avisha  
Aishwarya  
Hemanth  
Manish  
Arnav  

----------------------------

Featuring  
HVAC machines described to a chatbot, to retrieve the relationship between machine and effect (using knowledge graphs)
 
Research paper RAG- what kind of paper you want as a query, the database is the abstracts of the papers 

comp team rule book qna RAG
uses pdf (we need to use OCR for pdfs) 

legal amendments qna (LLMs will need to be complex)

screenr (stock market queries rag, mathematical databases)

Dune wiki chatbot (web scraping)

----------------------------

Runtime: ~5 weeks  

----------------------------

If you’re seeing this,  
we actually finished it.

Thanks for scrolling ✨  


