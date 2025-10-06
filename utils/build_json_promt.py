import json
import re
from typing import Dict, Union, Optional, Any

def build_block_prompt(payload: Union[str, Dict], original_config: Optional[Dict] = None, input_data_context: Optional[Dict] = None,language:str = 'vietnamese', **kwargs) -> str:
    """Build system instruction from payload with smart context_sources merging"""
    
    # Parse payload
    data = json.loads(payload) if isinstance(payload, str) else payload
    
    # Extract parts
    instruction = data.get('mission', '')
    input_data = data.get('input_schema', data.get('input', {}))
    output_data = data.get('output_schema', data.get('output', {}))
    
    # Smart merge context_sources if original_config is provided
    if original_config and 'input' in original_config:
        original_input = original_config.get('input', {})
        original_context = original_input.get('context_sources', {})
        current_context = input_data.get('context_sources', {})
        
        # If input_data_context is provided, use it as the source of new context
        if input_data_context:
            current_context = input_data_context

        
        if original_context and current_context:
            # Merge logic: keep original keys not in current, replace/add from current
            merged_context = original_context.copy()
            merged_context.update(current_context)
            input_data['context_sources'] = merged_context

        elif original_context and not current_context:
            # If no current context, use original
            input_data['context_sources'] = original_context

        elif current_context and not original_context:
            # If no original context, use current
            input_data['context_sources'] = current_context
    
    # Build markdown format
    parts = []
    
    # Task section
    if instruction:
        parts.append(f"# ROLE #\n{instruction}")
    
    # Input section
    if input_data:
        parts.append("# INPUT #")
        
        # Parse input fields
        user_question = input_data.get('user_question', '')
        context_sources = input_data.get('context_sources', {})
        
        if user_question:
            parts.append(f"## User Question ##\n{user_question}")
        
        if context_sources:
            parts.append("## Context Sources ##")
            if isinstance(context_sources, dict):
                for key, value in context_sources.items():
                    if key == 'rules' and isinstance(value, str) and re.search(r'\d+\.', value):
                        # Format rules as list
                        rules_list = [line.strip() for line in value.split('\n') if line.strip()]
                        formatted_rules = '\n'.join([f"- {rule}" for rule in rules_list])
                        parts.append(f"**{key.upper()}:**\n{formatted_rules}")
                    else:
                        parts.append(f"**{key.upper()}:** {value}")
            elif isinstance(context_sources, list):
                for i, item in enumerate(context_sources):
                    parts.append(f"**SOURCE {i+1}:** {item}")
            else:
                parts.append(f"**CONTEXT:** {context_sources}")
    
    
    # Output format
    if output_data:
        parts.append(f"# OUTPUT JSON FORMAT #\n{json.dumps(output_data, ensure_ascii=False, indent=2)}")
    
    # Constraints
    parts.append(f"""# RÀNG BUỘC #
- Chỉ trả về JSON hợp lệ
- Không thêm text thừa
- Tuân thủ chặt chẽ format trên
- Câu trả lời phải bằng tiếng {language}""")
    
    return '\n\n'.join(parts)