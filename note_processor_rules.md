# Universal Note Processor Rules

## Overview
This file contains rules for processing and improving notes on any topic. The system will automatically enhance any raw notes placed in the `input_notes.md` file according to these specifications, organizing them into appropriate topic directories.

## Note Organization Rules

1. **Topic-based directory structure**
   - Identify the main topic of the notes
   - Use existing directory if it matches the topic
   - Create new directory if needed
   - Place related notes in the same directory

2. **Filename conventions**
   - Use descriptive filenames in snake_case
   - Include topic name in filename
   - Add specific subtopic if applicable
   - Example: `java_collections_framework.md`, `python_decorators.md`

3. **Topic index/home files**
   - Create a Home.md file in each topic directory (e.g., `Collection framework/Home.md`)
   - List all documents within the topic with brief descriptions
   - Include creation/update dates for each document
   - Organize subtopics in logical groupings
   - Add a table of contents for quick navigation
   - Include a link to the main home page

4. **Navigation links**
   - Add consistent navigation elements at the top and bottom of each file
   - Top navigation format:
     ```markdown
     [← Home](Home.md) | [Main Home](../Home.md) | [Next: SubTopic →](subtopic.md)
     ```
   - Bottom navigation format:
     ```markdown
     ---
     [← Home](Home.md) | [Main Home](../Home.md) | [Back to Top](#topic-name) | [Next: SubTopic →](subtopic.md)
     ```
   - Adjust links based on document context and location

5. **Front and back link management**
   - Automatically update the main Home.md when new topics are added
     * Add new topic to the Topics table with description and count
     * Include link to the topic's Home.md file
     * Add latest document to Recently Updated section
   - Update each Topic's Home.md when new documents are added
     * Add entry to Available Documents table
     * Update section descriptions if needed
     * Ensure navigation links are complete and correct
   - Maintain bidirectional navigation
     * Every document should link to its topic home and main home
     * Main home should link to all topic homes
     * Topic homes should link to all documents in that topic

## Note Structure Rules

1. **Format all notes into clearly defined sections**
   - Use Markdown headers (# for main titles, ## for sections, ### for subsections)
   - Group related information under appropriate headers
   - Maintain consistent hierarchy based on topic

2. **Transform bullet points into structured data**
   - Convert simple key-value notes (e.g., "default capacity = 10") into formatted attributes
   - Format as "**Key**: Value" for consistent styling
   - Group related attributes together

3. **Standardize information categories for each note type**
   - Identify appropriate categories based on the topic
   - For technical topics: implementation, behavior, usage, examples
   - For conceptual topics: definition, characteristics, applications, examples
   - For procedural topics: steps, requirements, variations, best practices

4. **Enhance with additional contextual information**
   - Add relevant background information
   - Include appropriate comparisons to related concepts
   - Add practical applications or use cases
   - Identify common pitfalls or important considerations

5. **Create comparison tables for related concepts**
   - Use tabular format for easy comparison
   - Ensure consistent columns across compared items
   - Focus on key differentiating factors

## Styling Rules

1. **Use consistent formatting for emphasis**
   - **Bold** for important concepts, terms, and attribute names
   - *Italic* for supplementary information and emphasis
   - `Code formatting` for code examples, technical terms, and syntax

2. **Use hierarchical list structures**
   - Main points as primary bullets
   - Supporting details as nested bullets
   - Code examples as separate blocks with appropriate language tags

3. **Ensure readability**
   - Short, focused paragraphs
   - Clear section breaks
   - Consistent spacing
   - Use code blocks for all code samples with appropriate language tags

## Required Sections (Adapt Based on Topic)

1. **Overview** - Brief introduction to the topic
2. **Key Concepts** - Fundamental ideas and terminology
3. **Details** - In-depth explanation appropriate to the topic
4. **Examples** - Practical examples, code samples, or illustrations
5. **Use Cases** - When and how to apply the concept
6. **Related Topics** - Connections to other relevant subjects
7. **References** - Sources for additional information (if available)

## Metrics Tracking Integration

1. **Update .projectmetrics/improvements.md with each improvement**
   - Document points earned in each category
   - Calculate cumulative improvement percentage
   - Add specific details about improvements made
   - Update with current date

2. **Point allocation guidelines**
   - Structure improvements: 5-10 points each
   - Content additions: 10-20 points each
   - Visual enhancements: 5-15 points each
   - New sections: 20-30 points each
   - New topic creation: 40-50 points
   - Navigation improvements: 10-15 points each

## Workflow Process

1. User places raw notes in `input_notes.md`
2. System identifies the topic and appropriate directory
3. System processes notes according to these rules
4. Enhanced notes are added to the appropriate document
5. Update or create the topic's Home.md file with new entry
6. Add navigation links to the top and bottom of the document
7. Update main Home.md with new topic information and links
8. Ensure all bidirectional navigation is maintained and updated
9. Metrics file is updated with improvements
10. Input file is cleared for next use 