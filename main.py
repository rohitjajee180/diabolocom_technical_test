from fastapi import FastAPI, Query
from wrappers import (
    classify_text_wrapper,
    extract_customer_information_wrapper,
    extract_customer_information_wrapper_stream,
    generic_form_completion_wrapper,
    CustomerQuery,
    ConversationInput
)
from typing import Dict, Any
from fastapi.responses import StreamingResponse
from pydantic import Field, BaseModel

APP_NAME = "Customer Service Assistant"
APP_DESCRIPTION = (
    "A customer service assistant that can classify text and "
    "extract customer information"
)


app = FastAPI(
    title=APP_NAME,
    description=APP_DESCRIPTION,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)


@app.post(
    "/classify_text",
    response_model=Dict[str, Any],
    tags=["Classification"],
    summary="Classify text into predefined themes"
)
async def classify_text(
    query: CustomerQuery,
    num_tries: int = Query(
        default=1,
        ge=1,
        le=10,
        description="Number of classification attempts for consensus"
    )
):
    """
    Classifies the input text into predefined themes with consensus mechanism.

    Parameters:
    - **query**: CustomerQuery object containing text and available themes
    - **num_tries**: Number of classification attempts (default: 1)

    Returns:
    A dictionary containing:
    - **model_reasoning**: Explanation of the classification decision
    - **chosen_theme**: The selected theme with title and description
    - **statistics**: Consensus statistics including frequency and confidence

    Example:
    ```json
    {
        "model_reasoning": "The text discusses customer service issues",
        "chosen_theme": {
            "title": "Customer Support",
            "description": "Topics related to customer service"
        },
        "statistics": {
            "frequency": 3,
            "total_tries": 3,
            "confidence": 1.0
        }
    }
    ```
    """
    return await classify_text_wrapper(query, num_tries)


@app.post(
    "/form_filling",
    tags=["Form Extraction"],
    summary="Extract customer information from conversation"
)
async def form_filling(conversation: ConversationInput):
    """
    Extracts structured customer information from a conversation.

    Parameters:
    - **conversation**: ConversationInput object containing the conversation
      text

    Returns:
    A structured object containing extracted customer information including:
    - Personal information (name, gender, etc.)
    - Contact details (email, phone, preferred contact method)
    - Additional context (call reasons, etc.)

    Example Request:
    ```json
    {
        "text": "Agent: What's your name? Customer: John Doe"
    }
    ```
    """
    return await extract_customer_information_wrapper(conversation)


@app.post(
    "/form_filling/stream",
    tags=["Form Extraction"],
    summary="Stream customer information extraction results"
)
async def form_filling_stream(conversation: ConversationInput):
    """
    Streams the extraction of customer information in real-time using
    Server-Sent Events (SSE).

    Parameters:
    - **conversation**: ConversationInput object containing the conversation
      text

    Returns:
    A streaming response where each event contains a partial result of the
    extraction process.

    Example Event Data:
    ```json
    {
        "personal_info": {
            "first_name": "John"
        }
    }
    ```

    Note:
    - The response is streamed using SSE format
    - Each event starts with 'data: ' prefix
    - Events are separated by double newlines
    - Client should handle partial updates appropriately
    """
    return StreamingResponse(
        extract_customer_information_wrapper_stream(conversation),
        media_type="text/event-stream"
    )


class GenericFormRequest(BaseModel):
    conversation: ConversationInput
    json_schema: Dict[str, Any] = Field(
        ...,
        description="JSON Schema defining the structure of the output",
        example={
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "number"}
            },
            "required": ["name"]
        }
    )


@app.post(
    "/generic_form_completion",
    tags=["Form Extraction"],
    summary="Extract information using custom schema"
)
async def generic_form_completion(
    request: GenericFormRequest,
    max_retries: int = Query(
        default=3,
        ge=1,
        le=5,
        description="Maximum number of retry attempts for parsing"
    )
):
    """
    Extracts information from conversation using a custom JSON schema.

    Parameters:
    - **request**: Request object containing:
      - conversation: ConversationInput object with the conversation text
      - json_schema: JSON Schema defining the structure of the output
    - **max_retries**: Maximum number of retry attempts for parsing
      (default: 3)

    Returns:
    A dictionary containing the extracted information structured according to
    the provided schema.

    Example Request:
    ```json
    {
        "conversation": {
            "text": "Agent: What's your name? Customer: John Doe"
        },
        "json_schema": {
            "type": "object",
            "properties": {
                "customer": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "age": {"type": "number"}
                    },
                    "required": ["name"]
                }
            }
        }
    }
    ```

    Raises:
    - **SchemaError**: If the provided schema is not a valid JSON Schema
    - **ValidationError**: If schema doesn't follow required structure
    - **ValueError**: If parsing fails after all retry attempts
    """
    return await generic_form_completion_wrapper(
        request.conversation,
        request.json_schema,
        max_retries
    )
