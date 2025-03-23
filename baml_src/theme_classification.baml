class Theme {
  title string
  description string
}


class ThemeClassification {
  model_reasoning string @description(#"
    The chain of thought reasoning steps you followed to determine the matching theme in atmost 50 words.
  "#)
  chosen_theme Theme
}

function ClassifyTextByTheme(query: string) -> ThemeClassification {
  client "Llama_405b"
  prompt #"
    You are an advanced AI assistant that classifies text based on predefined themes. Your task is to analyze the provided text and determine the most relevant theme from the given options for themes. You must the below instructions to complete the task.

    Instructions for the task:
    1. Carefully read the input the text.
    2. Compare its meaning with the themes provided. For each theme you are provided with title and description. Read the description of the theme for comparison.
    3. Select the theme that best matches the intent and context of the input text.
    4. Provide the chain of thought reasoning steps you followed to determine the matching theme in atmost 50 words.
    5. Provide output in appropriate JSON format.

    Input:
    {{ query }}

    {{ ctx.output_format }}
  "#
}


test rohit_test_classify_text_by_theme {
  functions [ClassifyTextByTheme]
  args {
    query #"
      {
    "text": "I am calling because I have a problem with my internet connection",
    "themes": [
        {
            "title": "Technical support",
            "description": "The customer is calling for technical support"
        },
        {
            "title": "Billing",
            "description": "The customer is calling for billing issues"
        },
        {
            "title": "Refund",
            "description": "The customer is calling for a refund"
        }
    ]
}
    "#
  }
}