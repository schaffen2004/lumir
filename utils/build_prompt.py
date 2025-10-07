import json
import os
from typing import Dict, Union, Optional, Any
def generate_section(configs):
    section = []
    section.append(f"### Section: {configs['name']}")
    section.append(f"- **Format**:{configs['format']}")
    section.append(f"- **Tone**:{configs['tone']}")
    section.append(f"- **Content**:{configs['content']}")
    
    return '\n'.join(section)
    
def generate_format(format_config):
    format_parts = []
    format_parts.append('{')
    for key, value in format_config.items():
        format_parts.append(f'"{key}":"{value}"')
    format_parts.append('}')

    return '\n'.join(format_parts)
    

def build_block_prompt(payload: Union[str, Dict]) -> str:
    """
    Build a prompt string from the JSON configuration file.

    Args:
        payload: Either a string path to JSON config or a dictionary containing the configuration

    Returns:
        str: Formatted prompt string
    """
    # Load configuration
    if isinstance(payload, str):
        config_path = payload
        if not os.path.isabs(config_path):
            # Relative path from current directory
            config_path = os.path.join(os.getcwd(), config_path)

        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
    else:
        config = payload

    # Extract components from config
    role = config.get('prompt_role', '')
    goal = config.get('goal', '')
    input = config.get('input', {})
    output = config.get('output', {})
    context = output.get('context')
    user_question = input.get('user_question','')
    external_data = input.get('external_data','')
    context = config.get("context_souces",{})
    definition = context.get("definitions",{})
    steps = context.get("answer_steps",{})
    # Build prompt string
    parts = []

    if role:
        parts.append(f"# ROLE\n{role}\n")
    
    if goal:
        parts.append(f"# GOAL\n{goal}\n")
    
    if input:
        parts.append("# INPUT\n")
        
        parts.append("## User Question")
        parts.append(f"{user_question}\n")
        
        if external_data:
            parts.append("## External Data")
            for index,data in enumerate(external_data):
                parts.append(f"**Source {index+1}**: {data}")
    
    if context:
        parts.append("\n# CONTEXT SOURCES\n")
        
        parts.append('## Definitions')
        for key,value in definition.items():
            parts.append(f"- **{key}**: {value}")
        
        parts.append("\n## Answer Steps")
        for step in steps:
            parts.append(f"- {step}")
    
          
    if output:
        parts.append("\n# OUTPUT #\n")
        
        parts.append("## Output Format")
        format = generate_format(output.get("format",{}))
        parts.append(format)
        
        parts.append("\n## Output Structure")
        for section in output.get("output_structure",[]):
            content = generate_section(section)
            parts.append(f"\n{content}")
        
        parts.append("\n## Output Language")
        parts.append(output.get('language',"Vietnamese"))
    
    return "\n".join(parts)