# Practical Prompt Engineering Examples

:::tip Real-World Applications
This section provides practical, ready-to-use prompt examples for common business and personal scenarios. These examples demonstrate how to apply prompt engineering techniques to solve real problems.
:::

## Business Scenarios

### Customer Service Automation

**Scenario**: Automate responses for a bike shop's customer service.

```text title="System message for customer service bot:"
You are Emma, a customer service representative for Pedal Pro Bike Shop. You are knowledgeable, patient, and helpful.

CAPABILITIES:
- Answer questions about bikes, accessories, and services
- Help customers choose the right bike for their needs
- Provide maintenance advice and troubleshooting
- Check order status (simulate by asking for order number)
- Schedule appointments for bike fitting or repairs

LIMITATIONS:
- Cannot process payments or refunds (direct to manager)
- Cannot make promises about specific delivery dates
- Cannot access real-time inventory (provide general info)

TONE: Friendly, professional, enthusiastic about cycling

ESCALATION: If you cannot help, say "Let me connect you with our bike expert who can better assist you with that specific question."
```

```text title="Example customer query:"
Hi, I'm new to cycling and want to start commuting to work. It's about 8 miles each way with some hills. I'm not very fit yet and have a budget of around $1000. What would you recommend?
```

### Technical Writing Assistant

**Scenario**: Create technical documentation for bike maintenance.

```text title="Technical writing prompt:"
Create a step-by-step maintenance guide with these requirements:

AUDIENCE: Bike shop mechanics (intermediate skill level)
TASK: How to properly adjust rear derailleur shifting
STYLE: Clear, concise, professional
FORMAT: Numbered steps with safety warnings

STRUCTURE:
1. Tools and materials needed
2. Safety precautions
3. Detailed procedure (8-12 steps)
4. Testing and verification
5. Common troubleshooting issues

SPECIAL REQUIREMENTS:
- Include torque specifications where relevant
- Add warning callouts for potential damage points
- Mention when to refer to manufacturer specifications
- Include quality check criteria

Write as if this will be used to train new mechanics.
```

### Market Research Analysis

**Scenario**: Analyze competitor pricing and positioning.

```text title="Market analysis prompt:"
Analyze the electric bike market positioning based on this data:

COMPETITOR DATA:
Brand A: $1,200, 50-mile range, 3-year warranty, target: commuters
Brand B: $2,800, 80-mile range, 5-year warranty, target: enthusiasts  
Brand C: $900, 30-mile range, 1-year warranty, target: casual riders
Brand D: $3,500, 100-mile range, lifetime warranty, target: premium market

ANALYSIS FRAMEWORK:
1. Value proposition of each brand
2. Price-performance positioning
3. Target market segmentation
4. Gaps in the market
5. Recommended positioning for a new entrant

CONSTRAINTS:
- New brand budget: $1,500 - $2,000
- Must differentiate from existing options
- Target urban professionals aged 25-45

Provide specific recommendations for features, pricing, and marketing messaging.
```

## Personal Use Scenarios

### Trip Planning Assistant

**Scenario**: Plan a multi-day cycling vacation.

```text title="Trip planning prompt:"
Plan a 5-day cycling vacation for two intermediate cyclists. Requirements:

PREFERENCES:
- Scenic routes with moderate difficulty
- Daily distances: 40-60 miles
- Mix of road and light trail cycling
- Budget: $2,000 total for accommodation and meals
- Starting point: Portland, Oregon

MUST INCLUDE:
- Daily route descriptions with elevation profiles
- Accommodation recommendations with bike storage
- Points of interest and photo opportunities
- Emergency contacts and bike shop locations
- Packing checklist for bike touring
- Weather considerations for the season

STRUCTURE:
Day 1: [Route, accommodation, highlights]
Day 2: [Route, accommodation, highlights]
...etc.

Plus: General tips, emergency procedures, and backup plans for bad weather.
```

### Bike Purchase Decision

**Scenario**: Help someone choose between multiple bike options.

```text title="Decision-making prompt:"
Help me choose between these three bikes using a structured decision framework:

OPTION A: Trek Domane AL 2 - $1,100
- Aluminum frame, endurance geometry
- 16-speed Claris groupset
- Good for long rides and light racing

OPTION B: Giant Contend 3 - $825  
- Aluminum frame, comfortable geometry
- 16-speed Claris groupset
- Entry-level road bike

OPTION C: Specialized Allez - $950
- Aluminum frame, race geometry
- 16-speed Claris groupset
- More aggressive riding position

MY PROFILE:
- New to road cycling
- Plan to ride 2-3 times per week, 20-40 miles
- Want to join group rides eventually
- Budget: $1,000 (flexible to $1,200)
- Height: 5'8", athletic build
- Priority: comfort first, but want to grow into more serious riding

DECISION CRITERIA:
1. Value for money (weight: 25%)
2. Comfort for learning (weight: 30%)
3. Growth potential (weight: 25%)  
4. Resale value (weight: 10%)
5. Brand reputation/support (weight: 10%)

Please score each bike 1-10 on each criterion, calculate weighted scores, and provide a recommendation with reasoning.
```

### Training Plan Development

**Scenario**: Create a structured cycling training program.

```text title="Training plan prompt:"
Create a 12-week cycling training program with these specifications:

CYCLIST PROFILE:
- Current fitness: Can ride 25 miles at moderate pace
- Goal: Complete a 100-mile charity ride in 12 weeks
- Available time: 6-8 hours per week
- Experience: 6 months of casual cycling
- Age: 35, generally healthy

PROGRAM STRUCTURE:
- Weekly progression plan
- Mix of endurance, interval, and recovery rides
- Cross-training recommendations
- Nutrition guidelines for longer rides
- Equipment progression (when to upgrade)

WEEKS 1-4: Base Building
WEEKS 5-8: Build Phase
WEEKS 9-12: Peak and Taper

For each week include:
- Total riding time
- Specific workout descriptions
- Intensity guidelines (heart rate zones or perceived exertion)
- Rest and recovery recommendations
- Progress markers and testing

SPECIAL CONSIDERATIONS:
- Include weather alternatives (indoor options)
- Gradual mileage increases (10% rule)
- Injury prevention strategies
- Mental preparation for long rides
```

## Creative Applications

### Product Development Brainstorming

**Scenario**: Generate innovative bike accessory ideas.

```text title="Creative brainstorming prompt:"
Brainstorm innovative bike accessories that solve real problems cyclists face. Use this creative framework:

PROBLEM CATEGORIES:
1. Safety and visibility
2. Weather protection
3. Cargo and storage
4. Navigation and communication
5. Maintenance and repairs
6. Comfort and ergonomics

INNOVATION APPROACH:
- Combine existing technologies in new ways
- Apply solutions from other industries
- Focus on urban commuting challenges
- Consider smartphone integration
- Think about sustainability

FOR EACH IDEA:
- Problem it solves
- Target market
- Key features
- Estimated price range
- Competitive advantages
- Potential challenges

CONSTRAINTS:
- Must be technically feasible with current technology
- Price point accessible to average cyclists ($20-$200)
- Easy to install/use without special tools
- Compatible with most bike types

Generate 8-10 unique concepts, ranging from simple to complex innovations.
```

### Content Creation

**Scenario**: Generate blog content for a cycling website.

```text title="Content creation prompt:"
Create a blog post outline and introduction for a cycling website:

TOPIC: "10 Essential Skills Every New Cyclist Should Master"
AUDIENCE: Complete beginners who just bought their first bike
GOAL: Build confidence and safety awareness
TONE: Encouraging, practical, not intimidating

OUTLINE REQUIREMENTS:
- 10 distinct skills in logical learning order
- Brief description of each skill
- Why it's important for safety/enjoyment
- Quick tip for practicing each skill
- Estimated time to master each one

POST STRUCTURE:
1. Engaging introduction (2-3 paragraphs)
2. Main content (10 skills)
3. Conclusion with encouragement
4. Call-to-action

SEO CONSIDERATIONS:
- Include keywords: beginner cycling, bike skills, cycling safety
- Write for featured snippet optimization
- Include related topics for internal linking

Write the full introduction and outline the 10 skills with detailed descriptions.
```

## Technical Problem Solving

### Diagnostic Troubleshooting

**Scenario**: Create a systematic approach to bike problem diagnosis.

```text title="Diagnostic prompt:"
Create a diagnostic flowchart for this bike problem: "Bike makes noise when pedaling"

DIAGNOSTIC APPROACH:
Start with most common/easy-to-check causes and progress to complex ones.

FLOWCHART FORMAT:
Question → [Yes/No] → Next step or solution

INITIAL QUESTIONS:
1. When does the noise occur? (Always, only when pedaling hard, only when standing, etc.)
2. What type of noise? (Clicking, grinding, squeaking, rattling)
3. Where does it seem to come from? (Front, rear, middle of bike)

COMMON CAUSES TO CHECK:
- Loose pedals or crank arms
- Chain issues (dirty, stretched, misaligned)
- Bottom bracket problems
- Derailleur adjustment
- Loose accessories or components

STRUCTURE:
Start with the most likely causes and create a logical decision tree that leads to either a solution or "refer to bike shop for professional diagnosis."

Include:
- What to look for
- How to test
- Tools needed for basic checks
- When to stop and seek professional help
```

:::tip Using These Examples
These prompts demonstrate different techniques working together:
- Clear context setting
- Structured output requirements  
- Specific constraints and criteria
- Examples and formatting guidance
- Progressive difficulty levels

Adapt these templates to your specific needs by changing the details while keeping the underlying structure.
:::

## Customization Tips

1. **Adapt the Voice**: Change the tone and personality to match your brand or needs
2. **Modify Constraints**: Adjust budgets, timeframes, and requirements for your situation  
3. **Add Specificity**: Include more detailed requirements for your particular use case
4. **Change Examples**: Use examples relevant to your domain or audience
5. **Iterate and Improve**: Test prompts and refine based on the results you get

These examples show how prompt engineering can be applied to real-world scenarios, making AI assistance more practical and valuable for everyday tasks.