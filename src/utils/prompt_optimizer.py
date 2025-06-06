# src/utils/prompt_optimizer.py
class PromptOptimizer:
    @staticmethod
    def create_few_shot_examples():
        """Create few-shot examples for better LLM performance"""
        examples = {
            'resume_screening': [
                {
                    'input': 'Software Engineer with Python, 2 years experience',
                    'output': '{"overall_score": 75, "recommendation": "CONSIDER"}'
                },
                {
                    'input': 'Senior Developer, Java, Spring, 5 years',
                    'output': '{"overall_score": 90, "recommendation": "HIRE"}'
                }
            ],
            'sentiment_analysis': [
                {
                    'input': 'I love working here, great team!',
                    'output': '{"sentiment_score": 0.8, "attrition_risk": "LOW"}'
                },
                {
                    'input': 'Considering other opportunities',
                    'output': '{"sentiment_score": -0.3, "attrition_risk": "HIGH"}'
                }
            ]
        }
        return examples
    
    @staticmethod
    def optimize_prompt_with_examples(base_prompt: str, task_type: str) -> str:
        """Add few-shot examples to improve prompt performance"""
        examples = PromptOptimizer.create_few_shot_examples()
        
        if task_type in examples:
            example_text = "\n\nHere are some examples:\n"
            for example in examples[task_type]:
                example_text += f"Input: {example['input']}\n"
                example_text += f"Output: {example['output']}\n\n"
            
            return base_prompt + example_text
        
        return base_prompt