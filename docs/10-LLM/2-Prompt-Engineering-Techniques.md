# Prompt Engineering Techniques

:::tip Do OpenAI models learn?
OpenAI models like GPT-3 do not learn or adapt during user interactions. They generate responses based on pre-training with a large dataset and do not update their knowledge from individual conversations. Any improvements or updates to the model's capabilities are made through a controlled retraining process by OpenAI, not through real-time learning.
:::

This section discusses prompt engineering techniques that can help LLMs solve certain problems more effectively.

## Zero-shot learning

LLMs are trained on such large amounts of data they may be be able to perform some tasks with very little prompting. Try the example below and change the sentence to see what outcomes you find.

```text title="Enter in the user prompt:"
Classify the text into neutral, negative or positive.
Text: The Contoso Bike Store is a great place to buy a new bike.
Sentiment:
```

## Few-shot learning

If zero-shot learning is failing for your examples and more complex tasks, few shot prompting can provide examples that can better steer the model to the desired outcomes. Examples show the model cleanly how we want it to operate. Try the example below to see the outcome. Can you think of other examples that could leverage few-shot learning?

```text title="Enter in the user prompt:"
Headline: "Contoso Bike Store opens new location in Seattle"
Sentiment: Positive
Headline: "Contoso Bike Store announces new product line"
Sentiment: Neutral
Headline: "Contoso Bike Store recalls faulty bikes"
Sentiment: Negative
Headline: "Contoso Bike Store wins award for best customer service"
Sentiment:
```

The next two sections are very well described in the ['Meet Mr Prompty'](https://www.linkedin.com/pulse/meet-mr-prompty-break-tasks-down-chain-thought-dynamic-mario-fontana/?trackingId=%2FzJrYZ06TxWwVVLkU7rxug%3D%3D) articles on LinkedIn, thank you author, Mario Fontana, for sharing your insights.

## Chain of thought prompting

In this technique, the LLM is responsible for breaking the task down into smaller steps. The LLM uses its knowledge of the world and its ability to reason. The LLM then generates a chain of thoughts that leads to the solution of the task.

```text title="Enter in the user prompt:"
I like to ride my bike around the city, but I'm not sure if I should buy a new one or repair my old one. Can you help me decide?
Take a step-by-step approach in your response, cite sources, and give reasoning before sharing a final answer in the below format: ANSWER is: <name>
```

## Advanced Chain of Thought

Let's try a more complex reasoning task that requires multiple steps:

```text title="Enter in the user prompt:"
A cyclist is planning a 100-mile ride. Their bike has the following specifications:
- Wheel circumference: 2.1 meters
- Current gear ratio: 3:1 (3 pedal rotations = 1 wheel rotation)
- Average cadence: 80 RPM
- Expected riding time: 6 hours including breaks

Calculate:
1. How many wheel rotations are needed for 100 miles?
2. How many pedal rotations will that require?
3. What will be their average speed?
4. Is their planned cadence realistic for this duration?

Work through each step systematically, showing your calculations and reasoning.
```

## Prompt Decomposition

Break complex tasks into smaller, manageable components:

```text title="Enter in the user prompt:"
I want to organize a charity bike ride event for 200 participants. Break this down into the main planning components, then for each component, list the specific tasks needed. Structure your response as:

COMPONENT: [Name]
- Subtask 1
- Subtask 2
...

COMPONENT: [Next Name]
- Subtask 1
...

Consider: safety, logistics, marketing, legal requirements, fundraising, and participant experience.
```

## Multi-Step Reasoning

Guide the AI through complex logical processes:

```text title="Enter in the user prompt:"
A bike shop owner needs to decide whether to stock electric bikes. Help them analyze this decision using the following framework:

STEP 1: Market Analysis
- Who would buy electric bikes in their area?
- What's the competitive landscape?
- What are current trends?

STEP 2: Financial Analysis
- Initial investment required
- Expected profit margins
- Break-even analysis

STEP 3: Operational Analysis
- Storage and display requirements
- Staff training needs
- Maintenance and support implications

STEP 4: Risk Assessment
- What could go wrong?
- How to mitigate risks?

STEP 5: Decision Framework
- Criteria for making the decision
- Weighted importance of factors
- Final recommendation

Work through each step methodically with specific examples and numbers where possible.
```

## Comparative Analysis Prompting

Use structured comparisons to evaluate options:

```text title="Enter in the user prompt:"
Compare these three bike types for a daily 10-mile commute in a hilly city. Use this comparison framework:

CRITERIA TO COMPARE:
- Purchase cost
- Maintenance requirements
- Physical effort required
- Weather adaptability
- Security considerations
- Long-term durability

BIKES TO COMPARE:
1. Traditional road bike ($800)
2. Electric commuter bike ($2,200)
3. Folding bike ($600)

For each criterion, rank the bikes 1-3 (1=best) and explain your reasoning. Then provide an overall recommendation based on different commuter priorities.
```

## Evidence-Based Prompting

Request specific evidence and sources:

```text title="Enter in the user prompt:"
I've heard that cycling to work is better for the environment than driving, but I want to understand the actual impact. Please provide:

1. Specific data on CO2 emissions per mile for:
   - Average car
   - Electric car
   - Bicycle (including manufacturing)

2. Studies or sources that support these numbers

3. Other environmental factors beyond CO2 (tire waste, road wear, etc.)

4. The break-even point: how many miles of cycling offset the environmental cost of manufacturing a bike?

Please cite specific studies, government data, or research papers where possible.
```

## Constraint Optimization

Present problems with multiple constraints to solve:

```text title="Enter in the user prompt:"
Design the optimal bike maintenance kit with these constraints:

HARD CONSTRAINTS (must meet):
- Total weight under 2 pounds
- Fits in a small frame bag (8" x 4" x 3")
- Budget under $100
- Can handle 90% of roadside emergencies

SOFT CONSTRAINTS (nice to have):
- Tools have multiple functions
- Includes emergency contact method
- Weather-resistant storage
- Quick-access organization

List the specific items you'd include, with:
- Item name and purpose
- Weight and dimensions
- Cost estimate
- How it meets the constraints

Explain your trade-off decisions and what you excluded and why.
```

## Scenario Planning

Explore multiple future scenarios:

```text title="Enter in the user prompt:"
A city is planning bike infrastructure improvements. Analyze three different scenarios for how cycling might evolve over the next 10 years:

SCENARIO 1: "Electric Revolution"
- 60% of bikes are electric by 2034
- Higher average speeds and longer distances
- Different infrastructure needs

SCENARIO 2: "Micro-Mobility Integration"
- Bikes integrated with scooters, public transit
- Focus on first/last mile connections
- Shared mobility dominance

SCENARIO 3: "Health & Recreation Focus"
- Cycling primarily for fitness and leisure
- Emphasis on recreational trails and parks
- Less commuter cycling

For each scenario:
1. What infrastructure would be most important?
2. What policies would support this future?
3. What are the implications for bike shop businesses?
4. How likely is this scenario (0-100%)?

Then recommend a balanced infrastructure plan that works well across all scenarios.
```

These advanced techniques help you leverage the AI's reasoning capabilities more effectively. The key is providing clear structure and specific instructions while allowing the AI to apply its knowledge and analytical abilities.
