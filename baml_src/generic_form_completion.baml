function ExtractFormInformation(conversation: string, schema: string) -> string {
  client "Llama_405b"
  prompt #"
    You are an advanced AI assistant that extracts information from conversations based on a provided JSON schema. Your task is to analyze the provided conversation and extract the relevant information according to the schema. You must follow the below instructions to complete the task.

    Instructions for the task:
    1. Carefully read the input conversation.
    2. Extract the relevant information based on the provided JSON schema.
    3. Provide the extracted information in the appropriate JSON format that matches the schema exactly.
    4. If certain information is not available in the conversation, use null for optional fields or empty arrays/objects as appropriate.
    5. Ensure the output strictly follows the provided JSON schema structure.
    6. Your response must be a single valid JSON string that can be parsed by JSON.parse().
    7. Do not include any additional text, explanations, or formatting - only the JSON string.

    Schema:
    {{ schema }}

    Input:
    {{ conversation }}

    Remember: Respond only with a valid JSON string that matches the schema structure.
  "#
}

test rohit_test_fill_form {
  functions [ExtractFormInformation]
  args {
    conversation #"
      {
    "text": "Agent: Good morning! Thank you for reaching out. I'll need to collect some basic details to assist you better. Could you please provide your first and last name? Customer: Sure! My name is John Doe. Agent: Thank you, John. May I also ask for your gender? Customer: I'd prefer not to share that at the moment. Agent: No problem at all. Now, for contact purposes, could you share your email address? Customer: Yes, my email is johndoe@example.com. Agent: Great! Do you have a phone number where we can reach you? Customer: I'd rather not provide that right now. Agent: That's completely fine. How would you prefer us to contact you—by email or phone? Customer: Please contact me via Email. Agent: Understood! Lastly, can you share the reason for your call today? Customer: I'm not ready to specify that just yet. Agent: That's okay, John! I've noted everything down. If you need any further assistance, feel free to reach out. Have a great day!"
}
    "#
    schema #"
    {
      "type": "object",
      "properties": {
        "personal_info": {
          "type": "object",
          "properties": {
            "first_name": {"type": "string"},
            "last_name": {"type": "string"},
            "gender": {
              "type": "string",
              "enum": ["Male", "Female", "Other"]
            }
          },
          "required": ["first_name", "last_name"]
        },
        "contact_info": {
          "type": "object",
          "properties": {
            "email": {"type": "string"},
            "phone": {"type": "string"},
            "preferred_contact_method": {
              "type": "string",
              "enum": ["Email", "Phone"]
            },
            "call_reasons": {
              "type": "array",
              "items": {"type": "string"}
            }
          },
          "required": ["email", "preferred_contact_method"]
        }
      },
      "required": ["personal_info", "contact_info"]
    }
    "#
  }
}