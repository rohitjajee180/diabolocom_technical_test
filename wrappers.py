from baml_client.async_client import b
from dotenv import load_dotenv
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
import asyncio
from collections import Counter
import json
from jsonschema import validate, ValidationError, SchemaError
# Load environment variables from .env file if it exists
load_dotenv()


# Define the Theme model
class Theme(BaseModel):
    title: str
    description: str


# Define the CustomerQuery model
class CustomerQuery(BaseModel):
    text: str
    themes: List[Theme]


class ConversationInput(BaseModel):
    text: str


async def classify_text_wrapper(
    query: CustomerQuery,
    num_tries: int = 1
) -> Dict[str, Any]:
    """
    Run classification multiple times and return the most frequent theme with 
    consensus.
    Args:
        query: CustomerQuery object containing text and themes
        num_tries: Number of times to run the classification
    Returns:
        Dict containing the most common theme, and statistics
    """
    # Convert Pydantic model to JSON string using model_dump_json()
    query_str = query.model_dump_json()
    
    # Run the classification num_tries times
    results = await asyncio.gather(
        *[b.ClassifyTextByTheme(query_str) for _ in range(num_tries)]
    )
    
    # Extract themes and their data
    themes = [result.chosen_theme.title for result in results]
    theme_data = {
        result.chosen_theme.title: result for result in results
    }
    
    # Count theme frequencies
    theme_counts = Counter(themes)
    
    # Get the most common theme
    most_common_theme = theme_counts.most_common(1)[0]
    theme_title, frequency = most_common_theme
    
    # Get the full result for the most common theme
    most_common_result = theme_data[theme_title]
    
    # Return with additional statistics
    return {
        "model_reasoning": most_common_result.model_reasoning,
        "chosen_theme": {
            "title": most_common_result.chosen_theme.title,
            "description": most_common_result.chosen_theme.description
        },
        "statistics": {
            "frequency": frequency,
            "total_tries": num_tries,
            "confidence": frequency / num_tries
        }
    }


async def extract_customer_information_wrapper(
    conversation: ConversationInput
):
    conversation_str = conversation.model_dump_json()
    return await b.ExtractCustomerInformation(conversation_str)


async def extract_customer_information_wrapper_stream(
    conversation: ConversationInput
):
    """
    Streaming wrapper for customer information extraction.
    Yields partial results as they become available.
    
    Args:
        conversation: ConversationInput object containing the conversation
    Yields:
        Partial customer information objects as they are generated
    """
    conversation_str = conversation.model_dump_json()
    stream = b.stream.ExtractCustomerInformation(conversation_str)
    async for chunk in stream:
        yield f"data: {chunk.model_dump_json()}\n\n"


async def generic_form_completion_wrapper(
    conversation: ConversationInput,
    schema: Dict[str, Any],
    max_retries: int = 3
) -> Dict[str, Any]:
    """
    Wrapper for generic form completion that extracts information based on
    provided schema.
    Args:
        conversation: ConversationInput object containing the conversation
        schema: JSON schema dictionary defining the output structure
        max_retries: Maximum number of retries for JSON parsing failures
    Returns:
        Dict containing the extracted information based on the schema
    Raises:
        SchemaError: If the provided schema is not a valid JSON Schema
        ValidationError: If the schema doesn't follow basic JSON Schema rules
        ValueError: If all retries fail to parse the JSON response
    """
    # Validate that the schema is a valid JSON Schema
    try:
        # This meta-schema validates that 'schema' is a valid JSON Schema
        meta_schema = {
            "type": "object",
            "required": ["type", "properties"],
            "properties": {
                "type": {"type": "string", "enum": ["object"]},
                "properties": {"type": "object"},
                "required": {
                    "type": "array",
                    "items": {"type": "string"}
                }
            }
        }
        # First validate the schema against the meta-schema
        validate(instance=schema, schema=meta_schema)
        
    except SchemaError as e:
        raise SchemaError(
            f"Invalid JSON Schema format: {str(e)}"
        )
    except ValidationError as e:
        raise ValidationError(
            f"Schema must be an object type with properties: {str(e)}"
        )

    conversation_str = conversation.model_dump_json()
    schema_str = json.dumps(schema)
    
    last_error: Optional[Exception] = None
    for attempt in range(max_retries):
        try:
            result_str = await b.ExtractFormInformation(
                conversation_str,
                schema_str
            )
            return json.loads(result_str)
        except json.JSONDecodeError as e:
            last_error = e
            if attempt < max_retries - 1:
                # Wait with exponential backoff before retrying
                await asyncio.sleep(2 ** attempt)
                continue
    
    # If we get here, all retries failed
    raise ValueError(
        f"Failed to parse JSON response after {max_retries} attempts. "
        f"Last error: {str(last_error)}"
    )
