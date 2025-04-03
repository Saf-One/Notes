# Universal Note Processing System

## How to Use This System

1. **Add your raw notes** to the `input_notes.md` file below the divider line.

2. **Process your notes** with one of these steps:
   - Run the note processor script
   - Apply the note processor rules manually
   - Use the automated formatter

3. **The system will automatically**:
   - Read the rules from `note_processor_rules.md`
   - Identify the topic of your notes
   - Process your raw notes from `input_notes.md`
   - Format them according to the standardized structure
   - Create or update the appropriate document in the correct directory
   - Update the project metrics file
   - Clear the input file for your next use

## Example

### Raw Input:
```
PYTHON DECORATORS
syntax: @decorator_name
allows modifying function behavior
types: function decorators, class decorators
can be stacked
executed at definition time
built-in examples: @property, @classmethod, @staticmethod
```

### After Processing:
This would be transformed into a properly formatted document with additional context, explanations, and examples, then placed in an appropriate directory (e.g., `Python/python_decorators.md`).

## Tips for Best Results

1. Include a clear topic name at the beginning of your notes
2. List key attributes in simple format (key = value or key: value)
3. Mention any special characteristics or important points
4. Provide any known examples if available
5. Don't worry about formatting - the system handles that

## Customizing the Process

You can modify the rules in `note_processor_rules.md` to change:
- The structure of processed notes
- Required sections for different topic types
- Formatting conventions
- Point allocation for project metrics
- Directory organization patterns 