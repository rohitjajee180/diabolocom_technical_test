enum Gender {
  Male
  Female
  Other
}

enum ContactMethod {
  Email
  Phone
}

class PersonalInfo {
  first_name string
  last_name string
  gender Gender?
}

class ContactInfo {
  email string
  phone string?
  preferred_contact_method ContactMethod
  call_reasons string[]
}

class CustomerInformation {
  personal_info PersonalInfo
  contact_info ContactInfo
}

function ExtractCustomerInformation(conversation: string) -> CustomerInformation {
  client "Llama_405b"
  prompt #"
    You are an advanced AI assistant that collects customer information based on predefined fields. Your task is to analyze the provided conversation and extract the relevant customer information. You must follow the below instructions to complete the task.

    Instructions for the task:
    1. Carefully read the input conversation.
    2. Extract the relevant customer information based on the provided fields.
    3. Provide the extracted information in the appropriate JSON format.
    4. If the customer doesn't provide the information, return null for that field.
    5. Provide output in appropriate JSON format.
    Input:
    {{ conversation }}

    {{ ctx.output_format }}
  "#
}

test rohit_test_fill_form {
  functions [ExtractCustomerInformation]
  args {
    conversation #"
      {
    "text": "Agent: Good morning! Thank you for reaching out. I’ll need to collect some basic details to assist you better. Could you please provide your first and last name? Customer: Sure! My name is John Doe. Agent: Thank you, John. May I also ask for your gender? Customer: I'd prefer not to share that at the moment. Agent: No problem at all. Now, for contact purposes, could you share your email address? Customer: Yes, my email is johndoe@example.com. Agent: Great! Do you have a phone number where we can reach you? Customer: I’d rather not provide that right now. Agent: That’s completely fine. How would you prefer us to contact you—by email or phone? Customer: Please contact me via Email. Agent: Understood! Lastly, can you share the reason for your call today? Customer: I’m not ready to specify that just yet. Agent: That’s okay, John! I’ve noted everything down. If you need any further assistance, feel free to reach out. Have a great day!"
}
    "#
  }
}