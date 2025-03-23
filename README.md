# Technical Test Implementation Report

## Setup and Running Instructions

### Prerequisites
- Docker Desktop installed and running
- Visual Studio Code with Dev Containers extension installed

### Running the Application
1. Clone the repository
2. Open the project in VS Code
3. When prompted "Reopen in Container", click "Yes" 
   - Alternatively, press F1, type "Reopen in Container" and select the option
4. The dev container will automatically:
   - Set up Python 3.11
   - Install UV package manager
   - Install project dependencies
5. Copy `.env.example` to `.env` and add your Nebius API key
6. Run the FastAPI application:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```
7. Access the API documentation at `http://localhost:8000/docs`

---

# Solutions to 2 use cases and 3 bonus tasks

## Use Case 1: Text Classification

**Endpoint:** `/classify_text`

**Method:** `POST`

This endpoint allows you to classify input text into predefined themes. It's ideal for categorizing customer queries, support tickets, or any text that needs thematic classification.

### Request Body:
```json
{
    "text": "Your input text here",
    "available_themes": [
        {
            "title": "Theme Title",
            "description": "Theme Description"
        }
    ]
}
```

### Response:
```json
{
    "model_reasoning": "Explanation of why this classification was chosen",
    "chosen_theme": {
        "title": "Selected Theme",
        "description": "Theme Description"
    },
    "statistics": {
        "frequency": 1,
        "total_tries": 1,
        "confidence": 1.0
    }
}
```

---

## Use Case 2: Form Completion

**Endpoint:** `/form_filling`

**Method:** `POST`

This endpoint extracts structured customer information from conversation text. It's perfect for automatically filling out forms based on customer interactions.

### Request Body:
```json
{
    "text": "Your conversation text here"
}
```

### Response:
Returns structured customer information including:
- Personal information (name, gender)
- Contact details (email, phone, preferred contact method)
- Additional context (reasons for contact)

---

## Bonus 1: Parallel Classifications with Confidence Scoring

**Endpoint:** `/classify_text`

**Method:** `POST`

**Additional Parameter:** `num_tries` (1-10)

This enhanced version of the classification endpoint performs multiple classification attempts to build consensus and provide confidence scores.

### Request:
```json
{
    "text": "Your input text here",
    "available_themes": [...],
    "num_tries": 5
}
```

### Response:
```json
{
    "model_reasoning": "Consensus-based reasoning",
    "chosen_theme": {
        "title": "Most Frequent Theme",
        "description": "Theme Description"
    },
    "statistics": {
        "frequency": 4,
        "total_tries": 5,
        "confidence": 0.8
    }
}
```

---

## Bonus 2: Dynamic Schema Form Completion

**Endpoint:** `/generic_form_completion`

**Method:** `POST`

This flexible endpoint allows you to define custom schemas for information extraction, making it adaptable to any form structure.

### Request Body:
```json
{
    "conversation": {
        "text": "Your conversation text"
    },
    "json_schema": {
        "type": "object",
        "properties": {
            "your_custom_field": {"type": "string"}
        }
    }
}
```

**Additional Parameter:** `max_retries` (1-5, default: 3)

### Response:
Returns the structured information according to the provided JSON schema.

---

## Bonus 3: Streamed Form Completion

**Endpoint:** `/form_filling/stream`

**Method:** `POST`

This endpoint provides real-time streaming of form completion results using Server-Sent Events (SSE), ideal for responsive user interfaces.

### Request Body:
```json
{
    "text": "Your conversation text here"
}
```

### Response:
Streams data in SSE format:
```
data: {"personal_info": {"first_name": "John"}}

data: {"contact_info": {"email": "john@example.com"}}