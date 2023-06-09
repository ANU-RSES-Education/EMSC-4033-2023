# Assessment task 1, 2023 
## total 20 marks

This assessment task is worth 20% of the course mark. The assessment is due as a wattle submission.

It should take the form of a single `jupyter` notebook that you upload. We expect to be able to run your examples in the notebook on the course server, so please check this carefully. 

## A) Automating garden watering (5 marks)

Consider the following set of requirements:

When there is a drought in Australia, everyone has to set their garden irrigation to a specific timetable which depends on the day of the week and may alternate week on week. Here is an example of the instructions you might receive from the local water authority.

---

     WATERING TIMES FOR YOUR PROPERTY:
     
       Summer & Autumn, (September-March)
         Week 1: Mon, Wed, Fri, Sat - 5am-7am 
         Week 2: Tue, Thu, Sat, Sun - 9pm-11pm 

       Winter, Spring (April - August)
         Weekdays: 6am-10am
         Weekends: 9pm-11pm
         
 ---

1) Describe how you would approach this problem in the form of an algorithm. 
2) Now think about a different algorithm to address the problem
3) Code up each approach (in python) 

Is either choice better or worse. Which would work better if you had month-by-month instructions ?

## B) Loops (4 marks)

Why do programming languages have loops?

Compare a C/FORTRAN `for` loop (look it up) with a python loop (which uses an `iterator`). What is the conceptual difference between these two language constructs? Which is more powerful, which is faster?


## C) Declarative programming versus Imperative programming (4 marks)

Can you explain the difference between these two concepts (use examples - these do not need to be python examples). 

 - Discuss some examples in python that fit the imperative mode of programming?  
 - Discuss some examples in python that fit the declarative mode of programming?

## D) When can / should I use ChatGPT or GitHub copilot? (7 marks)

ChatGPT is well known for its ability to approximate human writing and we generally do not allow it to be used to produce answers for assignments. It churns out text that is has been trained to generate based on the prompts it receives and with a very large sample of existing text. It turns out that it can write reasonably good python code too. 

In this exercise, we would like you to write a simple python program entirely by instructing chatGPT, and to assess the job it does. Tell us what works well, and what you need to do to make the chatGPT engine write “good” code (well commented, easy to understand etc).

Ask chatGPT to code up the problem in question (A) — you will need first to register with [OpenAI](https://openai.com/) to have access to chatGPT. Then see if you can get it to give you nicely commented code for: 

  - Question A (above)
  - The [Seive of Eratosthenes](https://en.wikipedia.org/wiki/Sieve_of_Eratosthenes) (notebook example number 6)
  - The "nested-square root method for computing the golden ratio" which is given by 
    $$\phi = \lim_{n\rightarrow\infty} \underbrace{\sqrt{1 + \sqrt{1 + \sqrt{1+ \sqrt{ 1 + \cdots}}}}}_{\text{$n$ times}}$$

How useful is chatGPT for this kind of problem? When is it not so useful?

How do you know if it is correct?

**Here is a hint** - you can ask for the last two examples above by name and chatGPT can help you out, but it cannot figure out what to do if you provide an equation. It can give you the equation (as LaTeX code), but it has no idea how to turn it back into python!

**Here is another hint**- ask chatGPT to give you the output from the code for a few iterations. Is this actually the value of the golden ratio (yet another hint: ask it!).




