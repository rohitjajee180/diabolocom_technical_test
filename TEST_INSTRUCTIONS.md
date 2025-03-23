# **Technical Test Diabolocom AI - Data Scientist / LLM Ops Engineer**

## Introduction

Welcome to our technical test! This exercise is designed to assess your problem-solving approach, how you structure your work, and your intuition about LLMs. We are not necessarily looking for a fully polished solution. Instead, we want to understand your methodology and how you adapt when tackling an end-to-end use case.

## Instructions
The goal is to build an API with two routes that address the following use cases:
1. <b>Text Classification</b> – Classify a given text into a list of provided themes.
2. <b>Form Completion</b> – Extract structured information from a text to populate a predefined form.

### Technical Stack Constraints
You'll have several constraints in terms of stack to use:
* <b>Infra/Deployment</b>: We use [UV](https://docs.astral.sh/uv/) for managing projects. Please use it as well.
* <b>Text Generation</b>: We rely on [BAML](https://docs.boundaryml.com/) for constrained generation due to its efficiency in structured outputs. You will need to integrate it into your implementation. One of our evaluation goal is to see how you adapt to new tools.
* <b>API Framework</b>: You are free to choose any framework, but we recommend [FastAPI](https://fastapi.tiangolo.com/) due to its performance and ease of use.


## Use case 1. Text classification
### Input format
The API should accept input in the following format:
```json
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
```

### Output format
The API should return a response like this:
```json
{
    "model_reasoning": "This text is about technical support, therefore the chosen theme is 'Technical support'.",
    "chosen_theme": {
        "title": "Technical support",
        "description": "The customer is calling for technical support"
    }
}
```

## Use case 2. Form completion
### JSON Schema to Fill
The API should extract structured data from a given text and populate the following JSON schema:
```json
{
  "title":"Customer Information Form",
  "type":"object",
  "properties":{
    "personal_info":{
      "type":"object",
      "properties":{
        "first_name":{
          "type":"string",
          "description":"The customer's first name"
        },
        "last_name":{
          "type":"string",
          "description":"The customer's last name"
        },
        "gender":{
          "type":"string",
          "enum":[
            "Male",
            "Female",
            "Other"
          ],
          "description":"The customer's gender"
        }
      },
      "required":[
        "first_name",
        "last_name",
        "gender"
      ]
    },
    "contact_info":{
      "type":"object",
      "properties":{
        "email":{
          "type":"string",
          "format":"email",
          "description":"The customer's email address"
        },
        "phone":{
          "type":"string",
          "description":"The customer's phone number"
        },
        "preferred_contact_method":{
          "type":"string",
          "enum":[
            "Email",
            "Phone"
          ],
          "description":"The customer's preferred method of contact"
        },
        "call_reasons":{
          "type":"array",
          "items":{
            "type":"string"
          },
          "description":"The reasons for the call",
          "minItems":1
        }
      }
    }
  },
  "required":[
    "personal_info",
    "contact_info"
  ]
}
```

### Input format
The API should accept input in the following format:
```json
{
    "text": "Agent: Good morning! Thank you for reaching out. I’ll need to collect some basic details to assist you better. Could you please provide your first and last name? Customer: Sure! My name is John Doe. Agent: Thank you, John. May I also ask for your gender? Customer: I'd prefer not to share that at the moment. Agent: No problem at all. Now, for contact purposes, could you share your email address? Customer: Yes, my email is johndoe@example.com. Agent: Great! Do you have a phone number where we can reach you? Customer: I’d rather not provide that right now. Agent: That’s completely fine. How would you prefer us to contact you—by email or phone? Customer: Please contact me via Email. Agent: Understood! Lastly, can you share the reason for your call today? Customer: I’m not ready to specify that just yet. Agent: That’s okay, John! I’ve noted everything down. If you need any further assistance, feel free to reach out. Have a great day!"
}
```

### Output format
The API should return a response like this:
```json
{
  "personal_info": {
    "first_name": "John",
    "last_name": "Doe",
    "gender": null
  },
  "contact_info": {
    "email": "johndoe@example.com",
    "phone": null,
    "preferred_contact_method": "Email",
    "call_reasons": null
  }
}
```

## Bonuses

Below are three bonuses; you can choose one to complete if you have time (or more if you're feeling ambitious). These are not mandatory, but they will help us understand your skills better.

### Bonus 1: Probabilistic Text Classification

Since LLMs are stochastic, you can enhance the classification by running multiple parallel classifications and providing an estimate of the model’s confidence in its choice.

### Bonus 2: Generalized Form Completion

Modify the form completion functionality to dynamically handle <b>any</b> given JSON schema instead of only the predefined one.

### Bonus 3: Streamed form completion

For real time applications, we might want to stream the llm completion. Implement a streamed version of the form completion functionality.

## Additional Notes
* <b>LLM Inference</b>: You can use [Nebius's inference API](https://docs.nebius.com/studio/inference), which offers free usage up to 600 RPM or 400,000 TPM. This is a quick and efficient way to get started.
* <b>BAML Editor Support</b>: We recommend using VSCode or Cursor with the official [BAML extension](https://docs.boundaryml.com/guide/installation-editors/vs-code-extension) for improved structured generation development.